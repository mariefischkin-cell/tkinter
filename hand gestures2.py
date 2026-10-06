import subprocess
import time

import cv2
import mediapipe as mp
import numpy as np


mp_hands = mp.solutions.hands
draw = mp.solutions.drawing_utils

THUMB = mp_hands.HandLandmark.THUMB_TIP
INDEX = mp_hands.HandLandmark.INDEX_FINGER_TIP

WINDOW = "Hand Gesture Control - Mac"


def set_volume(percent):
    result = subprocess.run(
        ["osascript", "-e", f"set volume output volume {percent}"],
        capture_output=True,
        text=True,
        timeout=2,
    )
    if result.returncode != 0:
        print("Lautstaerke-Fehler:", result.stderr.strip())
        return False
    return True


def draw_bar(img, percent, x, color, title):
    height = img.shape[0]
    top = 90
    bottom = max(top + 50, height - 90)
    width = 30

    fill_y = int(np.interp(percent, [0, 100], [bottom, top]))

    cv2.rectangle(img, (x, top), (x + width, bottom), color, 2)
    cv2.rectangle(img, (x, fill_y), (x + width, bottom), color, -1)

    cv2.putText(
        img, title, (x - 15, top - 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1
    )
    cv2.putText(
        img, f"{percent}%", (x - 10, bottom + 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2
    )


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print(
            "Kamera nicht erreichbar. Erlaube VS Code bzw. Terminal "
            "unter Systemeinstellungen > Datenschutz & Sicherheit > Kamera."
        )
        cap.release()
        return

    last_volume_update = 0.0
    last_volume = None
    volume_percent = None
    brightness_percent = None

    try:
        cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)

        with mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        ) as hands:

            while True:
                ok, img = cap.read()
                if not ok:
                    print("Kein Kamerabild erhalten.")
                    break

                # Gespiegeltes Bild: MediaPipe-Handlabels passen dazu.
                img = cv2.flip(img, 1)
                height, width = img.shape[:2]

                rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                rgb.flags.writeable = False
                results = hands.process(rgb)

                if results.multi_hand_landmarks and results.multi_handedness:
                    for hand, handedness in zip(
                        results.multi_hand_landmarks,
                        results.multi_handedness,
                    ):
                        label = handedness.classification[0].label

                        draw.draw_landmarks(
                            img, hand, mp_hands.HAND_CONNECTIONS
                        )

                        thumb = hand.landmark[THUMB]
                        index = hand.landmark[INDEX]

                        thumb_point = (
                            int(thumb.x * width),
                            int(thumb.y * height),
                        )
                        index_point = (
                            int(index.x * width),
                            int(index.y * height),
                        )

                        cv2.circle(img, thumb_point, 8, (255, 0, 0), -1)
                        cv2.circle(img, index_point, 8, (255, 0, 0), -1)
                        cv2.line(
                            img, thumb_point, index_point, (0, 255, 0), 3
                        )

                        # Abstand relativ zur Handgroesse:
                        # weniger abhaengig vom Abstand zur Kamera.
                        wrist = hand.landmark[
                            mp_hands.HandLandmark.WRIST
                        ]
                        middle_base = hand.landmark[
                            mp_hands.HandLandmark.MIDDLE_FINGER_MCP
                        ]

                        hand_size = np.hypot(
                            (middle_base.x - wrist.x) * width,
                            (middle_base.y - wrist.y) * height,
                        )
                        finger_distance = np.hypot(
                            index_point[0] - thumb_point[0],
                            index_point[1] - thumb_point[1],
                        )

                        if hand_size < 1:
                            continue

                        ratio = finger_distance / hand_size
                        percent = int(
                            np.interp(ratio, [0.15, 1.5], [0, 100])
                        )

                        if label == "Right":
                            volume_percent = percent
                            now = time.monotonic()

                            if (
                                now - last_volume_update >= 0.25
                                and (
                                    last_volume is None
                                    or abs(percent - last_volume) >= 2
                                )
                            ):
                                try:
                                    if set_volume(percent):
                                        last_volume = percent
                                except (
                                    OSError,
                                    subprocess.TimeoutExpired,
                                ) as error:
                                    print("Lautstaerke-Fehler:", error)

                                last_volume_update = time.monotonic()

                        elif label == "Left":
                            # Anzeige; steuert die Mac-Helligkeit noch nicht.
                            brightness_percent = percent

                if volume_percent is not None:
                    draw_bar(
                        img, volume_percent, 35,
                        (255, 150, 0), "Volume"
                    )

                if brightness_percent is not None:
                    draw_bar(
                        img, brightness_percent, width - 65,
                        (0, 255, 0), "Preview"
                    )

                cv2.putText(
                    img,
                    "Right: volume | Left: preview | Q: quit",
                    (10, height - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                )

                cv2.imshow(WINDOW, img)

                key = cv2.waitKey(1) & 0xFF
                if key in (27, ord("q")):
                    break

                if cv2.getWindowProperty(
                    WINDOW, cv2.WND_PROP_VISIBLE
                ) < 1:
                    break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()