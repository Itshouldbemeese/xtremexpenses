import tkinter as tk
from tkinter import ttk
import sheet_functions as sheet_func
import custom_widgets as mk

from window import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, window_size
from styles import FONT_MAIN


sheet_tabs = []

names = ["Moose", "Bryce", "Cam"]


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(WINDOW_TITLE)
        self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.geometry(window_size(self.screen_width, self.screen_height))

        tabs = ttk.Notebook(self)

        scrollbar = ttk.Scrollbar(tabs, orient=tk.VERTICAL, command=multiple_yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # self.bind('<<NotebookTabChanged>>',  print_data)

        for i, name in enumerate(names):
            new_sheet = mk.ScrollableCanvas(tabs, name)
            sheet_tabs.append(new_sheet)
            new_sheet.link_scrollbar(scrollbar)

            tabs.add(new_sheet, text=name)

        tabs.pack(fill=tk.BOTH, expand=1)


def multiple_yview(*args):
    for i in sheet_tabs:
        i.yview_scroll(*args)


# def generate_spreadsheet(event=None):
#     name = tabs.select()
#     parent = tabs.nametowidget(name)


# def print_data(*args):
#     for key, value in cells.items():
#         print(f"{key} : {value.get()}")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()