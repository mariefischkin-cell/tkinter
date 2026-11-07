
import cv2
import numpy as np
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
    raise SystemExit("Could not open image")

height, width = image.shape[:2]

canvas = cv2.copyMakeBorder(
    image, 90, 30, 30, 30,
    cv2.BORDER_CONSTANT,
    value=(255, 255, 255)
)

start = (30, 55)
end = (width + 29, 55)

cv2.arrowedLine(
    canvas, start, end,
    (255, 0, 0), 3, tipLength=0.03
)

cv2.arrowedLine(
    canvas, end, start,
    (255, 0, 0), 3, tipLength=0.03
)

text = f"Width: {width} pixels"

cv2.putText(
    canvas, text,
    (30, 30),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7, (0, 0, 0), 2
)

cv2.line(
    canvas, (30, 65), (30, 90),
    (255, 0, 0), 2
)

cv2.line(
    canvas,
    (width + 29, 65),
    (width + 29, 90),
    (255, 0, 0), 2
)

print("Image width:", width)
print("Image height:", height)

cv2.imwrite("annotated_width.png", canvas)

cv2.imshow("Annotated Image Width", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
