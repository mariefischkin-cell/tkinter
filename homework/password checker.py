import tkinter as tk

def check():
    p = e.get()
    if len(p) < 6:
        result.config(text="Weak")
    elif len(p) < 10:
        result.config(text="Medium")
    else:
        result.config(text="Strong")

root = tk.Tk()

e = tk.Entry(root, show="*")
e.pack()

tk.Button(root, text="Check", command=check).pack()

result = tk.Label(root, text="")
result.pack()

root.mainloop()
