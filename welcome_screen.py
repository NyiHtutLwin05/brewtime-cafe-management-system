import tkinter as tk
from tkinter import ttk
from menu_screen import MenuScreen


class WelcomeScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg='white')
        self.create_widgets()

    def create_widgets(self):
        # Welcome label
        welcome_label = tk.Label(
            self,
            text="Welcome to BrewTime Cafe!",
            font=("Arial", 24, "bold"),
            pady=40,
            bg='white',
            fg='#6F4E37'
        )
        welcome_label.pack()

        button_frame = tk.Frame(self, bg='white', padx=20, pady=20)
        button_frame.pack(expand=True)

        style = ttk.Style()

        style.configure(
            'Coffee.TButton',
            font=('Arial', 14, 'bold'),
            width=40,
            padding=40,
            foreground='#6F4E37',
            background='#D2B48C',
            bordercolor='#6F4E37',
            relief=tk.RAISED,
            anchor='center'
        )

        style.map(
            'Coffee.TButton',
            background=[('active', '#C4A484')],
            # Keep same text color when active
            foreground=[('active', '#6F4E37')],
            relief=[('pressed', tk.SUNKEN)]
        )

        # Button options dictionary for consistent styling
        button_options = {
            'style': 'Coffee.TButton',
            'padding': (15, 10)
        }

        # Show Menu button
        menu_button = ttk.Button(
            button_frame,
            text="Show Menu",
            command=self.show_menu,
            **button_options
        )
        # ipady adds internal padding
        menu_button.pack(fill=tk.X, pady=15, ipady=10)

        # Place Order button
        order_button = ttk.Button(
            button_frame,
            text="Place Order",
            command=self.show_order_screen,
            **button_options
        )
        order_button.pack(fill=tk.X, pady=15, ipady=10)

        admin_button = ttk.Button(
            button_frame,
            text="Login as Admin",
            command=self.show_admin_login,
            **button_options
        )

        admin_button.pack(fill=tk.X, pady=15, ipady=10)

    def show_menu(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        menu_screen = MenuScreen(self.parent)
        menu_screen.pack(fill=tk.BOTH, expand=True)

    def show_order_screen(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        from order_screen import OrderScreen
        order_screen = OrderScreen(self.parent)
        order_screen.pack(fill=tk.BOTH, expand=True)

    def show_admin_login(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        from admin_login import AdminLoginScreen
        admin_login = AdminLoginScreen(self.parent)
        admin_login.pack(fill=tk.BOTH, expand=True)
