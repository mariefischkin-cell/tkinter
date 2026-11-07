
import cv2
import numpy as np
from datetime import datetime

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Camera not available")
    raise SystemExit

window = "Real-Time Color Filter Application"

cv2.namedWindow(window, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window, 1000, 750)

def nothing(value):
    pass

cv2.createTrackbar("Red", window, 100, 200, nothing)
cv2.createTrackbar("Green", window, 100, 200, nothing)
cv2.createTrackbar("Blue", window, 100, 200, nothing)
cv2.createTrackbar("Brightness", window, 100, 200, nothing)
cv2.createTrackbar("Contrast", window, 100, 200, nothing)
cv2.createTrackbar("Intensity", window, 100, 100, nothing)

filters = [
    "Normal",
    "Grayscale",
    "Sepia",
    "Negative",
    "Blur",
    "Cartoon",
    "Edges",
    "Warm"
]

current_filter = 0

def apply_filter(frame, filter_name):
    if filter_name == "Grayscale":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    if filter_name == "Sepia":
        matrix = np.array([
            [0.131, 0.534, 0.272],
            [0.168, 0.686, 0.349],
            [0.189, 0.769, 0.393]
        ])
        return cv2.transform(frame, matrix).clip(0, 255).astype(np.uint8)

    if filter_name == "Negative":
        return cv2.bitwise_not(frame)

    if filter_name == "Blur":
        return cv2.GaussianBlur(frame, (21, 21), 0)

    if filter_name == "Cartoon":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 9, 9
        )
        smooth = cv2.bilateralFilter(frame, 9, 150, 150)
        return cv2.bitwise_and(smooth, smooth, mask=edges)

    if filter_name == "Edges":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 80, 160)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    if filter_name == "Warm":
        warm = frame.astype(np.float32)
        warm[:, :, 2] *= 1.25
        warm[:, :, 0] *= 0.80
        return np.clip(warm, 0, 255).astype(np.uint8)

    return frame.copy()

print("Color Filter Application Started")
print("1-8: Select filter")
print("N: Next filter")
print("S: Save photo")
print("R: Reset sliders")
print("Q: Quit")

while True:
    success, frame = camera.read()

    if not success:
        print("Camera frame unavailable")
        break

    frame = cv2.flip(frame, 1)

    red = cv2.getTrackbarPos("Red", window) / 100
    green = cv2.getTrackbarPos("Green", window) / 100
    blue = cv2.getTrackbarPos("Blue", window) / 100
    brightness = cv2.getTrackbarPos("Brightness", window) - 100
    contrast = cv2.getTrackbarPos("Contrast", window) / 100
    intensity = cv2.getTrackbarPos("Intensity", window) / 100

    adjusted = frame.astype(np.float32)

    adjusted[:, :, 0] *= blue
    adjusted[:, :, 1] *= green
    adjusted[:, :, 2] *= red

    adjusted = adjusted * contrast + brightness
    adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)

    selected = filters[current_filter]
    filtered = apply_filter(adjusted, selected)

    output = cv2.addWeighted(
        filtered, intensity,
        adjusted, 1 - intensity, 0
    )

    photo = output.copy()

    cv2.rectangle(output, (0, 0), (650, 85), (25, 25, 25), -1)

    cv2.putText(
        output,
        "FILTER: " + selected.upper(),
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.85,
        (255, 255, 255),
        2
    )

    cv2.putText(
        output,
        "1-8 Filters | N Next | S Save | R Reset | Q Quit",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 255, 255),
        1
    )

    cv2.imshow(window, output)

    key = cv2.waitKey(1) & 0xFF

    if ord("1") <= key <= ord("8"):
        current_filter = key - ord("1")

    elif key == ord("n"):
        current_filter = (current_filter + 1) % len(filters)

    elif key == ord("s"):
        filename = "filtered_" + datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        ) + ".png"
        cv2.imwrite(filename, photo)
        print("Photo saved:", filename)

    elif key == ord("r"):
        for name in ["Red", "Green", "Blue",
                     "Brightness", "Contrast", "Intensity"]:
            cv2.setTrackbarPos(name, window, 100)

    elif key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
