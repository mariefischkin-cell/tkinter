
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class StationeryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stationery Order Management")
        self.root.geometry("900x750")
        self.root.configure(bg="#101827")

        self.currency = tk.StringVar(value="USD")
        self.quantities = {}

        self.products = {
            "Notebook": 4.50,
            "Pen": 1.20,
            "Pencil": 0.80,
            "Eraser": 0.60,
            "Ruler": 1.50,
            "Highlighter": 2.30,
            "Marker Set": 6.50,
            "Sketchbook": 8.00
        }

        self.exchange_rate = 83.0

        self.canvas = tk.Canvas(
            root,
            bg="#101827",
            highlightthickness=0,
            height=130
        )
        self.canvas.pack(fill="x")

        self.canvas.create_rectangle(
            0, 0, 1200, 130,
            fill="#1d3557",
            outline=""
        )

        self.canvas.create_text(
            450, 45,
            text="STATIONERY STORE",
            font=("Arial", 27, "bold"),
            fill="white"
        )

        self.canvas.create_text(
            450, 90,
            text="Smart Order Management System",
            font=("Arial", 13),
            fill="#bcd4ff"
        )

        main = ttk.Frame(root, padding=20)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main,
            text="Select Your Products",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        currency_frame = ttk.Frame(main)
        currency_frame.pack(pady=10)

        ttk.Label(
            currency_frame,
            text="Currency:"
        ).pack(side="left", padx=10)

        ttk.Radiobutton(
            currency_frame,
            text="USD",
            variable=self.currency,
            value="USD",
            command=self.update_total
        ).pack(side="left", padx=10)

        ttk.Radiobutton(
            currency_frame,
            text="INR",
            variable=self.currency,
            value="INR",
            command=self.update_total
        ).pack(side="left", padx=10)

        table = ttk.Frame(main)
        table.pack(pady=15)

        ttk.Label(
            table,
            text="Product",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, padx=20)

        ttk.Label(
            table,
            text="Price (USD)",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=1, padx=20)

        ttk.Label(
            table,
            text="Quantity",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=2, padx=20)

        for index, (product, price) in enumerate(
            self.products.items(), start=1
        ):
            ttk.Label(
                table,
                text=product
            ).grid(row=index, column=0, pady=7)

            ttk.Label(
                table,
                text=f"${price:.2f}"
            ).grid(row=index, column=1, pady=7)

            quantity = tk.StringVar(value="0")
            self.quantities[product] = quantity

            quantity.trace_add(
                "write",
                lambda *args: self.update_total()
            )

            ttk.Entry(
                table,
                textvariable=quantity,
                width=10
            ).grid(row=index, column=2, pady=7)

        self.total_label = ttk.Label(
            main,
            text="Total: $0.00",
            font=("Arial", 19, "bold")
        )
        self.total_label.pack(pady=15)

        buttons = ttk.Frame(main)
        buttons.pack(pady=10)

        ttk.Button(
            buttons,
            text="Calculate Total",
            command=self.update_total
        ).pack(side="left", padx=10)

        ttk.Button(
            buttons,
            text="Generate Receipt",
            command=self.generate_receipt
        ).pack(side="left", padx=10)

        ttk.Button(
            buttons,
            text="Clear Order",
            command=self.clear_order
        ).pack(side="left", padx=10)

        self.receipt = tk.Text(
            main,
            height=10,
            width=75,
            font=("Courier", 10)
        )
        self.receipt.pack(pady=15)

        self.update_total()

    def get_order(self):
        order = {}

        for product, quantity in self.quantities.items():
            value = quantity.get().strip()

            if not value.isdigit():
                raise ValueError(
                    f"Invalid quantity for {product}"
                )

            amount = int(value)

            if amount > 1000:
                raise ValueError(
                    f"Quantity too large for {product}"
                )

            if amount > 0:
                order[product] = amount

        return order

    def update_total(self):
        try:
            order = self.get_order()

            total = sum(
                self.products[product] * quantity
                for product, quantity in order.items()
            )

            converted = (
                total
                if self.currency.get() == "USD"
                else total * self.exchange_rate
            )

            symbol = "$" if self.currency.get() == "USD" else "₹"

            self.total_label.config(
                text=f"Total: {symbol}{converted:.2f}"
            )

        except ValueError:
            self.total_label.config(
                text="Total: Invalid quantity"
            )

    def generate_receipt(self):
        try:
            order = self.get_order()

        except ValueError as error:
            messagebox.showerror("Error", str(error))
            return

        if not order:
            messagebox.showwarning(
                "Empty Order",
                "Please select at least one product."
            )
            return

        currency = self.currency.get()
        rate = 1 if currency == "USD" else self.exchange_rate
        symbol = "$" if currency == "USD" else "₹"

        lines = [
            "STATIONERY STORE RECEIPT",
            "=" * 42,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "-" * 42
        ]

        total = 0

        for product, quantity in order.items():
            subtotal = self.products[product] * quantity * rate
            total += subtotal

            lines.append(
                f"{product} x{quantity}: {symbol}{subtotal:.2f}"
            )

        lines.extend([
            "-" * 42,
            f"TOTAL: {symbol}{total:.2f}",
            "=" * 42,
            "Thank you for your order!"
        ])

        receipt_text = "\n".join(lines)

        self.receipt.delete("1.0", tk.END)
        self.receipt.insert(tk.END, receipt_text)

        with open("stationery_receipt.txt", "w") as file:
            file.write(receipt_text)

        messagebox.showinfo(
            "Success",
            "Receipt generated and saved!"
        )

    def clear_order(self):
        for quantity in self.quantities.values():
            quantity.set("0")

        self.receipt.delete("1.0", tk.END)
        self.update_total()


if __name__ == "__main__":
    root = tk.Tk()
    app = StationeryApp(root)
    root.mainloop()
