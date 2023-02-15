from handler.utils import print_task, CYAN, RED
from handler.ups import ups
from handler.brt import brt
from handler.sda import sda


def companyHandler(company, tracking_number):
    if company == "ups":
        ups(tracking_number)
    elif company == "brt":
        brt(tracking_number)
    elif company == "sda":
        sda(tracking_number)
    else:
        print_task("invalid company", RED)


def tracker():
    import csv
    import threading
    print_task("starting tracker.csv...", CYAN)
    with open("Uzumaki/tracker/tracker.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            company = row[0].lower().strip()
            tracking_number = row[1].strip()

            threading.Thread(target=companyHandler, args=(
                company, tracking_number)).start()
