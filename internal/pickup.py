from handler.utils import *
from internal.security import processRunning
import csv
import threading


def pickup(username):
    processRunning()
    setTitlePickup()
    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")


    #reading csv file and get the info
    #book a pickup ups
    try:
        with open("Uzumaki/pickup/ups.csv", "r") as f:
            reader = csv.reader(f)

            try:
                next(reader)
            except StopIteration:
                print_task("file is empty, delete it.", RED)
                time.sleep(3)
                os._exit(1)

            try:
                row = next(reader)
            except StopIteration:
                print_task("please fill Uzumaki/pickup/ups.csv", RED)
                input("Press Enter to exit...")
                os._exit(1)

            f.seek(0)
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                print(row)
                # country = row[0].lower().strip()
                # zip_code = row[1].lower().strip()

                # threading.Thread(
                #     target=geocode_handler, args=(country, zip_code)
                # ).start()

    except FileNotFoundError:
        print_task("Uzumaki/geocode/geocode.csv not found", RED)
        input("Press Enter to exit...")
        return