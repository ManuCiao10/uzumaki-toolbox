import time
import os
import csv
import threading

from handler.utils import *
from internal.security import processRunning

from payout.restock import Restock


def payoutHandler(fileName, pid):
    company_mapping = {
        "restock.csv": Restock,
    }

    try:
        company_mapping[fileName](pid)
    except KeyError:
        print_task("invalid company", RED)
        time.sleep(3)
        return


def payout(username):
    """Displays a list of tracking files and prompts the user to select one.
    For each row in the selected file, launches a new thread to handle the tracking
    for the given company."""

    processRunning()
    setTitleMode("payout")

    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print(f"{RED}{BANNER}{RESET}")

        print(
            f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n"
        )

        try:
            os.chdir(os.path.join("Uzumaki", "payout"))
        except FileNotFoundError:
            print_task("missing payout folder", RED)
            time.sleep(3)
            return

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

    with open(os.path.join("Uzumaki", "payout", file), "r") as f:
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
                pid = row[0].strip()
                if not pid:
                    print_task("invalid tracking number", RED)
                    time.sleep(3)
                    return
            except IndexError:
                print_task("invalid file", RED)
                time.sleep(3)
                return

            threading.Thread(target=payoutHandler, args=(file, pid)).start()
