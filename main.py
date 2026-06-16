# main.py
import tkinter as tk
from gui import SistemPakarGiziApp

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemPakarGiziApp(root)
    root.mainloop()