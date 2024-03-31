# XtremeXpenses[^1]

---
## About

A basic expenses tracking app built from the ground up with Python's Tkinter[^2] and the TTKBootstrap framework.

Built using such technologies as I've wanted to try my hand at Tkinter for some time now, and wanted to keep things as lightweight as possible, adding TTKBootstrap reluctantly towards the end to try and make things look a *little* better.

---
## Features

* Allows depositing and widthdrawing funds into seperate accounts.
* Saves those files externally from the App into the human readable .csv file format, also preserving them between versions.
* Ignores `+` and `-` operands when inputting balance values.
* Completes mathematical operations when a new widthdrawl or deposit action is used.

---
## # TODO

- [ ] Ability to make new accounts
- [ ] Better rounding for numbers
- [ ] Change spacing for columns
- [ ] User preferences
- [ ] Add operands to the front of values

---
## Installing

> [!TIP]
> It is highly recommened to use a virtual environment when doing anything with Python dependencies!

1. Copy down the repo into your IDE of choice.
2. In a terminal window, run `pip3 install -r requirements.txt`
3. After the dependencies have been installed, run `python3 setup.py py2app`
4. You should now have a brand new, shiny expenses tracker to keep an eye on your coffers, congrats!


## Examples

|Date      |Subject         |Plus |Minus |Total |
|----------|----------------|-----|------|------|
|2024/03/07|Unicorn Overlord|+0.00|-66.00|140.00|


[^1]: Name was chosen by my Mom.
[^2]: *(I pronounce it Kinter)*