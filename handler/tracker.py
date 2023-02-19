from handler.utils import print_task, CYAN, RED
from handler.ups import ups
from handler.brt import brt
from handler.sda import sda
from handler.nike import nike
import time
import os


def companyHandler(company, tracking_number, email):
    if company == "ups":
        ups(tracking_number)
    elif company == "brt":
        brt(tracking_number)
    elif company == "sda":
        sda(tracking_number)
    elif company == "nike":
        nike(tracking_number, email)
    else:
        print_task("invalid company", RED)


def tracker():
    import csv
    import threading

    print_task("starting tracker.csv...", CYAN)
    with open("Uzumaki/tracker/tracker.csv", "r") as f:
        reader = csv.reader(f)

        try:
            next(reader)
        except StopIteration:
            print_task("file is empty", RED)
            time.sleep(2)
            os._exit(1)

        try:
            row = next(reader)
        except StopIteration:
            print_task("please fill tracker.csv", RED)
            time.sleep(2)
            os._exit(1)

        f.seek(0)
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            try:
                company = row[0].lower().strip()
                tracking_number = row[1].strip()
            except IndexError:
                print_task("company and tracking_number are required", RED)
                time.sleep(3)
                os._exit(1)
            try:
                email = row[2].strip()
            except IndexError:
                email = None

            threading.Thread(
                target=companyHandler, args=(company, tracking_number, email)
            ).start()
