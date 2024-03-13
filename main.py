import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import custom_widgets as mk

from window import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, window_size
from styles import FONT_MAIN

names = ["Moose", "Bryce", "Cam"]


class MainApp(ttkb.Window):
    def __init__(self):
        super().__init__()

        self.title(WINDOW_TITLE)
        self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.style.theme_use("vapor")

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.geometry(window_size(self.screen_width, self.screen_height))


    def create_spreadsheet(self):
        tabs = ttkb.Notebook(self)
        tabs.pack(fill=tk.BOTH, expand=True)

        for x, label in enumerate(names):
            frame = mk.SpreadSheet(tabs, label)
            tabs.add(frame.container, text=label)


if __name__ == "__main__":
    app = MainApp()
    app.create_spreadsheet()
    app.mainloop()