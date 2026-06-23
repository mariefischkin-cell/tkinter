import tkinter as tk

def calc():
    try:
        p = float(e1.get())
        r = float(e2.get())
        t = float(e3.get())
        si = (p * r * t) / 100
        result.config(text=f"SI: {si}")
    except:
        result.config(text="Error")

root = tk.Tk()

tk.Label(root, text="Principal").pack()
e1 = tk.Entry(root); e1.pack()

tk.Label(root, text="Rate (%)").pack()
e2 = tk.Entry(root); e2.pack()

tk.Label(root, text="Time").pack()
e3 = tk.Entry(root); e3.pack()

tk.Button(root, text="Calculate", command=calc).pack()

result = tk.Label(root, text="")
result.pack()

root.mainloop()