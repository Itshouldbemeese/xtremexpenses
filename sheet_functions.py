import csv
import os

PATH = "./sheets"


def create_directory():
    '''
    Creates a directory for the .csv files to live.
    '''

    if not os.path.exists(PATH):
        os.mkdir(PATH)
        print(f"Path {PATH} created successfully!")
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