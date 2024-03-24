import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame

import window as window
import observer_pattern as observe
import csv_functions as sheet_func


class MenuBar(tk.Menu):
    def __init__(self, main):
        super().__init__()

        self.file_menu = tk.Menu(self)
        self.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open...", command=self.open_file)

    def open_file(self):
        pass


class TopPanel(ttkb.Frame, observe.Observerable):
    def __init__(self, main, observable="observable"):
        ttkb.Frame.__init__(self)
        observe.Observerable.__init__(self)

        self.sheet_var = tk.StringVar()
        self.sheet_var.trace_add("write", self.sheet_selected)

        self.title_label = ttkb.Label(self, text=self.sheet_var.get())
        self.title_label.pack(side=tk.BOTTOM)

        self.dropdown = ttkb.Menubutton(self, text="Sheets")
        self.dropdown.menu = tk.Menu(self)
        self.dropdown["menu"] = self.dropdown.menu
        self.dropdown.pack(side=tk.LEFT, padx=(0, 5))

        self.deposit_button = ttkb.Button(self, text="Deposit", takefocus=False, command=self.create_deposit_window)
        self.deposit_button.pack(side=tk.LEFT, padx=(0, 5))

        self.widthdrawl_button = ttkb.Button(self, text="Widthdrawl", takefocus=False, command=self.create_widthdrawl_window)
        self.widthdrawl_button.pack(side=tk.LEFT)

    def add_dropdown_options(self, options):
        for i, label in enumerate(options):
            self.dropdown.menu.add_radiobutton(
                label = options[i],
                value = options[i],
                variable = self.sheet_var
            )

    def create_deposit_window(self):
        DepositWindow(self)

    def create_widthdrawl_window(self):
        WidthdrawlWindow(self)

    def sheet_selected(self, *args):
        signal = self.sheet_var.get()
        self.title_label["text"] = signal
        self.send_signal(signal)


class PopupWindow(ttkb.Frame):
    def __init__(self, main):
        super().__init__()

        self.grab_set()

        self.configure(style="primary.TFrame")

        self.columnconfigure((0, 2), weight=0)
        self.columnconfigure(1, weight=2)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.title = ttkb.Label(self, text="Undefined", bootstyle="secondary.TLabel")
        self.title.grid(row=0, column=1, padx=10, pady=10, sticky=tk.N)

        self.sumbit_button = ttkb.Button(self, text="Submit", bootstyle="success", command=self.submit)
        self.sumbit_button.grid(row=4, column=2, padx=10, pady=10, sticky=tk.SW)

        self.back_button = ttkb.Button(self, text="Back", bootstyle="danger", command=self.back)
        self.back_button.grid(row=4, column=0, padx=10, pady=10, sticky=tk.SE)

        self.place(rely=0.4, relx=0.5, relheight=0.5, relwidth=0.5, anchor=tk.CENTER)

    def submit(self):
        print("Submitted m'lord")

    def back(self):
        self.destroy()


class DepositWindow(PopupWindow):
    def __init__(self, main):
        super().__init__(self)

        self.title["text"] = "Deposit"

    def submit(self):
        print("Deposited!")


class WidthdrawlWindow(PopupWindow):
    def __init__(self, main):
        super().__init__(self)

        self.title["text"] = "Widthdrawl"

    def submit(self):
        print("Widthdrawn!")


class SpreadSheet(ScrolledFrame, observe.Observer):
    def __init__(self, main):
        ScrolledFrame.__init__(self)

        self.sheet_name = "Moose"

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
                self.id = f"{x}:{y}"

                self.var = tk.StringVar(self, "", self.id)
                self.entry_cell = ttkb.Entry(self, textvariable=self.var, width=8)
                self.entry_cell.grid(column=coord, row=y+1, sticky=tk.NSEW)
                self.entry_cell.configure(state="disabled")

                if x == "Plus":
                    self.entry_cell["width"] = 5
                    self.pluses.append(self.entry_cell)
                elif x == "Minus":
                    self.entry_cell["width"] = 5
                    self.minuses.append(self.entry_cell)
                elif x == "Total":
                    self.totals.append(self.entry_cell)
                    self.entry_cell.grid(padx=(0, 15))


                self.inner_sheet_cells.append(self.entry_cell)

                self.cells[self.id] = self.var

            self.main_sheet_cells.append(self.inner_sheet_cells)


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

        sheet_func.write_csv(self.sheet_name, self.header, self.main_array)


    def load_spreadsheet(self, name):
        sheet_func.create_directory()

        try:
            csv_file = sheet_func.read_csv(name)
        except FileNotFoundError:
            print("Read action failed.")
            return

        for y in range(self.y_axis):
            for coord, x in enumerate(self.x_axis_labels):
                var = self.main_sheet_cells[y][coord]
                var.configure(state="normal")
                var.insert(0, csv_file[1:][y][coord])
                var.configure(state="disabled")


    def receive_signal(self, observable, value=None, *args, **kwargs):
        self.sheet_name = value
        self.load_spreadsheet(value)

        print(value)