
import cv2
from tkinter import Tk, filedialog

root = Tk()
root.withdraw()

path = filedialog.askopenfilename(
    title="Select an image",
    filetypes=[("Images", "*.png *.jpg *.jpeg")]
)
root.destroy()

if not path:
    raise SystemExit("No image selected")

image = cv2.imread(path)

if image is None:
    raise SystemExit("Unable to load image")

sizes = {
    "Small": (320, 240),
    "Medium": (640, 480),
    "Large": (1280, 720)
}

print("IMAGE RESIZER")
print("Original size:", image.shape[1], "x", image.shape[0])

for name, size in sizes.items():
    resized = cv2.resize(
        image,
        size,
        interpolation=cv2.INTER_AREA
    )

    filename = f"resized_{name.lower()}.png"

    cv2.imwrite(filename, resized)

    print(f"{name}: {size[0]} x {size[1]}")
    print("Saved:", filename)

    cv2.imshow(f"{name} Image", resized)

print("Press any key to close all windows")

cv2.waitKey(0)
cv2.destroyAllWindows()
