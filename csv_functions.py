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
            with open(f"{PATH}/{name.lower()}.csv", "w") as file:
                writer = csv.writer(file)

                writer.writerow(HEADER)
        return
    else:
        print(f"Path {PATH} already exists!")
        return


def write_csv(name, header, sheet):
    '''
    Creates a .csv file and updates it with current values.
    name = name of person and file. Example: moose.csv
    '''

    with open(f"{PATH}/{name.lower()}.csv", "w") as file:
        writer = csv.writer(file)

        writer.writerow(header)
        writer.writerows(sheet)


def dict_write_csv(name, row):
    with open(f"{PATH}/{name.lower()}.csv", "a+") as file:
        dict_writer = csv.DictWriter(file, fieldnames=HEADER)

        dict_writer.writerow(row)


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
        return


def return_column(name, column):
    with open(f"{PATH}/{name.lower()}.csv", "r") as file:
        column = [row[column] for row in csv.reader(file)][1:]
        return column