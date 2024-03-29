import csv
import os

PATH = "./sheets"
HEADER = ["Date", "Subject", "Plus", "Minus", "Total"]

names = ["Moose", "Bryce", "Cam"]


def create_directory():
    '''
    Creates a directory for the .csv files to live.
    '''

    if not os.path.exists(PATH):
        os.mkdir(PATH)
        print(f"Path {PATH} created successfully!")

    for name in names:
        if not os.path.exists(f"{PATH}/{name.lower()}.csv"):
            with open(f"{PATH}/{name.lower()}.csv", "w") as file:
                writer = csv.writer(file)

                writer.writerow(HEADER)
    else:
        print(f"Path {PATH} already exists!")
        return


def dict_write_csv(name, row):
    check_sheet_length(name)

    with open(f"{PATH}/{name.lower()}.csv", "a+") as file:
        dict_writer = csv.DictWriter(file, fieldnames=HEADER)

        dict_writer.writerow(row)


def check_sheet_length(name):
    rows = read_csv(name)

    if len(rows) >= 32:
        with open(f"{PATH}/{name.lower()}.csv", "w") as file:
            writer = csv.writer(file)

            writer.writerow(HEADER)
            writer.writerow(rows[-1])
        return
    else:
        return

def read_csv(name):
    '''
    Reads the given .csv file and returns each row.
    '''
    try:
        with open(f"{PATH}/{name.lower()}.csv", "r") as file:
            return [row for row in csv.reader(file)]
    except FileNotFoundError:
        print("UH OH")
        raise