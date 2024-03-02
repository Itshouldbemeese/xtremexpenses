from tkinter import *
from tkinter import ttk

from window import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, window_size
from styles import FONT_MAIN

x_axis_labels = ["Date", "Subject", "Plus", "Minus", "Total"]


root = Tk()
root.title(WINDOW_TITLE)
root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(window_size(screen_width, screen_height))

entry = StringVar()

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

sheet_one = ttk.Frame(tabs)
sheet_two = ttk.Frame(tabs)

# Date
sheet_one.columnconfigure(0, weight=1)
# Subject
sheet_one.columnconfigure(1, weight=2)
# Plus
sheet_one.columnconfigure(2, weight=1)
# Minus
sheet_one.columnconfigure(3, weight=1)
# Running total
sheet_one.grid_columnconfigure(0, weight=1)
sheet_one.rowconfigure(0, weight=1)

for i, label in enumerate(x_axis_labels):
    text = Label(sheet_one, text=label)
    text.grid(column=i, row=0, sticky=NW)

tabs.add(sheet_one, text="Moose")
tabs.add(sheet_two, text="Bryce")

root.mainloop()