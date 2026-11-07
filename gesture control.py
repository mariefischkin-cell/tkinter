
import cv2
import mediapipe as mp
import numpy as np
import time
import os

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

drawing = mp.solutions.drawing_utils

filters = ["Normal", "Grayscale", "Sepia", "Negative", "Blur"]
filter_index = 0
last_action = 0

os.makedirs("photos", exist_ok=True)

def apply_filter(frame, name):
    if name == "Grayscale":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    if name == "Sepia":
        matrix = np.array([
            [0.131, 0.534, 0.272],
            [0.168, 0.686, 0.349],
            [0.189, 0.769, 0.393]
        ])
        return cv2.transform(frame, matrix).clip(0, 255).astype(np.uint8)

    if name == "Negative":
        return cv2.bitwise_not(frame)

    if name == "Blur":
        return cv2.GaussianBlur(frame, (25, 25), 0)

    return frame.copy()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Camera not available")

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    current_time = time.time()
    action = ""

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            points = hand.landmark

            thumb = points[4]
            index = points[8]
            middle = points[12]

            index_distance = (
                (thumb.x - index.x) ** 2 +
                (thumb.y - index.y) ** 2
            ) ** 0.5

            middle_distance = (
                (thumb.x - middle.x) ** 2 +
                (thumb.y - middle.y) ** 2
            ) ** 0.5

            if current_time - last_action > 1.2:
                if index_distance < 0.05 and index_distance < middle_distance:
                    action = "photo"
                    last_action = current_time

                elif middle_distance < 0.05:
                    filter_index = (filter_index + 1) % len(filters)
                    last_action = current_time

    output = apply_filter(frame, filters[filter_index])

    if action == "photo":
        filename = f"photos/photo_{int(time.time() * 1000)}.png"
        cv2.imwrite(filename, output)
        print("Photo saved:", filename)

    cv2.putText(
        output,
        "Filter: " + filters[filter_index],
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Gesture Photo App", output)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()
