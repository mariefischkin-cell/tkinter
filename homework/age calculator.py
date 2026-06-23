import tkinter as tk
from datetime import datetime

def calc():
    try:
        y = int(e1.get())
        m = int(e2.get())
        d = int(e3.get())
        age = datetime.now().year - y
        result.config(text=f"Age: {age}")
    except:
        result.config(text="Error")

root = tk.Tk()

tk.Label(root, text="Year").pack()
e1 = tk.Entry(root); e1.pack()

tk.Label(root, text="Month").pack()
e2 = tk.Entry(root); e2.pack()

tk.Label(root, text="Day").pack()
e3 = tk.Entry(root); e3.pack()

tk.Button(root, text="Calculate", command=calc).pack()

result = tk.Label(root, text="")
result.pack()

root.mainloop()