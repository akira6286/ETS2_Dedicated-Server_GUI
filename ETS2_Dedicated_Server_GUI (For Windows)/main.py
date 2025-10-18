# main.py

import sys, os

BASE_DIR = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
TEMPLATES_DIR = os.path.join(BASE_DIR, "config_manager", "templates")
GENERATED_DIR = os.path.join(BASE_DIR, "generated")
os.makedirs(GENERATED_DIR, exist_ok=True)







import tkinter as tk
from modules.gui import ServerConfigGUI

def main():
    root = tk.Tk()
    app = ServerConfigGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
