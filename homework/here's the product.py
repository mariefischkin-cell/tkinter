import tkinter as tk

def calc():
    try:
        result.config(text=float(e1.get()) * float(e2.get()))
    except:
        result.config(text="Error")

root = tk.Tk()

e1 = tk.Entry(root)
e1.pack()
e2 = tk.Entry(root)
e2.pack()

tk.Button(root, text="Multiply", command=calc).pack()

result = tk.Label(root, text="")
result.pack()

root.mainloop()