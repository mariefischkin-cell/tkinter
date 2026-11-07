
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

class EdgeDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Edge Detection Studio")
        self.root.geometry("1200x800")
        self.root.configure(bg="#151821")

        self.original = None
        self.processed = None
        self.preview_refs = []

        title = tk.Label(
            root,
            text="ADVANCED EDGE DETECTION STUDIO",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#151821"
        )
        title.pack(pady=18)

        toolbar = tk.Frame(root, bg="#151821")
        toolbar.pack(pady=10)

        tk.Button(
            toolbar,
            text="Upload Image",
            command=self.upload_image,
            width=18
        ).pack(side="left", padx=10)

        tk.Button(
            toolbar,
            text="Save Image",
            command=self.save_image,
            width=18
        ).pack(side="left", padx=10)

        tk.Button(
            toolbar,
            text="Reset",
            command=self.reset,
            width=18
        ).pack(side="left", padx=10)

        controls = tk.Frame(root, bg="#151821")
        controls.pack(pady=15)

        self.method = tk.StringVar(value="Canny")

        methods = [
            "Original",
            "Canny",
            "Sobel",
            "Laplacian",
            "Gaussian Blur",
            "Median Blur",
            "Bilateral Filter"
        ]

        self.dropdown = ttk.Combobox(
            controls,
            textvariable=self.method,
            values=methods,
            state="readonly",
            width=25
        )
        self.dropdown.pack(pady=8)
        self.dropdown.bind(
            "<<ComboboxSelected>>",
            lambda event: self.process_image()
        )

        self.intensity = tk.Scale(
            controls,
            from_=1,
            to=100,
            orient="horizontal",
            label="Filter Intensity",
            length=350,
            bg="#151821",
            fg="white",
            highlightthickness=0,
            command=lambda value: self.process_image()
        )
        self.intensity.set(50)
        self.intensity.pack()

        self.threshold = tk.Scale(
            controls,
            from_=10,
            to=250,
            orient="horizontal",
            label="Edge Threshold",
            length=350,
            bg="#151821",
            fg="white",
            highlightthickness=0,
            command=lambda value: self.process_image()
        )
        self.threshold.set(100)
        self.threshold.pack()

        images = tk.Frame(root, bg="#151821")
        images.pack(fill="both", expand=True, padx=20, pady=15)

        left = tk.Frame(images, bg="#222633")
        left.pack(side="left", fill="both", expand=True, padx=8)

        right = tk.Frame(images, bg="#222633")
        right.pack(side="left", fill="both", expand=True, padx=8)

        tk.Label(
            left,
            text="ORIGINAL IMAGE",
            font=("Arial", 14, "bold"),
            bg="#222633",
            fg="white"
        ).pack(pady=10)

        tk.Label(
            right,
            text="PROCESSED IMAGE",
            font=("Arial", 14, "bold"),
            bg="#222633",
            fg="white"
        ).pack(pady=10)

        self.original_label = tk.Label(
            left, bg="#222633"
        )
        self.original_label.pack(expand=True)

        self.processed_label = tk.Label(
            right, bg="#222633"
        )
        self.processed_label.pack(expand=True)

        self.status = tk.Label(
            root,
            text="Upload an image to begin",
            bg="#151821",
            fg="#aab4c8",
            font=("Arial", 11)
        )
        self.status.pack(pady=10)

    def upload_image(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.bmp")
            ]
        )

        if not path:
            return

        self.original = cv2.imread(path)

        if self.original is None:
            messagebox.showerror(
                "Error",
                "Could not load the image."
            )
            return

        self.display_image(
            self.original,
            self.original_label
        )
        self.process_image()

    def process_image(self):
        if self.original is None:
            return

        image = self.original.copy()
        gray = cv2.cvtColor(
            image, cv2.COLOR_BGR2GRAY
        )

        method = self.method.get()
        strength = self.intensity.get()
        threshold = self.threshold.get()

        kernel = max(3, (strength // 5) * 2 + 1)
        kernel = min(kernel, 41)

        if method == "Canny":
            result = cv2.Canny(
                gray,
                threshold,
                min(threshold * 2, 500)
            )

        elif method == "Sobel":
            sx = cv2.Sobel(
                gray, cv2.CV_64F, 1, 0,
                ksize=3
            )
            sy = cv2.Sobel(
                gray, cv2.CV_64F, 0, 1,
                ksize=3
            )
            magnitude = cv2.magnitude(sx, sy)
            result = cv2.convertScaleAbs(
                magnitude,
                alpha=strength / 50
            )

        elif method == "Laplacian":
            lap = cv2.Laplacian(
                gray, cv2.CV_64F,
                ksize=3
            )
            result = cv2.convertScaleAbs(
                lap,
                alpha=strength / 50
            )

        elif method == "Gaussian Blur":
            result = cv2.GaussianBlur(
                image, (kernel, kernel), 0
            )

        elif method == "Median Blur":
            result = cv2.medianBlur(
                image, kernel
            )

        elif method == "Bilateral Filter":
            result = cv2.bilateralFilter(
                image,
                9,
                strength * 2,
                strength * 2
            )

        else:
            result = image

        self.processed = result

        self.display_image(
            result,
            self.processed_label
        )

        self.status.config(
            text=f"Applied: {method} | Intensity: {strength}"
        )

    def display_image(self, image, label):
        if len(image.shape) == 2:
            rgb = cv2.cvtColor(
                image, cv2.COLOR_GRAY2RGB
            )
        else:
            rgb = cv2.cvtColor(
                image, cv2.COLOR_BGR2RGB
            )

        pil = Image.fromarray(rgb)
        pil.thumbnail((520, 420))

        photo = ImageTk.PhotoImage(pil)
        label.configure(image=photo)
        label.image = photo

    def save_image(self):
        if self.processed is None:
            messagebox.showwarning(
                "Warning",
                "No processed image to save."
            )
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg")
            ]
        )

        if path:
            cv2.imwrite(path, self.processed)
            messagebox.showinfo(
                "Saved",
                "Image saved successfully!"
            )

    def reset(self):
        self.method.set("Original")
        self.intensity.set(50)
        self.threshold.set(100)
        self.process_image()


if __name__ == "__main__":
    root = tk.Tk()
    app = EdgeDetectionApp(root)
    root.mainloop()
