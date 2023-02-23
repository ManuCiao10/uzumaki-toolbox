import os
import time
import datetime
import json
from colorama import init, Fore, Back, Style

PURPLE = "\033[95m"
CYAN = "\033[96m"
DARKCYAN = "\033[36m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
TAB = "\t"
WHITE = "\033[97m"

init()

LOGO = "https://media.discordapp.net/attachments/819084339992068110/1075180966349381773/logo.jpeg"
BANNER = f"""
      .---.        .-----------
     /     \  __  /    ------
    / /     \(  )/    -----
   //////   ' \/ '   ---            ┏───────────────────────────────┓
  //// / // :    : ---              │    WELCOME TO UZUMAKI TOOLS   │
 // /   /  /'    '--                │ https://uzumakitools.hyper.co │
//           /..\                   │           v.0.0.23            │
       ====UU====UU====             └───────────────────────────────┘
            ./||\.
             ''''
"""


def banner(username):
    print(Fore.RED + BANNER + Style.RESET_ALL)

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    print(
        f"\t{Back.RED}{Fore.WHITE} Select an option or type 00 for exiting {Style.RESET_ALL}\n"
    )

    print(f"\t{Fore.RED} 01 {Fore.WHITE}Redirect\tRedirect packages (Brt)")
    print(f"\t{Fore.RED} 02 {Fore.WHITE}Tracker\tOrder Tracker (Ups Brt Sda Nike)")
    print(f"\t{Fore.RED} 03 {Fore.WHITE}Geocode\tGeocode address")
    print(f"\t{Fore.RED} 04 {Fore.WHITE}Csv\t\tCsv filler Jig")
    print(f"\t{Fore.RED} 05 {Fore.WHITE}Scraper\tScraper Order (New Balance)")
    print(f"\t{Fore.RED} 06 {Fore.WHITE}Restock\tMissing Payout Scraper")
    print(f"\t{Fore.RED} 00 {Fore.WHITE}Exit\tExit from Uzumaki Tools\n")

    option = input("\t> choose: ")
    return option


def checking():
    firstRun = False

    # ----Uzumaki----#
    if not os.path.exists("Uzumaki"):
        print_task("creating folder Uzumaki...", GREEN)
        os.makedirs("Uzumaki")

        firstRun = True

    directories = [
        "Uzumaki/tracker",
        "Uzumaki/redirect",
        "Uzumaki/geocode",
        "Uzumaki/jigger",
        "Uzumaki/scraper",
        "Uzumaki/restock",
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # ----settings.json----#

    if not os.path.exists("Uzumaki/settings.json"):
        with open("Uzumaki/settings.json", "w") as f:
            f.write('{\n  "webhook": "WEBHOOK HERE",\n  "key": "KEY HERE"\n}')
            f.close()

    # ----credentials.json----#
    if not os.path.exists("Uzumaki/restock/credentials.json"):
        with open("Uzumaki/restock/credentials.json", "w") as f:
            f.write(
                '{\n  "userGmail": "userGmail here",\n  "passwordGmail": "passwordGmail here", \n\n  "userRestock": "userRestock here",\n  "passwordRestock": "passwordRestock here"\n}'
            )
            f.close()

    # ----tracker----#

    if not os.path.exists("Uzumaki/tracker/nike.csv"):
        with open("Uzumaki/tracker/nike.csv", "w") as f:
            f.write("orderNumber,email")
            f.close()

    if not os.path.exists("Uzumaki/tracker/brt.csv"):
        with open("Uzumaki/tracker/brt.csv", "w") as f:
            f.write("tracking_number")
            f.close()

    if not os.path.exists("Uzumaki/tracker/ups.csv"):
        with open("Uzumaki/tracker/ups.csv", "w") as f:
            f.write("tracking_number")
            f.close()

    if not os.path.exists("Uzumaki/tracker/sda.csv"):
        with open("Uzumaki/tracker/sda.csv", "w") as f:
            f.write("tracking_number")
            f.close()

    # ----redirect----#

    if not os.path.exists("Uzumaki/redirect/brt.csv"):
        with open("Uzumaki/redirect/brt.csv", "w") as f:
            f.write(
                "tracking_number,OrderZipcode,name,phone,address,city,state(FI),zip,email"
            )
            f.close()

    # ----scraper----#
    if not os.path.exists("Uzumaki/scraper/newBalance.csv"):
        with open("Uzumaki/scraper/newBalance.csv", "w") as f:
            f.write("orderNumber,postalCode,orderLastname")
            f.close()

    # ----geocode----#

    if not os.path.exists("Uzumaki/geocode/geocoding.csv"):
        with open("Uzumaki/geocode/geocoding.csv", "w") as f:
            f.write("zip_code")
            f.close()

    # ----Csv jig----#

    if not os.path.exists("Uzumaki/jigger/jig.csv"):
        with open("Uzumaki/jigger/jig.csv", "w") as f:
            f.write(
                "First Name,Second name,Mobile Number,Address,HouseNumber,country(italy)"
            )
            f.close()

    if firstRun:
        print_task("folder created, check " + os.getcwd(), PURPLE)
        input("Press Enter to exit...")
        os._exit(1)


def time_task():
    """
    Returns the current time formatted as a string.
    """
    now = datetime.datetime.now()
    return "[" + now.strftime("%H:%M:%S:%f") + "] "


def uzumaki():
    """
    Returns the name and version number of the program as a string.
    """
    return "[Uzumaki 0.0.23] "


def print_task(msg, color):
    """
    Prints a message with a color code and a timestamp.

    Args:
        msg (str): The message to print.
        color (str): The ANSI color code to use.
    """
    print(color + uzumaki() + time_task() + msg.upper() + RESET)


def print_file(file_name):
    """
    Prints the name of a file.

    Args:
        file_name (str): The name of the file to print.
    """
    print(PURPLE + uzumaki() + time_task() + WHITE + file_name + RESET)


def load_settings():
    """
    Reads the settings from a JSON file.

    Returns:
        dict: The settings as a dictionary.
    """
    try:
        with open("Uzumaki/settings.json", "r") as settings_file:
            settings = json.load(settings_file)

    except FileNotFoundError:
        print_task("settings.json not found", RED)
        print_task("please check your folder", RED)
        time.sleep(3)
        os._exit(1)

    return settings


def bye():
    """
    Prints a goodbye message and exits the program.
    """
    print_task("bye bye...", RED)
    time.sleep(3)
    os._exit(1)
