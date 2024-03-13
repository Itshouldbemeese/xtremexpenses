import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import sheet_functions as sheet_func


class SpreadSheet(ScrolledFrame):
    def __init__(self, main, name):
        super().__init__()

        self.name = name

        self.cells = {}
        self.sheet_cells = []
        self.totals = []

        self.x_axis_labels = ["Date", "Subject", "Plus", "Minus", "Total"]
        self.y_axis = range(32)

        self.columnconfigure((0, 2, 3, 4), weight=0)
        self.columnconfigure(1, weight=1)

        for i, label in enumerate(self.x_axis_labels):
            self.text = ttkb.Label(self, text=label)
            self.text.grid(column=i, row=0, sticky=tk.NW)


        self.main_sheet_cells = []
        for y in self.y_axis:
            self.inner_sheet_cells = []
            for coord, x in enumerate(self.x_axis_labels):
                self.id = f"{name}{x}:{y}"

                self.var = tk.StringVar(self, "", self.id)
                self.var.trace("w", self.generate_csv)

                if x == "Total":
                    self.entry_cell = ttkb.Entry(self, textvariable=self.var, width=8)
                    self.totals.append(self.entry_cell)
                else:
                    self.entry_cell = ttkb.Entry(self, textvariable=self.var, width=8)

                self.inner_sheet_cells.append(self.entry_cell)
                self.entry_cell.grid(column=coord, row=y+1, sticky=tk.NSEW)

                self.cells[self.id] = self.var

            self.main_sheet_cells.append(self.inner_sheet_cells)

        self.load_spreadsheet()


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

        sheet_func.write_csv(self.name, self.header, self.main_array)


    def load_spreadsheet(self):
        sheet_func.create_directory()

        try:
            csv_file = sheet_func.read_csv(self.name)
        except FileNotFoundError:
            print("Read action failed.")
            return

        for y in self.y_axis:
            for coord, x in enumerate(self.x_axis_labels):
                var = self.main_sheet_cells[y][coord]
                var.insert(0, csv_file[1:][y][coord])


    def print_data(self):
        spread = []
        children = self.winfo_children()
        for x, i in enumerate(children):
            if children[1:][x].name == "total":
                spread.append(children[1:][x])
                print(spread)