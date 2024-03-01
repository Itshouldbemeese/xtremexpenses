from tkinter import *
from tkmacosx import Button

from window import WINDOW_TITLE, window_size
from styles import FONT_MAIN

root = Tk()
root.title(WINDOW_TITLE)

entry = StringVar()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(window_size(screen_width, screen_height))
root.resizable(False, False)

greeting = Label(
    root, 
    text="Howdy bitches!",
    font=FONT_MAIN
).pack()

text_entry = Entry(root, textvariable=entry).pack()

quit_button = Button(
    root,
    text="Quit Program",
    command=lambda: root.quit()
).pack()

root.mainloop()