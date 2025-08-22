# theme_manager.py
import tkinter as tk
from tkinter import ttk
import platform


def configure_theme(root):
    style = ttk.Style()

    # Detect operating system
    system = platform.system()

    if system == "Windows":
        # Windows-specific theme
        try:
            style.theme_use('vista')
        except:
            style.theme_use('winnative')
    elif system == "Linux":
        # Linux-specific theme (for WSL)
        try:
            style.theme_use('clam')
        except:
            pass
    else:
        # macOS or other
        style.theme_use('clam')

    # Cross-platform style configurations
    style.configure(
        'Coffee.TButton',
        font=('Arial', 12),
        padding=(15, 8),
        foreground='#6F4E37',
        background='#D2B48C'
    )

    style.map(
        'Coffee.TButton',
        background=[('active', '#C4A484'), ('pressed', '#A68B65')],
        relief=[('pressed', 'sunken'), ('!pressed', 'raised')]
    )
