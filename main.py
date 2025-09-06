import tkinter as tk
from tkinter import messagebox
from theme_manager import configure_theme
from welcome_screen import WelcomeScreen


class BrewTimeCafeApp:
    """Main application class for BrewTime Cafe system."""

    def __init__(self, root):
        # Store root window
        self.root = root
        self.root.title("BrewTime Cafe")
        self.root.geometry("900x800")

        # Configure theme based on OS
        configure_theme(self.root)

        # Initialize Welcome Screen
        self.welcome_screen = WelcomeScreen(self.root)
        self.welcome_screen.pack(fill=tk.BOTH, expand=True)

    def run(self):
        """Run the Tkinter main loop."""
        self.root.mainloop()


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = BrewTimeCafeApp(root)
    app.run()
