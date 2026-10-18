
import time
import cv2
import mediapipe as mp
import pyautogui

pyautogui.FAILSAFE = True

hands_module = mp.solutions.hands
drawing = mp.solutions.drawing_utils

camera = cv2.VideoCapture(0)

last_scroll = 0
scroll_interval = 0.7

if not camera.isOpened():
    raise RuntimeError("Camera not available")

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

        gesture = "Show your hand"

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]

            drawing.draw_landmarks(
                frame,
                hand,
                hands_module.HAND_CONNECTIONS
            )

            points = hand.landmark

            extended = [
                points[tip].y < points[pip].y
                for tip, pip in [
                    (8, 6),
                    (12, 10),
                    (16, 14),
                    (20, 18)
                ]
            ]

            if all(extended):
                gesture = "OPEN PALM: SCROLL UP"

                if time.monotonic() - last_scroll > scroll_interval:
                    pyautogui.scroll(4)
                    last_scroll = time.monotonic()

            elif not any(extended):
                gesture = "CLOSED FIST: SCROLL DOWN"

                if time.monotonic() - last_scroll > scroll_interval:
                    pyautogui.scroll(-4)
                    last_scroll = time.monotonic()

            else:
                gesture = "No scroll gesture"

        cv2.putText(
            frame,
            gesture,
            (20, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow("Gesture Scrolling", frame)

        if cv2.waitKey(1) & 255 == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()
