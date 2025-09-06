# admin_crud.py
import tkinter as tk
from tkinter import ttk, messagebox
from data import add_menu_item, update_menu_item, delete_menu_item, get_categories


class AddItemScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg='white')
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure(
            'Coffee.TButton',
            font=('Arial', 12),
            padding=10,
            foreground='#6F4E37',
            background='#D2B48C'
        )
        style.map(
            'Coffee.TButton',
            background=[('active', '#C4A484')]
        )

        # Back button
        back_button = ttk.Button(
            self,
            text="Back",
            command=self.go_back,
            style='Coffee.TButton'
        )
        back_button.pack(anchor="nw", padx=10, pady=10)

        # Title
        title_label = tk.Label(
            self,
            text="Add New Menu Item",
            font=("Arial", 20, "bold"),
            pady=20,
            bg='white',
            fg='#6F4E37'
        )
        title_label.pack()

        # Form frame
        form_frame = tk.Frame(self, bg='white')
        form_frame.pack(expand=True, padx=50)

        # Category
        tk.Label(
            form_frame,
            text="Category:",
            font=("Arial", 12),
            bg='white',
            fg='#6F4E37'
        ).grid(row=0, column=0, sticky="w", pady=5)

        self.category_var = tk.StringVar()
        categories = get_categories()
        category_menu = ttk.Combobox(
            form_frame,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            font=("Arial", 12)
        )
        category_menu.grid(row=0, column=1, sticky="ew", pady=5)

        # Item Name
        tk.Label(
            form_frame,
            text="Item Name:",
            font=("Arial", 12),
            bg='white',
            fg='#6F4E37'
        ).grid(row=1, column=0, sticky="w", pady=5)

        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(
            form_frame,
            textvariable=self.name_var,
            font=("Arial", 12)
        )
        name_entry.grid(row=1, column=1, sticky="ew", pady=5)

        # Base Price
        tk.Label(
            form_frame,
            text="Base Price (Small):",
            font=("Arial", 12),
            bg='white',
            fg='#6F4E37'
        ).grid(row=2, column=0, sticky="w", pady=5)

        self.price_var = tk.StringVar()
        price_entry = ttk.Entry(
            form_frame,
            textvariable=self.price_var,
            font=("Arial", 12)
        )
        price_entry.grid(row=2, column=1, sticky="ew", pady=5)

        # Price info
        info_label = tk.Label(
            form_frame,
            text="Note: Medium (+$0.50) and Large (+$1.00) prices will be calculated automatically",
            font=("Arial", 10, "italic"),
            bg='white',
            fg='#6F4E37',
            wraplength=400
        )
        info_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=5)

        # Submit button
        submit_button = ttk.Button(
            form_frame,
            text="Add Item",
            command=self.add_item,
            style='Coffee.TButton'
        )
        submit_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)

    def add_item(self):
        # Validate inputs
        if not all([self.category_var.get(), self.name_var.get(), self.price_var.get()]):
            messagebox.showerror("Error", "Please fill all required fields")
            return

        # Validate price
        try:
            base_price = float(self.price_var.get())
            if base_price <= 0:
                raise ValueError("Price must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid price")
            return

        # Add to data
        success = add_menu_item(
            self.category_var.get(),
            self.name_var.get(),
            base_price
        )

        if success:
            from data import debug_menu_data
            debug_menu_data()
            messagebox.showinfo("Success", "Item added successfully!")
            self.go_back()
        else:
            messagebox.showerror("Error", "Failed to add item")

    def go_back(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        from admin_dashboard import AdminDashboard
        admin_dashboard = AdminDashboard(self.parent)
        admin_dashboard.pack(fill=tk.BOTH, expand=True)


class UpdateItemScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg='white')
        self.selected_item = None
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure(
            'Coffee.TButton',
            font=('Arial', 12),
            padding=10,
            foreground='#6F4E37',
            background='#D2B48C'
        )
        style.map(
            'Coffee.TButton',
            background=[('active', '#C4A484')]
        )

        # Back button
        back_button = ttk.Button(
            self,
            text="Back",
            command=self.go_back,
            style='Coffee.TButton'
        )
        back_button.pack(anchor="nw", padx=10, pady=10)

        # Title
        title_label = tk.Label(
            self,
            text="Update Menu Item",
            font=("Arial", 20, "bold"),
            pady=20,
            bg='white',
            fg='#6F4E37'
        )
        title_label.pack()

        # Selection frame
        selection_frame = tk.Frame(self, bg='white')
        selection_frame.pack(expand=True, padx=50, pady=10)

        # Category selection
        tk.Label(
            selection_frame,
            text="Select Category:",
            font=("Arial", 12),
            bg='white',
            fg='#6F4E37'
        ).grid(row=0, column=0, sticky="w", pady=5)

        self.category_var = tk.StringVar()
        categories = get_categories()
        category_menu = ttk.Combobox(
            selection_frame,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            font=("Arial", 12)
        )
        category_menu.grid(row=0, column=1, sticky="ew", pady=5)
        category_menu.bind('<<ComboboxSelected>>', self.update_item_list)

        # Item selection
        tk.Label(
            selection_frame,
            text="Select Item:",
            font=("Arial", 12),
            bg='white',
            fg='#6F4E37'
        ).grid(row=1, column=0, sticky="w", pady=5)

        self.item_var = tk.StringVar()
        self.item_menu = ttk.Combobox(
            selection_frame,
            textvariable=self.item_var,
            state="readonly",
            font=("Arial", 12)
        )
        self.item_menu.grid(row=1, column=1, sticky="ew", pady=5)
        self.item_menu.bind('<<ComboboxSelected>>', self.load_item_details)

        # Form frame (initially hidden)
        self.form_frame = tk.Frame(self, bg='white')

        # Base Price
        tk.Label(
            self.form_frame,
            text="Base Price (Small):",
            font=("Arial", 12),
            bg='white',
            fg='#6F4E37'
        ).grid(row=0, column=0, sticky="w", pady=5)

        self.price_var = tk.StringVar()
        price_entry = ttk.Entry(
            self.form_frame,
            textvariable=self.price_var,
            font=("Arial", 12)
        )
        price_entry.grid(row=0, column=1, sticky="ew", pady=5)

        # Price info
        info_label = tk.Label(
            self.form_frame,
            text="Note: Medium (+$0.50) and Large (+$1.00) prices will be calculated automatically",
            font=("Arial", 10, "italic"),
            bg='white',
            fg='#6F4E37',
            wraplength=400
        )
        info_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)

        # Update button
        self.update_button = ttk.Button(
            self.form_frame,
            text="Update Item",
            command=self.update_item,
            style='Coffee.TButton'
        )
        self.update_button.grid(row=2, column=0, columnspan=2, pady=20)

        # Configure grid weights
        selection_frame.columnconfigure(1, weight=1)
        self.form_frame.columnconfigure(1, weight=1)

    def update_item_list(self, event=None):
        from data import get_items_by_category
        category = self.category_var.get()
        if category:
            items = get_items_by_category(category)
            self.item_menu['values'] = items
            self.item_var.set('')
            self.form_frame.pack_forget()  # Hide form until item is selected

    def load_item_details(self, event=None):
        from data import get_item_base_price
        category = self.category_var.get()
        item_name = self.item_var.get()

        if category and item_name:
            base_price = get_item_base_price(category, item_name)
            self.selected_item = (category, item_name)

            # Populate price field
            self.price_var.set(str(base_price))

            # Show the form
            self.form_frame.pack(expand=True, padx=50, pady=10)

    def update_item(self):
        if not self.selected_item:
            messagebox.showerror("Error", "Please select an item to update")
            return

        category, item_name = self.selected_item

        # Validate price
        try:
            base_price = float(self.price_var.get())
            if base_price <= 0:
                raise ValueError("Price must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid price")
            return

        # Update in data
        success = update_menu_item(
            category,
            item_name,
            base_price
        )

        if success:
            messagebox.showinfo("Success", "Item updated successfully!")
            self.go_back()
        else:
            messagebox.showerror("Error", "Failed to update item")

    def go_back(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        from admin_dashboard import AdminDashboard
        admin_dashboard = AdminDashboard(self.parent)
        admin_dashboard.pack(fill=tk.BOTH, expand=True)


class DeleteItemScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg='white')
        self.selected_item = None
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure(
            'Coffee.TButton',
            font=('Arial', 12),
            padding=10,
            foreground='#6F4E37',
            background='#D2B48C'
        )
        style.map(
            'Coffee.TButton',
            background=[('active', '#C4A484')]
        )

        # Back button
        back_button = ttk.Button(
            self,
            text="Back",
            command=self.go_back,
            style='Coffee.TButton'
        )
        back_button.pack(anchor="nw", padx=10, pady=10)

        # Title
        title_label = tk.Label(
            self,
            text="Delete Menu Item",
            font=("Arial", 20, "bold"),
            pady=20,
            bg='white',
            fg='#6F4E37'
        )
        title_label.pack()

        # Selection frame
        selection_frame = tk.Frame(self, bg='white')
        selection_frame.pack(expand=True, padx=50, pady=10)

        # Category selection
        tk.Label(
            selection_frame,
            text="Select Category:",
            font=("Arial", 12),
            bg='white',
            fg='#6F4E37'
        ).grid(row=0, column=0, sticky="w", pady=5)

        self.category_var = tk.StringVar()
        categories = get_categories()
        category_menu = ttk.Combobox(
            selection_frame,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            font=("Arial", 12)
        )
        category_menu.grid(row=0, column=1, sticky="ew", pady=5)
        category_menu.bind('<<ComboboxSelected>>', self.update_item_list)

        # Item selection
        tk.Label(
            selection_frame,
            text="Select Item:",
            font=("Arial", 12),
            bg='white',
            fg='#6F4E37'
        ).grid(row=1, column=0, sticky="w", pady=5)

        self.item_var = tk.StringVar()
        self.item_menu = ttk.Combobox(
            selection_frame,
            textvariable=self.item_var,
            state="readonly",
            font=("Arial", 12)
        )
        self.item_menu.grid(row=1, column=1, sticky="ew", pady=5)
        self.item_menu.bind('<<ComboboxSelected>>', self.select_item)

        # Delete button
        self.delete_button = ttk.Button(
            selection_frame,
            text="Delete Item",
            command=self.delete_item,
            style='Coffee.TButton'
        )
        self.delete_button.grid(row=2, column=0, columnspan=2, pady=20)
        self.delete_button.config(state="disabled")

        # Configure grid weights
        selection_frame.columnconfigure(1, weight=1)

    def update_item_list(self, event=None):
        from data import get_items_by_category
        category = self.category_var.get()
        if category:
            items = get_items_by_category(category)
            self.item_menu['values'] = items
            self.item_var.set('')
            self.selected_item = None
            self.delete_button.config(state="disabled")

    def select_item(self, event=None):
        category = self.category_var.get()
        item_name = self.item_var.get()

        if category and item_name:
            self.selected_item = (category, item_name)
            self.delete_button.config(state="normal")

    def delete_item(self):
        if not self.selected_item:
            messagebox.showerror("Error", "Please select an item to delete")
            return

        category, item_name = self.selected_item

        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{item_name}' from '{category}'?"
        )

        if result:
            from data import delete_menu_item
            success = delete_menu_item(category, item_name)

            if success:
                messagebox.showinfo("Success", "Item deleted successfully!")
                self.go_back()
            else:
                messagebox.showerror("Error", "Failed to delete item")

    def go_back(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        from admin_dashboard import AdminDashboard
        admin_dashboard = AdminDashboard(self.parent)
        admin_dashboard.pack(fill=tk.BOTH, expand=True)
