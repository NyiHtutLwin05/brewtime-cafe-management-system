# admin_login.py
import tkinter as tk
from tkinter import ttk, messagebox


class AdminLoginScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg='white')
        self.create_widgets()

        self.admin_password = "123"

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

        # Configure entry style for better appearance
        style.configure(
            'Coffee.TEntry',
            fieldbackground='white',
            foreground='#6F4E37',
            font=('Arial', 12),
            padding=8
        )

        # Back button
        back_button = ttk.Button(
            self,
            text="← Back",
            command=self.go_back,
            style='Coffee.TButton'
        )
        back_button.pack(anchor="nw", padx=10, pady=10)

        # Main login container with better spacing
        login_container = tk.Frame(self, bg='white')
        login_container.pack(expand=True, fill='both', pady=80)

        # Title with better spacing
        title_label = tk.Label(
            login_container,
            text="Admin Login",
            font=("Arial", 28, "bold"),
            bg='white',
            fg='#6F4E37',
            pady=30
        )
        title_label.pack()

        # Login frame with grid layout for better control
        login_frame = tk.Frame(login_container, bg='white')
        login_frame.pack(expand=True)

        # Password label
        password_label = tk.Label(
            login_frame,
            text="Password:",
            font=("Arial", 14),
            bg='white',
            fg='#6F4E37'
        )
        password_label.grid(row=0, column=0, sticky="w",
                            pady=(0, 8), padx=(0, 10))

        # Password entry - larger and better styled
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(
            login_frame,
            textvariable=self.password_var,
            show="*",
            style='Coffee.TEntry',
            width=25,
            font=("Arial", 14)
        )
        password_entry.grid(row=0, column=1, sticky="ew",
                            pady=(0, 8), padx=(10, 0))

        # Configure grid weights for proper resizing
        login_frame.columnconfigure(1, weight=1)

        # Login button - better proportioned
        login_button = ttk.Button(
            login_frame,
            text="Login",
            command=self.attempt_login,
            style='Coffee.TButton',
            width=15  # Consistent width
        )
        login_button.grid(row=1, column=0, columnspan=2, pady=25)

        # Center the login frame content
        login_container.grid_rowconfigure(0, weight=1)
        login_container.grid_columnconfigure(0, weight=1)
        login_frame.grid_rowconfigure(1, weight=1)

        # Bind Enter key to login
        password_entry.bind('<Return>', lambda event: self.attempt_login())

    def attempt_login(self):
        if self.password_var.get() == self.admin_password:
            self.show_admin_dashboard()
        else:
            messagebox.showerror("Login Failed", "Incorrect password")

    def show_admin_dashboard(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        from admin_dashboard import AdminDashboard
        admin_dashboard = AdminDashboard(self.parent)
        admin_dashboard.pack(fill=tk.BOTH, expand=True)

    def go_back(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        from welcome_screen import WelcomeScreen
        welcome_screen = WelcomeScreen(self.parent)
        welcome_screen.pack(fill=tk.BOTH, expand=True)
