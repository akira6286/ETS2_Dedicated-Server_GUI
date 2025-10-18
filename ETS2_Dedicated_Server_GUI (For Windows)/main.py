# assets/main.py

import tkinter as tk
from modules.gui import ServerConfigGUI

def main():
    root = tk.Tk()
    app = ServerConfigGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
