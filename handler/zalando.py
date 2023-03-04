import os
from handler.utils import *
import csv
import time
import threading

zalandoAPI = "rRo4r3bdjx5uPqcoZq8lo4b4ZoJtNG4B2ZG7I9Hx"

def zalandoHandler(username):
    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    try:
        with open("Uzumaki/zalando/accounts.csv") as f:
            reader = csv.reader(f)

            try:
                next(reader)
            except StopIteration:
                print_task("file is empty", RED)
                time.sleep(3)
                return

            try:
                row = next(reader)
            except StopIteration:
                print_task(f"Please Fill Uzumaki/zalando/accounts.csv", RED)
                time.sleep(3)
                return

            f.seek(0)
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                email = row[0].strip()
                password = row[1].strip()

                try:
                    threading.Thread(target=zalando, args=(email, password)).start()
                except:
                    print_task("Error starting tasks", RED)
                    input("Press enter to exit...")
                    return

    except FileNotFoundError:
        print_task("file accounts.csv not found", RED)
        input("Press Enter to exit...")
        return


def zalando(email, password):
    print_task(f"Checking {email}:{password}", PURPLE)
    # login
    # add to cart

    
