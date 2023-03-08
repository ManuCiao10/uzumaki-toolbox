import ctypes
import os
import datetime
import json
from colorama import init, Fore, Back, Style
import logging
import logging
from logtail import LogtailHandler
import platform

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
VERSION = "0.0.27"

init()

LOGO = "https://media.discordapp.net/attachments/819084339992068110/1075180966349381773/logo.jpeg"
BANNER = (
    f"""
      .---.        .-----------
     /     \  __  /    ------
    / /     \(  )/    -----
   //////   ' \/ '   ---            ┏───────────────────────────────┓
  //// / // :    : ---              │    WELCOME TO UZUMAKI TOOLS   │
 // /   /  /'    '--                │ https://uzumakitools.hyper.co │
//           /..\                   │            v.%s           │
       ====UU====UU====             └───────────────────────────────┘
            ./||\.
             ''''
"""
    % VERSION
)


def banner(username):
    os.system("cls" if os.name == "nt" else "clear")

    print(Fore.RED + BANNER + Style.RESET_ALL)

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    print(
        f"\t{Back.RED}{Fore.WHITE} Select an option or type 00 for exiting {Style.RESET_ALL}\n"
    )

    print(f"\t{Fore.RED} 01 {Fore.WHITE}Redirect\tRedirect packages (Brt)")
    print(f"\t{Fore.RED} 02 {Fore.WHITE}Tracker\tOrder Tracker (Ups Brt Sda Nike)")
    print(f"\t{Fore.RED} 03 {Fore.WHITE}Geocode\tGeocode address")
    print(f"\t{Fore.RED} 04 {Fore.WHITE}Jigger\tCsv filler Jig")
    print(f"\t{Fore.RED} 05 {Fore.WHITE}Scraper\tScraper Order (New Balance Courir)")
    print(f"\t{Fore.RED} 06 {Fore.WHITE}Restock\tMissing Payout Scraper")
    print(f"\t{Fore.RED} 07 {Fore.WHITE}Email\tUnsubscriber")
    # print(f"\t{Fore.RED} 08 {Fore.WHITE}Zalando\tAccount Checker [LOCKED]")
    # print(f"\t{Fore.RED} 09 {Fore.WHITE}Redirect\tRedirect packages (Ups)")
    print(f"\t{Fore.RED} 00 {Fore.WHITE}Exit\tExit from Uzumaki Tools\n")

    option = input("\t> choose: ")
    return option


def checking():
    firstRun = False

    # ----Uzumaki----#
    if not os.path.exists("Uzumaki"):
        print_task("creating folder Uzumaki...", PURPLE)
        print_task("Uzumaki created", GREEN)
        os.makedirs("Uzumaki")

        firstRun = True

    directories = [
        "Uzumaki/tracker",
        "Uzumaki/redirect",
        "Uzumaki/geocode",
        "Uzumaki/jigger",
        "Uzumaki/scraper",
        "Uzumaki/restock",
        "Uzumaki/unsubscriber",
        # "Uzumaki/zalando",
    ]

    for directory in directories:
        if not os.path.exists(directory):
            print_task(directory + " created", GREEN)
            os.makedirs(directory)

    # ----settings.json----#
    setting = {"webhook": "WEBHOOK HERE", "key": "KEY HERE"}

    if not os.path.exists("Uzumaki/settings.json"):
        with open("Uzumaki/settings.json", "w") as f:
            json.dump(setting, f, indent=2)
            print_task("settings.json created", GREEN)

    # ----credentials.json----#

    credentials = {
        "userGmail": "",
        "passwordGmail": "",
        "userRestock": "",
        "passwordRestock": "",
    }

    if not os.path.exists("Uzumaki/restock/credentials.json"):
        with open("Uzumaki/restock/credentials.json", "w") as f:
            json.dump(credentials, f, indent=2)
            print_task("credentials.json created", GREEN)

    # ----tracker----#

    if not os.path.exists("Uzumaki/tracker/nike.csv"):
        with open("Uzumaki/tracker/nike.csv", "w") as f:
            f.write("orderNumber,email")
            print_task("nike.csv created", GREEN)
            f.close()

    if not os.path.exists("Uzumaki/tracker/brt.csv"):
        with open("Uzumaki/tracker/brt.csv", "w") as f:
            f.write("tracking_number")
            print_task("brt.csv created", GREEN)
            f.close()

    if not os.path.exists("Uzumaki/tracker/ups.csv"):
        with open("Uzumaki/tracker/ups.csv", "w") as f:
            f.write("tracking_number")
            f.close()

    if not os.path.exists("Uzumaki/tracker/sda.csv"):
        with open("Uzumaki/tracker/sda.csv", "w") as f:
            f.write("tracking_number")
            print_task("sda.csv created", GREEN)
            f.close()

    # ----redirect----#

    # ----BRT----#
    if not os.path.exists("Uzumaki/redirect/brt_checker.csv"):
        with open("Uzumaki/redirect/brt_checker.csv", "w") as f:
            f.write("tracking_number,OrderZipcode")
            print_task("brt_checker.csv created", GREEN)
            f.close()

        if os.path.exists("Uzumaki/redirect/brt.csv"):
            os.remove("Uzumaki/redirect/brt.csv")

    if not os.path.exists("Uzumaki/redirect/brt_redirect.csv"):
        with open("Uzumaki/redirect/brt_redirect.csv", "w") as f:
            f.write("tracking_number,name,phone,address,city,state(FI),zip,email")
            print_task("brt_redirect.csv created", GREEN)
            f.close()

    # ----scraper----#

    if not os.path.exists("Uzumaki/scraper/newBalance.csv"):
        with open("Uzumaki/scraper/newBalance.csv", "w") as f:
            f.write("orderNumber,postalCode,orderLastname")
            print_task("newBalance.csv created", GREEN)
            f.close()

    if not os.path.exists("Uzumaki/scraper/courir.csv"):
        with open("Uzumaki/scraper/courir.csv", "w") as f:
            f.write("email,zipCode")
            print_task("courir.csv created", GREEN)
            f.close()

    # ----geocode----#

    if not os.path.exists("Uzumaki/geocode/geocode.csv"):
        with open("Uzumaki/geocode/geocode.csv", "w") as f:
            print_task("geocode.csv created", GREEN)
            f.write("country,zip_code")
            f.close()

        if os.path.exists("Uzumaki/geocode/geocoding.csv"):
            os.remove("Uzumaki/geocode/geocoding.csv")

    # ----Csv jig----#

    if not os.path.exists("Uzumaki/jigger/jig.csv"):
        with open("Uzumaki/jigger/jig.csv", "w") as f:
            f.write(
                "First Name,Second name,Mobile Number,Address,HouseNumber,country(italy)"
            )
            print_task("jig.csv created", GREEN)
            f.close()

    unsubscriber = {
        "userGmail": "",
        "passwordGmail": "",
    }

    if not os.path.exists("Uzumaki/unsubscriber/unsubscriber.json"):
        with open("Uzumaki/unsubscriber/unsubscriber.json", "w") as f:
            json.dump(unsubscriber, f, indent=2)
            print_task("unsubscriber.json created", GREEN)

    # ----zalando----#

    # if not os.path.exists("Uzumaki/zalando/accounts.csv"):
    #     with open("Uzumaki/zalando/accounts.csv", "w") as f:
    #         f.write("Email,Password")
    #         print_task("accounts.csv created", GREEN)
    #         f.close()

    if firstRun:
        print_task("folder created, check " + os.getcwd(), YELLOW)
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
    return "[Uzumaki %s] " % VERSION


def logsTailer(msg, color):
    """
    Logs a message with a color code and a timestamp.

    """
    try:
        handler = LogtailHandler(source_token="***REMOVED***")

        logger = logging.getLogger(__name__)
        logger.handlers = []

        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        logger.info(color + uzumaki() + time_task() + msg.upper() + RESET)
    except:
        pass


def print_task(msg, color):
    """
    Prints a message with a color code and a timestamp.

    Args:
        msg (str): The message to print.
        color (str): The ANSI color code to use.
    """

    print(color + uzumaki() + time_task() + msg.upper() + RESET)

    logsTailer(msg.upper(), color)


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

    path = "Uzumaki/settings.json"

    try:
        with open(path, "r") as f:
            settings = json.load(f)

    except FileNotFoundError:
        print_task("settings.json not found", RED)
        print_task("check your folder", RED)
        input("Press Enter to exit...")
        return

    except json.decoder.JSONDecodeError:
        print_task("settings.json is corrupted", RED)
        print_task("check your folder", RED)
        input("Press Enter to exit...")
        return

    return settings


def bye(username):
    """
    Prints a goodbye message and exits the program.
    """
    print_task(f"bye bye {username}...", RED)
    input("Press Enter to exit...")
    return


def validate(credentials):
    required_fields = ["userGmail", "passwordGmail"]
    for field in required_fields:
        if credentials.get(field, "").strip() == "":
            return False
    return True


country_prefix = {
    "France": "+33",
    "Italy": "+39",
    "Spain": "+34",
}


def setTitle(title):
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW(
            title + " | Uzumaki Version: " + VERSION
        )
