import ctypes
import os
import datetime
import json
from colorama import init, Fore, Back, Style
import logging
import logging
from logtail import LogtailHandler
import time

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
VERSION = "0.0.33"

init()

LOGO = "https://media.discordapp.net/attachments/819084339992068110/1083492784146743416/Screenshot_2023-03-09_at_21.53.23.png"
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

    print(RED + BANNER + Style.RESET_ALL)

    print(f"{Fore.WHITE}WELCOME BACK: {RED}{username.upper()}{Style.RESET_ALL}\n")

    print(
        f"\t{Back.RED}{Fore.WHITE} Select an option or type 00 for exiting {Style.RESET_ALL}\n"
    )

    print(f"\t{RED} 01 {Fore.WHITE}Brt\t\tRedirect packages ")
    print(f"\t{RED} 02 {Fore.WHITE}Tracker\tOrder Tracker")
    print(f"\t{RED} 03 {Fore.WHITE}Geocode\tGeocode address")
    print(f"\t{RED} 04 {Fore.WHITE}Jigger\tCsv filler Jig")
    print(f"\t{RED} 05 {Fore.WHITE}Scraper\tScraper Orders")
    print(f"\t{RED} 06 {Fore.WHITE}Restock\tMissing Payout Scraper")
    print(f"\t{RED} 07 {Fore.WHITE}Email\tUnsubscriber")
    print(f"\t{RED} 08 {Fore.WHITE}Gls\t\tRedirect packages [LOCKED]")
    print(f"\t{RED} 09 {Fore.WHITE}Schedule\tSchedule a ups pickup")
    print(f"\t{RED} 10 {Fore.WHITE}Payout\tRestock")
    print(f"\t{RED} 11 {Fore.WHITE}Quicktask\tWethenew Quicktask")
    print(f"\t{RED} 00 {Fore.WHITE}Exit\tExit from Uzumaki\n")

    option = input("\t> choose: ")
    return option


def checking():
    firstRun = False
    print_task("checking folders...", PURPLE)

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
        "Uzumaki/gls",
        "Uzumaki/pickup",
        "Uzumaki/payout",
        "Uzumaki/wethenew",
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

    if not os.path.exists("Uzumaki/tracker/dhl.csv"):
        with open("Uzumaki/tracker/dhl.csv", "w") as f:
            f.write("tracking_number")
            print_task("dhl.csv created", GREEN)
            f.close()

    if not os.path.exists("Uzumaki/tracker/gls.csv"):
        with open("Uzumaki/tracker/gls.csv", "w") as f:
            f.write("tracking_number")
            print_task("gls.csv created", GREEN)
            f.close()

    if not os.path.exists("Uzumaki/tracker/poste_nl.csv"):
        with open("Uzumaki/tracker/poste_nl.csv", "w") as f:
            f.write("tracking_number,zipcode")
            print_task("poste_nl.csv created", GREEN)
            f.close()

    if not os.path.exists("Uzumaki/tracker/correos.csv"):
        with open("Uzumaki/tracker/correos.csv", "w") as f:
            f.write("tracking_number")
            print_task("correos.csv created", GREEN)
            f.close()

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

    # ----glsRedirect----#

    if not os.path.exists("Uzumaki/gls/gls.json"):
        with open("Uzumaki/gls/gls.json", "w") as f:
            json.dump(unsubscriber, f, indent=2)
            print_task("gls.json created", GREEN)

    if not os.path.exists("Uzumaki/gls/gls.csv"):
        with open("Uzumaki/gls/gls.csv", "w") as f:
            f.write("name,surname,phone,address,city,state,zip")
            print_task("gls.csv created", GREEN)
            f.close()

    # ----upsPickup----#
    if not os.path.exists("Uzumaki/pickup/pickup_ups.csv"):
        with open("Uzumaki/pickup/pickup_ups.csv", "w") as f:
            f.write("name,surname,phone,address,city,zip,country(it),email")
            print_task("pickup_ups.csv created", GREEN)

        if os.path.exists("Uzumaki/pickup/ups.csv"):
            os.remove("Uzumaki/pickup/ups.csv")

    # ----payout----#
    if not os.path.exists("Uzumaki/payout/restock.csv"):
        with open("Uzumaki/payout/restock.csv", "w") as f:
            f.write("sku")
            print_task("restock.csv created", GREEN)

    wethenew_login = {
        "email": "",
        "password": "",
    }
    # ----wethewnew----#
    if not os.path.exists("Uzumaki/wethenew/login.json"):
        with open("Uzumaki/wethenew/login.json", "w") as f:
            json.dump(wethenew_login, f, indent=2)
            print_task("login.json created", GREEN)

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
    print(PURPLE + uzumaki() + time_task() + Fore.WHITE + file_name + RESET)


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
    time.sleep(1)
    return


def validate(credentials):
    required_fields = ["userGmail", "passwordGmail"]
    for field in required_fields:
        if credentials.get(field, "").strip() == "":
            return False
    return True


def validate_wethenew(credentials):
    required_fields = ["email", "password"]
    for field in required_fields:
        if credentials.get(field, "").strip() == "":
            return False
    return True


country_prefix = {
    "France": "+33",
    "Italy": "+39",
    "Spain": "+34",
}


def setTitleMode(mode):
    """
    Sets the title of the console window.
    """

    title = "Uzumaki | Uzumaki Version: " + VERSION + " | " + mode
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW(title)


def setTitle():
    """
    Sets the title of the console window.
    """

    title = "Uzumaki | Uzumaki Version: " + VERSION
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW(title)


def updateTitle(succes, fail):
    """
    Updates the title of the console window.
    """

    title = (
        "Uzumaki | Uzumaki Version: "
        + VERSION
        + " | "
        + "Success: "
        + str(succes)
        + " | "
        + "Failure: "
        + str(fail)
    )
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW(title)
