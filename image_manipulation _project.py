import cv2
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from urllib.request import Request, urlopen

url = "https://static.vecteezy.com/system/resources/thumbnails/053/733/179/small/every-detail-of-a-sleek-modern-car-captured-in-close-up-photo.jpg"

request = Request(url, headers={"User-Agent": "Mozilla/5.0"})

with urlopen(request, timeout=30) as response:
    image_data = np.frombuffer(response.read(), dtype=np.uint8)

image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

if image is None:
    raise ValueError("Could not decode the downloaded image.")

grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

height, width = image.shape[:2]
cropped = image[
    height // 4:max(height // 4 + 1, 3 * height // 4),
    width // 4:max(width // 4 + 1, 3 * width // 4)
]

center = (width / 2, height / 2)
rotation_matrix = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(image, rotation_matrix, (width, height))

brightened = cv2.convertScaleAbs(image, alpha=1.0, beta=50)

output_folder = Path(__file__).resolve().parent

results = {
    "grayscale.png": grayscale,
    "cropped.png": cropped,
    "rotated.png": rotated,
    "brightened.png": brightened
}

for filename, result in results.items():
    output_path = output_folder / filename
    if not cv2.imwrite(str(output_path), result):
        raise OSError(f"Could not save image: {output_path}")

fig, axes = plt.subplots(2, 3, figsize=(12, 8))

images = [image, grayscale, cropped, rotated, brightened]
titles = [
    "Original Image",
    "Grayscale Image",
    "Cropped Image",
    "Rotated Image (45 Degrees)",
    "Brightened Image"
]

for ax, result, title in zip(axes.flat, images, titles):
    if result.ndim == 2:
        ax.imshow(result, cmap="gray", vmin=0, vmax=255)
    else:
        ax.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    ax.set_title(title)
    ax.axis("off")

axes.flat[-1].axis("off")
plt.tight_layout()

print(f"All images saved to: {output_folder}")

plt.show()