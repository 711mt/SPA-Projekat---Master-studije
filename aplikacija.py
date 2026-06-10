import tkinter as tk
from tkinter import ttk

from gui.stek_panel import StekPanel
from gui.red_panel import RedPanel


class Aplikacija(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vizuelna simulacija rada steka i reda")
        self.geometry("900x680")
        self.minsize(760, 560)
        self.configure(bg="white")

        stil = ttk.Style(self)
        stil.configure("TNotebook.Tab", font=("Helvetica", 11), padding=(14, 6))

        tabovi = ttk.Notebook(self)
        tabovi.pack(fill=tk.BOTH, expand=True)
        tabovi.add(StekPanel(tabovi), text="Stek (LIFO)")
        tabovi.add(RedPanel(tabovi), text="Red (FIFO)")
def main():
    aplikacija = Aplikacija()
    aplikacija.mainloop()

if __name__ == "__main__":
    main()
