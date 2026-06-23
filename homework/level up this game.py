import tkinter as tk

root = tk.Tk()
root.title("Background")
root.geometry("600x400")

# Background image
bg = tk.PhotoImage(file="/Users/der.coole.account/Desktop/Neuer Ordner 2/modern-city-scape-silhouette-simple-minimalist-blue-city-skyline-background-urban-cityscape-silhouettes-illustration-vector (1).jpg")

label = tk.Label(root, image=bg)
label.pack()

root.mainloop()