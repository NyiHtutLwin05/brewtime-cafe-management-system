# order_screen.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from data import get_categories, get_items_by_category, get_item_base_price, get_size_modifiers


class OrderScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg='white')
        self.current_category = None
        self.current_drink = None
        self.order_items = []

        # Price configuration (in cents)
        self.size_prices = {
            "Small": 0,
            "Medium": 50,
            "Large": 100
        }

        self.addon_prices = {
            "Milk foam": 300,
            "Bubble": 300,
            "Extra shot": 500,
            "Soy Milk": 400,
            "Almond Milk": 400
        }

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()

        # Configure styles
        style.configure(
            'Coffee.TButton',
            font=('Arial', 10),
            padding=5,
            foreground='#6F4E37',
            background='#D2B48C',
            bordercolor='#6F4E37'
        )
        style.map(
            'Coffee.TButton',
            background=[('active', '#C4A484')],
            relief=[('pressed', tk.SUNKEN)]
        )

        style.configure(
            'Coffee.TRadiobutton',
            background='white',
            foreground='#6F4E37',
            font=('Arial', 10)
        )

        style.configure(
            'Coffee.TCheckbutton',
            background='white',
            foreground='#6F4E37',
            font=('Arial', 10)
        )

        style.configure(
            'Coffee.TCombobox',
            fieldbackground='white',
            foreground='#6F4E37'
        )

        style.configure(
            'Coffee.TFrame',
            background='white'
        )

        # Back button
        back_button = ttk.Button(
            self,
            text="Back",
            command=self.go_back,
            style='Coffee.TButton'
        )
        back_button.pack(anchor="nw", padx=10, pady=10)

        # Title label
        title_label = tk.Label(
            self,
            text="Please place your order",
            font=("Arial", 16, "bold"),
            pady=10,
            bg='white',
            fg='#6F4E37'
        )
        title_label.pack()

        # Main container frame
        main_frame = ttk.Frame(self, style='Coffee.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left side - Order selection
        selection_frame = ttk.Frame(main_frame, style='Coffee.TFrame')
        selection_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Category selection
        category_label = tk.Label(
            selection_frame,
            text="Select Category",
            font=("Arial", 12, "bold"),
            anchor="w",
            bg='white',
            fg='#6F4E37'
        )
        category_label.pack(fill=tk.X, pady=(0, 5))

        self.category_var = tk.StringVar()
        categories = get_categories()

        for category in categories:
            rb = ttk.Radiobutton(
                selection_frame,
                text=category,
                variable=self.category_var,
                value=category,
                command=self.update_drink_options,
                style='Coffee.TRadiobutton'
            )
            rb.pack(anchor="w", padx=10, pady=2)

        # Drink type selection
        drink_frame = ttk.Frame(selection_frame, style='Coffee.TFrame')
        drink_frame.pack(fill=tk.X, pady=(10, 5))

        drink_label = tk.Label(
            drink_frame,
            text="Select Drink Type",
            font=("Arial", 12, "bold"),
            anchor="w",
            bg='white',
            fg='#6F4E37'
        )
        drink_label.pack(fill=tk.X)

        self.drink_var = tk.StringVar()
        self.drink_options = ttk.Combobox(
            drink_frame,
            textvariable=self.drink_var,
            state="readonly",
            style='Coffee.TCombobox'
        )
        self.drink_options.pack(fill=tk.X, pady=5)

        # Size selection
        size_frame = ttk.Frame(selection_frame, style='Coffee.TFrame')
        size_frame.pack(fill=tk.X, pady=(10, 5))

        size_label = tk.Label(
            size_frame,
            text="Size",
            font=("Arial", 12, "bold"),
            anchor="w",
            bg='white',
            fg='#6F4E37'
        )
        size_label.pack(fill=tk.X)

        self.size_var = tk.StringVar()
        sizes = ["Small", "Medium", "Large"]

        for size in sizes:
            rb = ttk.Radiobutton(
                size_frame,
                text=size,
                variable=self.size_var,
                value=size,
                style='Coffee.TRadiobutton'
            )
            rb.pack(anchor="w", padx=10, pady=2)

        # Add-ons selection
        addons_frame = ttk.Frame(selection_frame, style='Coffee.TFrame')
        addons_frame.pack(fill=tk.X, pady=(10, 5))

        addons_label = tk.Label(
            addons_frame,
            text="Add-ons: (Optional)",
            font=("Arial", 12, "bold"),
            anchor="w",
            bg='white',
            fg='#6F4E37'
        )
        addons_label.pack(fill=tk.X)

        self.addon_vars = {}
        addons = ["Milk foam", "Bubble",
                  "Extra shot", "Soy Milk", "Almond Milk"]

        for addon in addons:
            self.addon_vars[addon] = tk.BooleanVar()
            cb = ttk.Checkbutton(
                addons_frame,
                text=f"{addon} (+${self.addon_prices[addon]/100:.2f})",
                variable=self.addon_vars[addon],
                style='Coffee.TCheckbutton'
            )
            cb.pack(anchor="w", padx=10, pady=2)

        # Quantity selection
        qty_frame = ttk.Frame(selection_frame, style='Coffee.TFrame')
        qty_frame.pack(fill=tk.X, pady=(10, 5))

        qty_label = tk.Label(
            qty_frame,
            text="Amount:",
            font=("Arial", 12, "bold"),
            anchor="w",
            bg='white',
            fg='#6F4E37'
        )
        qty_label.pack(side=tk.LEFT)

        self.qty_var = tk.IntVar(value=1)
        qty_spin = ttk.Spinbox(
            qty_frame,
            from_=1,
            to=10,
            textvariable=self.qty_var,
            width=5
        )
        qty_spin.pack(side=tk.LEFT, padx=10)

        # Add Order button
        add_button = ttk.Button(
            selection_frame,
            text="Add Order",
            command=self.add_to_order,
            style='Coffee.TButton'
        )
        add_button.pack(pady=10)

        # Right side - Order summary
        summary_frame = ttk.Frame(
            main_frame,
            style='Coffee.TFrame',
            relief=tk.GROOVE,
            borderwidth=2
        )
        summary_frame.pack(side=tk.RIGHT, fill=tk.BOTH,
                           expand=True, padx=(10, 0))

        summary_label = tk.Label(
            summary_frame,
            text="Order Summary",
            font=("Arial", 12, "bold"),
            pady=5,
            bg='white',
            fg='#6F4E37'
        )
        summary_label.pack()

        # Order list
        self.order_listbox = tk.Listbox(
            summary_frame,
            height=15,
            font=("Arial", 10)
        )
        self.order_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Total price
        total_frame = ttk.Frame(summary_frame, style='Coffee.TFrame')
        total_frame.pack(fill=tk.X, padx=5, pady=5)

        self.total_label = tk.Label(
            total_frame,
            text="Total: $0.00",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='#6F4E37'
        )
        self.total_label.pack(side=tk.RIGHT)

        # Checkout button
        checkout_button = ttk.Button(
            summary_frame,
            text="Checkout",
            command=self.checkout,
            style='Coffee.TButton'
        )
        checkout_button.pack(pady=5)

        # Remove item button
        remove_button = ttk.Button(
            summary_frame,
            text="Select & Remove Item",
            command=self.remove_item,
            style='Coffee.TButton'
        )
        remove_button.pack(pady=5)

        # Bind drink selection
        self.drink_options.bind('<<ComboboxSelected>>', self.on_drink_select)

    def update_drink_options(self):
        category = self.category_var.get()
        if category:
            drinks = get_items_by_category(category)
            self.drink_options['values'] = drinks
            self.drink_var.set('')

    def voucher_back(self):
        # Keep the order and go back to order screen
        self.voucher_frame.destroy()
        self.pack(fill=tk.BOTH, expand=True)

    def on_drink_select(self, event):
        category = self.category_var.get()
        drink = self.drink_var.get()
        if category and drink:
            self.current_drink = drink
            self.current_category = category

    def add_to_order(self):
        # Validate selections
        if not self.category_var.get():
            messagebox.showerror("Error", "Please select a category")
            return

        if not self.drink_var.get():
            messagebox.showerror("Error", "Please select a drink type")
            return

        if not self.size_var.get():
            messagebox.showerror("Error", "Please select a size")
            return

        # Calculate price
        base_price = get_item_base_price(
            self.category_var.get(),
            self.drink_var.get()
        )
        # Convert cents to dollars
        size_modifier = self.size_prices[self.size_var.get()] / 100
        base_price += size_modifier

        if not base_price:
            messagebox.showerror("Error", "Price not found for selected item")
            return

        addons_price = sum(
            self.addon_prices[addon] / 100
            for addon, var in self.addon_vars.items()
            if var.get()
        )

        total_price = base_price + addons_price
        quantity = self.qty_var.get()

        # Create order item
        order_item = {
            "category": self.category_var.get(),
            "drink": self.drink_var.get(),
            "size": self.size_var.get(),
            "addons": [addon for addon,
                       var in self.addon_vars.items() if var.get()],
            "price": total_price,
            "quantity": quantity
        }

        # Add to order list
        self.order_items.append(order_item)

        # Update order summary
        self.update_order_summary()

        # Reset selections
        self.reset_selections()

    def update_order_summary(self):
        self.order_listbox.delete(0, tk.END)
        total = 0

        for i, item in enumerate(self.order_items):
            item_text = f"{item['quantity']}x {item['drink']} ({item['size']})"
            if item['addons']:
                item_text += f" + {', '.join(item['addons'])}"
            item_text += f" - ${item['price'] * item['quantity']:.2f}"

            self.order_listbox.insert(tk.END, item_text)
            total += item['price'] * item['quantity']

        self.total_label.config(text=f"Total: ${total:.2f}")

    def remove_item(self):
        selected = self.order_listbox.curselection()
        if selected:
            index = selected[0]
            self.order_items.pop(index)
            self.update_order_summary()

    def reset_selections(self):
        # Reset all selections except category
        self.drink_var.set('')
        self.size_var.set('')
        for var in self.addon_vars.values():
            var.set(False)
        self.qty_var.set(1)

    def checkout(self):
        if not self.order_items:
            messagebox.showerror("Error", "Your order is empty")
            return

        total = sum(item['price'] * item['quantity']
                    for item in self.order_items)

        # Generate order summary
        order_summary = "Order Summary:\n\n"
        for item in self.order_items:
            order_summary += f"{item['quantity']}x {item['drink']} ({item['size']})"
            if item['addons']:
                order_summary += f" + {', '.join(item['addons'])}"
            order_summary += f" - ${item['price'] * item['quantity']:.2f}\n"

        order_summary += f"\nTotal: ${total:.2f}"

        # Show confirmation
        result = messagebox.askyesno(
            "Confirm Order",
            f"{order_summary}\n\nConfirm order?"
        )

        if result:
            self.show_voucher()

    def show_voucher(self):
        # Hide the order screen
        self.pack_forget()

        # Create voucher screen
        self.voucher_frame = tk.Frame(self.parent, bg='white')
        self.voucher_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(
            self.voucher_frame,
            text="Order Receipt",
            font=("Arial", 16, "bold"),
            pady=10,
            bg='white',
            fg='#6F4E37'
        )
        title_label.pack()

        # Receipt content in a scrollable text widget
        receipt_text = scrolledtext.ScrolledText(
            self.voucher_frame,
            wrap=tk.WORD,
            width=50,
            height=20,
            font=("Courier New", 10)
        )
        receipt_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Insert receipt content
        receipt = self.generate_receipt()
        receipt_text.insert(tk.INSERT, receipt)
        receipt_text.config(state=tk.DISABLED)  # Make it read-only

        # Button frame
        button_frame = tk.Frame(self.voucher_frame, bg='white')
        button_frame.pack(pady=10)

        # OK button - clears order and goes back to order screen
        ok_button = ttk.Button(
            button_frame,
            text="OK",
            command=self.voucher_ok,
            style='Coffee.TButton',
            width=10
        )
        ok_button.pack(side=tk.LEFT, padx=10)

        # Back button - keeps order and goes back to order screen
        back_button = ttk.Button(
            button_frame,
            text="Back",
            command=self.voucher_back,
            style='Coffee.TButton',
            width=10
        )
        back_button.pack(side=tk.LEFT, padx=10)

    def generate_receipt(self):
        receipt = "BrewTime Cafe\n"
        receipt += "Thank you for your order!\n"
        receipt += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        receipt += "-" * 40 + "\n"

        total = 0

        for item in self.order_items:
            # Get base price for the drink
            base_price = get_item_base_price(item['category'], item['drink'])
        # Add size modifier
            size_modifier = self.size_prices[item['size']] / 100
            base_price += size_modifier

            # Calculate add-ons price
            addons_price = sum(
                self.addon_prices[addon] / 100
                for addon in item['addons']
            )

        # Item total
            item_total = (base_price + addons_price) * item['quantity']
            total += item_total

        # Format the item line
            receipt += f"{item['quantity']}x {item['drink']} ({item['size']})"

        # Add base price
            receipt += f" ${base_price:.2f}"

            # Add add-ons with their prices if any
            if item['addons']:
                for addon in item['addons']:
                    addon_price = self.addon_prices[addon] / 100
                    receipt += f"\n  + {addon} (+${addon_price:.2f})"

        # Add item subtotal
        receipt += f"\n  Subtotal: ${item_total:.2f}\n\n"

        receipt += "-" * 40 + "\n"
        receipt += f"Total: ${total:.2f}\n"
        receipt += "-" * 40 + "\n"
        receipt += "Enjoy your drinks!"

        return receipt

    def voucher_ok(self):
        self.order_items.clear()
        self.voucher_frame.destroy()
        self.pack(fill=tk.BOTH, expand=True)
        self.update_order_summary()

    def voucher_back(self):
        self.voucher_frame.destroy()
        self.pack(fill=tk.BOTH, expand=True)

    def go_back(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        from welcome_screen import WelcomeScreen
        welcome_screen = WelcomeScreen(self.parent)
        welcome_screen.pack(fill=tk.BOTH, expand=True)
