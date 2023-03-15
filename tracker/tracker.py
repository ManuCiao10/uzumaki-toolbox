from handler.utils import *
from tracker.ups import ups
from tracker.brt import brt
from tracker.sda import sda
from tracker.nike import nike
from tracker.dhl import dhl
from tracker.gls import gls
from tracker.poste import poste
from tracker.correos import correos
import time
import os
import csv
import threading
from internal.security import processRunning


def companyHandler(fileName, tracking_number, email):
    company_mapping = {
        "ups.csv": ups,
        "brt.csv": brt,
        "sda.csv": sda,
        "dhl.csv": dhl,
        "gls.csv": gls,
        "correos.csv": correos,
    }

    nike_mapping = {
        "nike.csv": nike,
        "poste_nl.csv": poste,
    }

    try:
        company_mapping[fileName](tracking_number)
    except KeyError:
        try:
            nike_mapping[fileName](tracking_number, email)
        except KeyError:
            print_task("invalid company", RED)
            time.sleep(3)
            return


def tracker(username):
    processRunning()
    setTitleMode("tracker")
    """Displays a list of tracking files and prompts the user to select one.
    For each row in the selected file, launches a new thread to handle the tracking
    for the given company."""

    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print(f"{RED}{BANNER}{RESET}")

        print(
            f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n"
        )

        os.chdir(os.path.join("Uzumaki", "tracker"))
        files = os.listdir()
        os.chdir(os.path.join("..", ".."))

        files_dict = {}

        for index, file in enumerate(files):
            print_file(f"{index}. {file}")

            files_dict[str(index)] = file

        print("\n")
        option = input(f"{TAB}> choose: ")

        try:
            file = files_dict[option]
            break
        except KeyError:
            print_task("invalid option", RED)
            time.sleep(1)

    with open(os.path.join("Uzumaki", "tracker", file), "r") as f:
        reader = csv.reader(f)

        try:
            next(reader)
        except StopIteration:
            print_task("file is empty", RED)
            time.sleep(2)
            return

        try:
            row = next(reader)
        except StopIteration:
            print_task(f"please fill {file}", RED)
            time.sleep(3)
            return

        f.seek(0)
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            try:
                tracking_number = row[0].strip()
                if not tracking_number:
                    print_task("invalid tracking number", RED)
                    time.sleep(3)
                    return
            except IndexError:
                print_task("invalid file", RED)
                time.sleep(3)
                return
            try:
                email = row[1].strip()
            except IndexError:
                email = ""

            threading.Thread(
                target=companyHandler, args=(file, tracking_number, email)
            ).start()
