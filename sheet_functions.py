import csv
import os

PATH = "./sheets"


def create_directory():
    if not os.path.exists(PATH):
        os.mkdir(PATH)
        print(f"Path {PATH} created successfully!")
        return
    else:
        print(f"Path {PATH} already exists!")
        return


def write_csv(name, header, sheet):
    with open(f"{PATH}/{name.lower()}.csv", "w") as file:
        writer = csv.writer(file)

        writer.writerow(header)
        writer.writerows(sheet)


def read_csv(name):
    try:
        with open(f"{PATH}/{name.lower()}.csv", "r") as file:
            return [row for row in csv.reader(file)]
    except FileNotFoundError:
        print("UH OH")
        raise
        return