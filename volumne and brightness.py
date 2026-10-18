
import math
import subprocess
import time
import cv2
import mediapipe as mp

hands_module = mp.solutions.hands
drawing = mp.solutions.drawing_utils

camera = cv2.VideoCapture(0)

mode = "VOLUME"
last_adjustment = 0

if not camera.isOpened():
    raise RuntimeError("Camera not available")

def set_volume(value):
    subprocess.run(
        ["osascript", "-e", f"set volume output volume {value}"],
        check=False
    )

def set_brightness(value):
    subprocess.run(
        ["brightness", str(value / 100)],
        check=False
    )

with hands_module.Hands(
    max_num_hands=1,
    min_detection_confidence=0.65,
    min_tracking_confidence=0.6
) as tracker:

    while True:
        success, frame = camera.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = tracker.process(rgb)

        message = "Show thumb and index finger"

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]

            drawing.draw_landmarks(
                frame,
                hand,
                hands_module.HAND_CONNECTIONS
            )

            thumb = hand.landmark[4]
            index = hand.landmark[8]

            x1 = int(thumb.x * width)
            y1 = int(thumb.y * height)

            x2 = int(index.x * width)
            y2 = int(index.y * height)

            cv2.circle(frame, (x1, y1), 9, (0, 255, 255), -1)
            cv2.circle(frame, (x2, y2), 9, (0, 255, 255), -1)

            cv2.line(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 255, 0),
                3
            )

            distance = math.hypot(
                thumb.x - index.x,
                thumb.y - index.y
            )

            value = round(
                max(0, min(100, (distance - 0.03) / 0.27 * 100))
            )

            message = f"{mode}: {value}%"

            if time.monotonic() - last_adjustment > 0.3:

                try:
                    if mode == "VOLUME":
                        set_volume(value)
                    else:
                        set_brightness(value)

                except FileNotFoundError:
                    message = "Brightness utility not installed"

                last_adjustment = time.monotonic()

        cv2.putText(
            frame,
            message,
            (20, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "V: Volume  B: Brightness  Q: Quit",
            (20, height - 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.imshow("Volume and Brightness Control", frame)

        key = cv2.waitKey(1) & 255

        if key == ord("q"):
            break

        if key == ord("b"):
            mode = "BRIGHTNESS"

        if key == ord("v"):
            mode = "VOLUME"

camera.release()
cv2.destroyAllWindows()
