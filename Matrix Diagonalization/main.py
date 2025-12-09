import tkinter as tk
from gui import MatrixDiagonalizationApp

def main():
    root = tk.Tk()
    app = MatrixDiagonalizationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()