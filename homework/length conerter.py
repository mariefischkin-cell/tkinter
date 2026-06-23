import tkinter as tk

def convert():
    try:
        cm = float(e.get()) * 2.54
        result.config(text=f"{cm} cm")
    except:
        result.config(text="Error")

root = tk.Tk()

e = tk.Entry(root)
e.pack()

tk.Button(root, text="Convert", command=convert).pack()

result = tk.Label(root, text="")
result.pack()

root.mainloop()