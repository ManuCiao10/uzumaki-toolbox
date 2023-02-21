from handler.utils import *
from handler.ups import ups
from handler.brt import brt
from handler.sda import sda
from handler.nike import nike
import time
import os
import csv
import threading


def companyHandler(fileName, tracking_number, email):
    if fileName == "ups.csv":
        ups(tracking_number)
    elif fileName == "brt.csv":
        brt(tracking_number)
    elif fileName == "sda.csv":
        sda(tracking_number)
    elif fileName == "nike.csv":
        nike(tracking_number, email)
    else:
        print_task("invalid company", RED)


def tracker():
    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

    os.chdir("Uzumaki/tracker")
    files = os.listdir()
    os.chdir("../..")

    files_dict = {}

    for index, file in enumerate(files):
        print_file(str(index) + ". " + file)

        files_dict[str(index)] = file

    print("\n")
    option = input(TAB + "> choose: ")

    try:
        file = files_dict[option]
    except KeyError:
        print_task("invalid option", RED)
        time.sleep(3)
        os._exit(1)

    with open("Uzumaki/tracker/" + file, "r") as f:
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
            print_task("please fill " + file, RED)
            time.sleep(2)
            os._exit(1)

        f.seek(0)
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            try:
                tracking_number = row[0].strip()
            except IndexError:
                print_task("tracking/orderNumber are required", RED)
                time.sleep(3)
                os._exit(1)
            try:
                email = row[1].strip()
            except IndexError:
                email = ""

            threading.Thread(
                target=companyHandler, args=(file, tracking_number, email)
            ).start()
