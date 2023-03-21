import imaplib
import os
import json

from handler.utils import *
from internal.kith import kith_handler
from internal.zalando import zalando_handler
from internal.snipes import snipes_handler
import time
from internal.security import processRunning


def unsubscriber(username):
    processRunning()
    setTitleMode("unsubscriber")
    try:
        os.chdir("Uzumaki/unsubscriber")
    except:
        print_task("error finding unsubscriber folder...", RED)
        time.sleep(3)
        return

    # Get credentials from file
    try:
        with open("unsubscriber.json", "r") as f:
            credentials = json.load(f)

        if not validate(credentials):
            print_task("please fill unsubscriber.json", RED)
            time.sleep(3)
            return

    except:
        print_task("error getting credentials", RED)
        time.sleep(3)
        return

    user = credentials["userGmail"]
    password = credentials["passwordGmail"]

    # connect to email
    imap_url = "imap.gmail.com"
    try:
        my_mail = imaplib.IMAP4_SSL(imap_url)
        my_mail.login(user, password)
        my_mail.select("Inbox")

    except:
        print_task("error connecting to email", RED)
        time.sleep(3)
        return

    # Define the companies and their corresponding names
    companies = {
        "01": "Kith",
        "02": "Zalando prive",
        "03": "Snipes",
    }

    # Define the handlers for each company
    handlers = {
        "01": kith_handler,
        "02": zalando_handler,
        "03": snipes_handler,
    }

    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print(f"{RED}{BANNER}{RESET}")

        print(
            f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n"
        )

        for key, value in companies.items():
            print(f"{TAB}{RED}{key}{TAB}{WHITE}{value}{RESET}")

        print("\n")
        option = input(f"{TAB}{WHITE}> Select a website: {RESET}")

        # Call the appropriate handler for the selected company
        try:
            handlers[option](my_mail)
            break
        except KeyError:
            print_task("Invalid company", RED)
            time.sleep(1)
