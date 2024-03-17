import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import sheet_functions as sheet_func


class SpreadSheet(ScrolledFrame):
    def __init__(self, main, name):
        super().__init__()

        self.name = name

        self.balance = 0

        self.cells = {}
        self.sheet_cells = []

        self.pluses = []
        self.minuses = []
        self.totals = []

        self.x_axis_labels = ["Date", "Subject", "Plus", "Minus", "Total"]
        self.y_axis = 32

        self.columnconfigure((0, 2, 3, 4), weight=0)
        self.columnconfigure(1, weight=1)

        for i, label in enumerate(self.x_axis_labels):
            self.text = ttkb.Label(self, text=label)
            self.text.grid(column=i, row=0, sticky=tk.NW)


        self.main_sheet_cells = []
        for y in range(self.y_axis):
            self.inner_sheet_cells = []
            for coord, x in enumerate(self.x_axis_labels):
                self.id = f"{name}{x}:{y}"

                self.var = tk.StringVar(self, "", self.id)
                self.entry_cell = ttkb.Entry(self, textvariable=self.var, width=8)

                if x == "Plus":
                    self.entry_cell["width"] = 5
                    self.entry_cell.bind("<FocusOut>", self.calculate_spreadsheet)
                    self.pluses.append(self.entry_cell)
                elif x == "Minus":
                    self.entry_cell["width"] = 5
                    self.entry_cell.bind("<FocusOut>", self.calculate_spreadsheet)
                    self.minuses.append(self.entry_cell)
                elif x == "Total":
                    self.totals.append(self.entry_cell)


                self.inner_sheet_cells.append(self.entry_cell)
                self.entry_cell.grid(column=coord, row=y+1, sticky=tk.NSEW)

                self.cells[self.id] = self.var

            self.main_sheet_cells.append(self.inner_sheet_cells)

        self.load_spreadsheet()


    def calculate_spreadsheet(self, *args):
        for i in range(self.y_axis):
            self.total = self.trim_value(self.totals[i].get())
            self.plus = self.trim_value(self.pluses[i].get())
            self.minus = self.trim_value(self.minuses[i].get())

            self.value = (
                float(0 if self.plus is None else self.plus) 
                - float(0 if self.minus is None else self.minus)
            )

            if self.value == 0.0:
                self.totals[i].delete(0, tk.END)
            else:
                self.totals[i].delete(0, tk.END)
                self.totals[i].insert(0, self.value)

                print(self.balance, self.value)


    def trim_value(self, value):
        if not value == "":
            if '+' or '-' in value[0]:
                return value[1:]


    def generate_csv(self, *args):
        self.header = self.x_axis_labels
        self.csv_data = []
        for key, value in self.cells.items():
            self.csv_data.append(value.get())

        self.counter = 0
        self.main_array = []
        for y in range(self.y_axis):
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