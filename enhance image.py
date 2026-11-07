
import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not found")
    exit()

filter_mode = 0

filters = [
    "Normal",
    "Grayscale",
    "Sepia",
    "Negative",
    "Blur",
    "Canny Edges",
    "Sobel Edges",
    "Laplacian Edges"
]

while True:
    success, frame = cap.read()

    if not success:
        print("Failed to read camera")
        break

    frame = cv2.flip(frame, 1)
    output = frame.copy()

    if filter_mode == 1:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        output = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    elif filter_mode == 2:
        matrix = np.array([
            [0.131, 0.534, 0.272],
            [0.168, 0.686, 0.349],
            [0.189, 0.769, 0.393]
        ])
        output = cv2.transform(frame, matrix)
        output = np.clip(output, 0, 255).astype(np.uint8)

    elif filter_mode == 3:
        output = cv2.bitwise_not(frame)

    elif filter_mode == 4:
        output = cv2.GaussianBlur(frame, (25, 25), 0)

    elif filter_mode == 5:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        output = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    elif filter_mode == 6:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

        magnitude = cv2.magnitude(sx, sy)
        edges = cv2.convertScaleAbs(magnitude)
        output = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    elif filter_mode == 7:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Laplacian(gray, cv2.CV_64F)
        edges = cv2.convertScaleAbs(edges)
        output = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    cv2.rectangle(
        output,
        (0, 0),
        (output.shape[1], 75),
        (20, 20, 20),
        -1
    )

    cv2.putText(
        output,
        "Filter: " + filters[filter_mode],
        (15, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.putText(
        output,
        "0-7: Filters | S: Save | Q: Quit",
        (15, 62),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1
    )

    cv2.imshow("Real-Time Image Processing", output)

    key = cv2.waitKey(1) & 0xFF

    if ord("0") <= key <= ord("7"):
        filter_mode = key - ord("0")

    elif key == ord("s"):
        filename = f"photo_{int(time.time() * 1000)}.png"
        cv2.imwrite(filename, output)
        print("Image saved:", filename)

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
