import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import custom_widgets as mk

import window as window
from styles import FONT_MAIN

names = ["Moose", "Bryce", "Cam"]


class MainApp(ttkb.Window):
    def __init__(self):
        super().__init__()

        self.title(window.WINDOW_TITLE)
        self.minsize(window.WINDOW_WIDTH, window.WINDOW_HEIGHT)
        self.style.theme_use("vapor")

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.geometry(window.window_size(self.screen_width, self.screen_height))


    def create_spreadsheet(self):
        self.frame = mk.SpreadSheet(self)
        self.frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, padx=(10, 0), pady=10)


    def create_menu_bar(self):
        new_menu = mk.MenuBar(self)
        self.config(menu=new_menu)


    def create_top_panel(self):
        top_panel = mk.TopPanel(self)
        top_panel.add_dropdown_options(names)
        top_panel.subscribe(self.frame)
        top_panel.pack(fill=tk.BOTH, padx=(10, 0), pady=10)


if __name__ == "__main__":
    app = MainApp()
    app.create_menu_bar()
    app.create_spreadsheet()
    app.create_top_panel()
    app.mainloop()