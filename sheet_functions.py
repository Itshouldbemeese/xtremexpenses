import csv

def write_csv(name, header, sheet):
    with open(f"{name}.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(sheet)