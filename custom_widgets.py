import tkinter as tk
from tkinter import ttk
import sheet_functions as sheet_func

class ScrollableCanvas(tk.Canvas):
    def __init__(self, main, name):
        self.name = name

        tk.Canvas.__init__(self)
        self["highlightthickness"] = 0

        self.new_sheet = SpreadSheet(self)

        self.bind('<Configure>', self.canvas_config)

        self.create_window((0,0), window=self.new_sheet, anchor=tk.NW, tags=name)

        self.pack(fill=tk.BOTH, expand=1)


    def canvas_config(self, event):
        self.configure(scrollregion=self.bbox("all"))
        self.itemconfigure(self.name, width=event.width)
        self.bind_all('<MouseWheel>', lambda event: self.yview_scroll(int(-1*(event.delta)), "units"))


    def link_scrollbar(self, scrollbar):
        self.configure(yscrollcommand=scrollbar.set)


class SpreadSheet(tk.Frame):
    def __init__(self, main):
        tk.Frame.__init__(self)

        self.cells = {}
        self.sheet_cells = []

        self.x_axis_labels = ["Date", "Subject", "Plus", "Minus", "Total"]
        self.y_axis = range(32)

        self.grid_columnconfigure((0, 2, 3, 4), weight=0)
        self.grid_columnconfigure(2, weight=1)

        for i, label in enumerate(self.x_axis_labels):
            self.text = tk.Label(self, text=label)
            self.text.grid(column=i, row=0, sticky=tk.NW)


        for y in self.y_axis:
            for coord, x in enumerate(self.x_axis_labels):
                i = 0
                self.id = f"{x}:{y}"
                self.var = tk.StringVar(self, "", self.id)
                self.var.trace("w", self.generate_csv)
                self.entry_cell = tk.Entry(self, textvariable=self.var, width=8)
                self.sheet_cells.append(self.entry_cell)
                self.entry_cell.grid(column=coord, row=y+1, sticky=tk.EW)
                self.cells[self.id] = self.var
                i += 1


    def generate_csv(self, *args):
        self.header = self.x_axis_labels
        self.csv_data = []
        for key, value in self.cells.items():
            self.csv_data.append(value.get())

        self.counter = 0
        self.main_array = []
        for y in self.y_axis:
            self.inner_array = []
            for x in self.x_axis_labels:
                self.inner_array.append(self.csv_data[self.counter])
                self.counter += 1
            self.main_array.append(self.inner_array)

        sheet_func.write_csv("moose", self.header, self.main_array)