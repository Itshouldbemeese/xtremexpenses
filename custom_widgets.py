import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import sheet_functions as sheet_func


class MenuBar(tk.Menu):
    def __init__(self, main):
        super().__init__()

        self.file_menu = tk.Menu(self)
        self.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open...", command=self.open_file)

    def open_file(self):
        pass


class TopPanel(ttkb.Frame):
    def __init__(self, main):
        super().__init__()

        self.sheet_var = tk.StringVar()
        self.sheet_var.trace_add("write", self.sheet_selected)

        self.sheet_dropdown = ttkb.Menubutton(self, text="Sheets")
        self.sheet_dropdown.pack(side=tk.LEFT, padx=(0, 5))

        self.menu = tk.Menu(self.sheet_dropdown)

        self.sheet_dropdown["menu"] = self.menu

        self.deposit_button = ttkb.Button(self, text="Deposit", takefocus=False)
        self.deposit_button.pack(side=tk.LEFT, padx=(0, 5))

        self.widthdrawl_button = ttkb.Button(self, text="Widthdrawl", takefocus=False)
        self.widthdrawl_button.pack(side=tk.LEFT)


    def add_dropdown_options(self, options):
        for i, label in enumerate(options):
            self.menu.add_radiobutton(
                label = options[i],
                value = options[i],
                variable = self.sheet_var
            )


    def sheet_selected(self):
        pass


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
                self.entry_cell.grid(column=coord, row=y+1, sticky=tk.NSEW)
                self.entry_cell.configure(state="disabled")

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
                    self.entry_cell.grid(padx=(0, 15))


                self.inner_sheet_cells.append(self.entry_cell)

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