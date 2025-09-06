import tkinter as tk
from tkinter import ttk, messagebox
from menu_screen import MenuScreen


class AdminDashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg='white')
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure(
            'Coffee.TButton',
            font=('Arial', 14),
            padding=15,
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
            text="Admin Dashboard",
            font=("Arial", 24, "bold"),
            pady=30,
            bg='white',
            fg='#6F4E37'
        )
        title_label.pack()

        # Button frame
        button_frame = tk.Frame(self, bg='white')
        button_frame.pack(expand=True)

        # Add Item button
        add_button = ttk.Button(
            button_frame,
            text="Add Menu Item",
            command=self.add_item,
            style='Coffee.TButton'
        )
        add_button.pack(fill=tk.X, pady=15, padx=50)

        # Update Item button
        update_button = ttk.Button(
            button_frame,
            text="Update Menu Item",
            command=self.update_item,
            style='Coffee.TButton'
        )
        update_button.pack(fill=tk.X, pady=15, padx=50)

        # Delete Item button
        delete_button = ttk.Button(
            button_frame,
            text="Delete Menu Item",
            command=self.delete_item,
            style='Coffee.TButton'
        )
        delete_button.pack(fill=tk.X, pady=15, padx=50)

    def add_item(self):
        from admin_crud import AddItemScreen
        self.show_crud_screen(AddItemScreen)

    def update_item(self):
        from admin_crud import UpdateItemScreen
        self.show_crud_screen(UpdateItemScreen)

    def delete_item(self):
        from admin_crud import DeleteItemScreen
        self.show_crud_screen(DeleteItemScreen)

    def show_crud_screen(self, screen_class):
        for widget in self.parent.winfo_children():
            widget.destroy()
        screen = screen_class(self.parent)
        screen.pack(fill=tk.BOTH, expand=True)

    def go_back(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        from welcome_screen import WelcomeScreen
        welcome_screen = WelcomeScreen(self.parent)
        welcome_screen.pack(fill=tk.BOTH, expand=True)
