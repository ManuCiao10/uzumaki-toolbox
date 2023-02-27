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
VERSION = "0.0.25"

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
    ]

    for directory in directories:
        if not os.path.exists(directory):
            print_task(directory + "created", GREEN)
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

    if not os.path.exists("Uzumaki/redirect/brt.csv"):
        with open("Uzumaki/redirect/brt.csv", "w") as f:
            f.write(
                "tracking_number,OrderZipcode,name,phone,address,city,state(FI),zip,email"
            )
            print_task("brt.csv created", GREEN)
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

    if not os.path.exists("Uzumaki/geocode/geocoding.csv"):
        with open("Uzumaki/geocode/geocoding.csv", "w") as f:
            print_task("geocoding.csv created", GREEN)
            f.write("zip_code")
            f.close()

    # ----Csv jig----#

    if not os.path.exists("Uzumaki/jigger/jig.csv"):
        with open("Uzumaki/jigger/jig.csv", "w") as f:
            f.write(
                "First Name,Second name,Mobile Number,Address,HouseNumber,country(italy)"
            )
            print_task("jig.csv reated", GREEN)
            f.close()

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

    path = "Uzumaki/settings.json"

    try:
        with open(path, "r") as f:
            settings = json.load(f)

    except FileNotFoundError:
        print_task("settings.json not found", RED)
        print_task("please check your folder", RED)
        input("Press Enter to exit...")
        return

    except json.decoder.JSONDecodeError:
        print_task("settings.json is corrupted", RED)
        print_task("please check your folder", RED)
        input("Press Enter to exit...")
        return

    return settings


def bye():
    """
    Prints a goodbye message and exits the program.
    """
    print_task("bye bye...", RED)
    input("Press Enter to exit...")
    return


country_prefix = {
    "Afghanistan": "+93",
    "Albania": "+355",
    "Algeria": "+213",
    "Andorra": "+376",
    "Angola": "+244",
    "Antigua and Barbuda": "+1-268",
    "Argentina": "+54",
    "Armenia": "+374",
    "Australia": "+61",
    "Austria": "+43",
    "Azerbaijan": "+994",
    "Bahamas": "+1-242",
    "Bahrain": "+973",
    "Bangladesh": "+880",
    "Barbados": "+1-246",
    "Belarus": "+375",
    "Belgium": "+32",
    "Belize": "+501",
    "Benin": "+229",
    "Bhutan": "+975",
    "Bolivia": "+591",
    "Bosnia and Herzegovina": "+387",
    "Botswana": "+267",
    "Brazil": "+55",
    "Brunei": "+673",
    "Bulgaria": "+359",
    "Burkina Faso": "+226",
    "Burundi": "+257",
    "Cambodia": "+855",
    "Cameroon": "+237",
    "Canada": "+1",
    "Cape Verde": "+238",
    "Central African Republic": "+236",
    "Chad": "+235",
    "Chile": "+56",
    "China": "+86",
    "Colombia": "+57",
    "Comoros": "+269",
    "Congo, Democratic Republic of the": "+243",
    "Congo, Republic of the": "+242",
    "Costa Rica": "+506",
    "Cote d'Ivoire": "+225",
    "Croatia": "+385",
    "Cuba": "+53",
    "Cyprus": "+357",
    "Czech Republic": "+420",
    "Denmark": "+45",
    "Djibouti": "+253",
    "Dominica": "+1-767",
    "Dominican Republic": "+1-809, +1-829, +1-849",
    "East Timor (Timor-Leste)": "+670",
    "Ecuador": "+593",
    "Egypt": "+20",
    "El Salvador": "+503",
    "Equatorial Guinea": "+240",
    "Eritrea": "+291",
    "Estonia": "+372",
    "Ethiopia": "+251",
    "Fiji": "+679",
    "Finland": "+358",
    "France": "+33",
    "Gabon": "+241",
    "Gambia": "+220",
    "Georgia": "+995",
    "Germany": "+49",
    "Ghana": "+233",
    "Greece": "+30",
    "Grenada": "+1-473",
    "Guatemala": "+502",
    "Guinea": "+224",
    "Guinea-Bissau": "+245",
    "Guyana": "+592",
    "Haiti": "+509",
    "Honduras": "+504",
    "Hungary": "+36",
    "Iceland": "+354",
    "India": "+91",
    "Indonesia": "+62",
    "Iran": "+98",
    "Iraq": "+964",
    "Ireland": "+353",
    "Israel": "+972",
    "Italy": "+39",
    "Jamaica": "+1-876",
    "Japan": "+81",
    "Jordan": "+962",
}
