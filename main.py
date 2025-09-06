from welcome_screen import WelcomeScreen
import tkinter as tk
from tkinter import messagebox
from theme_manager import configure_theme

# Initialize the main application window
root = tk.Tk()
root.title("BrewTime Cafe")  # Set window title
root.geometry("900x800")     # Define default window size

# Apply theme settings based on operating system
configure_theme(root)

# Create and display the welcome screen as the starting UI
welcome_screen = WelcomeScreen(root)
welcome_screen.pack(fill=tk.BOTH, expand=True)

# Run the Tkinter event loop
root.mainloop()
