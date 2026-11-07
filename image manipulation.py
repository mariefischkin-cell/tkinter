
import cv2
from tkinter import Tk, filedialog

root = Tk()
root.withdraw()

path = filedialog.askopenfilename(
    title="Choose an image",
    filetypes=[("Images", "*.png *.jpg *.jpeg")]
)
root.destroy()

if not path:
    raise SystemExit("No image selected")

image = cv2.imread(path)

if image is None:
    raise SystemExit("Could not read image")

original = image.copy()

def show_image():
    cv2.imshow("Image Manipulation", image)

print("IMAGE MANIPULATION")
print("1 - Rotate 90 degrees")
print("2 - Rotate 180 degrees")
print("3 - Crop center")
print("4 - Increase brightness")
print("5 - Decrease brightness")
print("6 - Flip horizontally")
print("7 - Reset image")
print("S - Save image")
print("Q - Quit")

while True:
    show_image()
    key = cv2.waitKey(0) & 0xFF

    if key == ord("1"):
        image = cv2.rotate(
            image, cv2.ROTATE_90_CLOCKWISE
        )

    elif key == ord("2"):
        image = cv2.rotate(
            image, cv2.ROTATE_180
        )

    elif key == ord("3"):
        h, w = image.shape[:2]

        if h < 4 or w < 4:
            print("Image too small to crop")
            continue

        x1, x2 = w // 4, 3 * w // 4
        y1, y2 = h // 4, 3 * h // 4

        image = image[y1:y2, x1:x2].copy()

    elif key == ord("4"):
        image = cv2.convertScaleAbs(
            image, alpha=1, beta=40
        )

    elif key == ord("5"):
        image = cv2.subtract(
            image,
            40
        )

    elif key == ord("6"):
        image = cv2.flip(image, 1)

    elif key == ord("7"):
        image = original.copy()

    elif key == ord("s"):
        cv2.imwrite("manipulated_image.png", image)
        print("Image saved successfully")

    elif key == ord("q"):
        break

cv2.destroyAllWindows()
