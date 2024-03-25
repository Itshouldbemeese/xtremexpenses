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
    def __init__(self, main, spreadsheet, observable="observable"):
        ttkb.Frame.__init__(self)
        observe.Observerable.__init__(self)

        self.spreadsheet = spreadsheet

        self.subscribe(spreadsheet)

        self.sheet_var = tk.StringVar()
        self.sheet_var.trace_add("write", self.sheet_selected)

        self.dropdown = ttkb.Menubutton(self, text="Accounts", takefocus=False, width=8)
        self.dropdown.menu = tk.Menu(self)
        self.dropdown["menu"] = self.dropdown.menu
        self.dropdown.pack(side=tk.LEFT, padx=(0, 5))

        self.deposit_button = ttkb.Button(self, text="Deposit", takefocus=False, command=self.create_deposit_window)
        self.deposit_button.configure(state=tk.DISABLED)
        self.deposit_button.pack(side=tk.LEFT, padx=(0, 5))

        self.widthdrawl_button = ttkb.Button(self, text="Widthdrawl", takefocus=False, command=self.create_widthdrawl_window)
        self.widthdrawl_button.configure(state=tk.DISABLED)
        self.widthdrawl_button.pack(side=tk.LEFT)

    def add_dropdown_options(self, options):
        for i, label in enumerate(options):
            self.dropdown.menu.add_radiobutton(
                label = options[i],
                value = options[i],
                variable = self.sheet_var
            )

    def create_deposit_window(self):
        deposit = DepositWindow(self, self.sheet_var.get())
        deposit.subscribe(self.spreadsheet)

    def create_widthdrawl_window(self):
        widthdrawl = WidthdrawlWindow(self, self.sheet_var.get())
        widthdrawl.subscribe(self.spreadsheet)

    def sheet_selected(self, *args):
        signal = self.sheet_var.get()
        self.dropdown["text"] = signal

        self.send_signal(signal)

        self.deposit_button.configure(state=tk.NORMAL)
        self.widthdrawl_button.configure(state=tk.NORMAL)


class PopupWindow(ttkb.Frame):
    def __init__(self):
        super().__init__()

        self.grab_set()

        self.configure(style="primary.TFrame")

        self.columnconfigure((0, 2), weight=0)
        self.columnconfigure(1, weight=2)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        self.current_sheet = ""

        self.date_var = tk.StringVar(self, "", "date")
        self.subject_var = tk.StringVar(self, "", "subject")
        self.value_var = tk.StringVar(self, "", "value")

        self.title = ttkb.Label(self, text="Undefined", bootstyle="secondary.TLabel")
        self.title.grid(row=0, column=1, padx=10, pady=10, sticky=tk.N)

        self.date = ttkb.Label(self, text="Date")
        self.date.grid(row=1, column=0, columnspan=3, padx=10, sticky=tk.EW)

        self.date_entry = ttkb.Entry(self, textvariable=self.date_var)
        self.date_entry.grid(row=2, column=0, columnspan=3, padx=10, sticky=tk.EW)

        self.subject = ttkb.Label(self, text="Subject")
        self.subject.grid(row=3, column=0, columnspan=3, padx=10, sticky=tk.EW)

        self.subject_entry = ttkb.Entry(self, textvariable=self.subject_var)
        self.subject_entry.grid(row=4, column=0, columnspan=3, padx=10, sticky=tk.EW)

        self.value = ttkb.Label(self, text="Value")
        self.value.grid(row=5, column=0, columnspan=3, padx=10, sticky=tk.EW)

        self.value_entry = ttkb.Entry(self, textvariable=self.value_var)
        self.value_entry.grid(row=6, column=0, columnspan=3, padx=10, sticky=tk.EW)

        self.sumbit_button = ttkb.Button(self, text="Submit", bootstyle="success", command=self.submit)
        self.sumbit_button.grid(row=7, column=2, padx=10, pady=10, sticky=tk.SW)

        self.back_button = ttkb.Button(self, text="Back", bootstyle="danger", command=self.back)
        self.back_button.grid(row=7, column=0, padx=10, pady=10, sticky=tk.SE)

        self.place(rely=0.4, relx=0.5, relheight=0.6, relwidth=0.5, anchor=tk.CENTER)

    def submit(self):
        print("Submitted m'lord")

    def back(self):
        self.destroy()

    def trim_value(self, value):
        if not value == "":
            if '+' or '-' in value[0]:
                return value[1:]


class DepositWindow(PopupWindow, observe.Observerable):
    def __init__(self, main, current, observable = "observable"):
        PopupWindow.__init__(self)
        observe.Observerable.__init__(self)

        self.current_sheet = current

        self.title["text"] = "Deposit"
        self.value["text"] = "Plus"

    def submit(self):
        csv_row = {
            "Date": "0",
            "Subject": "None",
            "Plus": "0",
            "Minus": "0",
            "Total": "0",
        }

        plus = self.trim_value(self.value_var.get())

        prev_total = sheet_func.read_csv(self.current_sheet)

        print(prev_total[-1][-1])

        if prev_total[-1][-1] == "Total":
             new_total = float(csv_row["Total"])
        else:
            new_total = float(prev_total[-1][-1])

        new_total += float(plus)

        csv_row["Date"] = self.date_var.get()
        csv_row["Subject"] = self.subject_var.get()
        csv_row["Plus"] = plus
        csv_row["Total"] = str(new_total)

        sheet_func.dict_write_csv(self.current_sheet, csv_row)
        self.send_signal(self.current_sheet)
        self.back()

        print("Deposited!")


class WidthdrawlWindow(PopupWindow, observe.Observerable):
    def __init__(self, main, current, observable = "observable"):
        PopupWindow.__init__(self)
        observe.Observerable.__init__(self)

        self.current_sheet = current

        self.title["text"] = "Widthdrawl"
        self.value["text"] = "Minus"

    def submit(self):
        csv_row = {
            "Date": "0",
            "Subject": "None",
            "Plus": "0",
            "Minus": "0",
            "Total": "0",
        }

        minus = self.trim_value(self.value_var.get())

        prev_total = sheet_func.read_csv(self.current_sheet)

        print(prev_total[-1][-1])

        if prev_total[-1][-1] == "Total":
             new_total = float(csv_row["Total"])
        else:
            new_total = float(prev_total[-1][-1])

        new_total -= float(minus)

        csv_row["Date"] = self.date_var.get()
        csv_row["Subject"] = self.subject_var.get()
        csv_row["Minus"] = minus
        csv_row["Total"] = str(new_total)

        sheet_func.dict_write_csv(self.current_sheet, csv_row)
        self.send_signal(self.current_sheet)
        self.back()

        print("Widthdrawn!")


class SpreadSheet(ScrolledFrame, observe.Observer):
    def __init__(self, main):
        ScrolledFrame.__init__(self)

        self.sheet_name = ""

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

                try:
                    var.delete(0, tk.END)
                    var.insert(0, csv_file[1:][y][coord])
                except IndexError:
                    pass

    def receive_signal(self, observable, value=None, *args, **kwargs):
        if value == None:
            pass
        else:
            self.sheet_name = value

        self.load_spreadsheet(value)