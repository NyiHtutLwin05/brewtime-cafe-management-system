# menu_screen.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from data import get_categories, get_items_by_category, get_item_base_price, calculate_item_price, get_addon_prices, get_size_modifiers


class MenuScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # Changed to white background to match welcome screen
        self.configure(bg='white')
        self.create_widgets()

    def create_widgets(self):
        # Configure styles to match welcome screen
        style = ttk.Style()

        # Button style
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

        # Back button
        back_button = ttk.Button(
            self,
            text="Back",
            command=self.go_back,
            style='Coffee.TButton'
        )
        back_button.pack(anchor="nw", padx=10, pady=10)

        # Title label with matching color scheme
        title_label = tk.Label(
            self,
            text="BrewTime Cafe - Today's Menu",
            font=("Arial", 18, "bold"),
            pady=15,
            bg='white',
            fg='#6F4E37'
        )
        title_label.pack()

        # Create notebook with custom style to match theme
        style.configure(
            'Coffee.TNotebook',
            background='white',
            bordercolor='#6F4E37'
        )
        style.configure(
            'Coffee.TNotebook.Tab',
            background='#D2B48C',
            foreground='#6F4E37',
            padding=[10, 5],
            font=('Arial', 10, 'bold')
        )
        style.map(
            'Coffee.TNotebook.Tab',
            background=[('selected', '#C4A484'), ('active', '#E6D5B8')]
        )

        notebook = ttk.Notebook(self, style='Coffee.TNotebook')

        # Create tabs for each category
        categories = get_categories()
        for category in categories:
            category_tab = tk.Frame(notebook, bg='white')
            self.create_category_menu(category_tab, category)
            notebook.add(category_tab, text=category)

        notebook.pack(expand=True, fill="both", padx=20, pady=10)

    def create_category_menu(self, parent, category):
        items = get_items_by_category(category)
        size_modifiers = get_size_modifiers()

        # Create a frame to hold the canvas and scrollbar
        container = tk.Frame(parent, bg='white')
        container.pack(fill='both', expand=True)

        # Create canvas and scrollbar
        canvas = tk.Canvas(container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

       # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

       # Add menu items to the scrollable frame
        for item in items:
            base_price = get_item_base_price(category, item)
            prices = {}
            for size, modifier in size_modifiers.items():
                total_price = calculate_item_price(base_price, size, [])
                prices[size] = total_price

            price_texts = [f"{size}: ${price:.2f}" for size,
                           price in prices.items()]
            self.create_menu_item(scrollable_frame, item, price_texts)

    def create_menu_item(self, parent, name, prices):
        """Helper function to create consistent menu items with matching colors"""
        if not prices:
            prices = ["Price not available"]
        frame = tk.Frame(parent, bg='white', padx=10, pady=5)

        # Item name
        tk.Label(
            frame,
            text=name,
            font=("Arial", 12, "bold"),
            bg='white',
            fg='#6F4E37'
        ).pack(anchor="w")

        # Prices
        for price in prices:
            tk.Label(
                frame,
                text=price,
                font=("Arial", 10),
                bg='white',
                fg='#6F4E37'
            ).pack(anchor="w")

        # Separator
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=5)

        frame.pack(fill="x", padx=15, pady=5)

    def go_back(self):
        """Return to welcome screen"""
        for widget in self.parent.winfo_children():
            widget.destroy()

        from welcome_screen import WelcomeScreen
        welcome_screen = WelcomeScreen(self.parent)
        welcome_screen.pack(fill=tk.BOTH, expand=True)
