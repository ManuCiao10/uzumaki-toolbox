from handler.utils import *
from handler.gls import gls

def redirectHandler(company, tracking_number, tkn, city, address, number_house, province, zip_code, name, surname, instructions):

    if company == "gls":
        gls(company, tracking_number, tkn, city, address, number_house,
            province, zip_code, name, surname, instructions)


def redirect():
    import csv
    import threading
    print_task("starting redirect.csv...", CYAN)
    with open("Uzumaki/redirect/redirect.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            company = row[0].lower().strip()
            tracking_number = row[1].strip()
            tkn = row[2].strip()
            city = row[3].strip()
            address = row[4].strip()
            number_house = row[5].strip()
            province = row[6].strip()
            zip_code = row[7].strip()
            name = row[8].strip()
            surname = row[9].strip()
            instructions = row[10].strip()

            threading.Thread(target=redirectHandler, args=(
                company, tracking_number, tkn, city, address, number_house, province, zip_code, name, surname, instructions)).start()
