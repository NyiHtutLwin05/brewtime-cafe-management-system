from welcome_screen import WelcomeScreen
import tkinter as tk
from theme_manager import configure_theme

root = tk.Tk()
root.title("BrewTime Cafe")
root.geometry("900x800")

# Configure theme based on OS
configure_theme(root)

welcome_screen = WelcomeScreen(root)
welcome_screen.pack(fill=tk.BOTH, expand=True)

root.mainloop()
