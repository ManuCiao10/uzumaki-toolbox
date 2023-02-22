import os
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
LOGO = "https://media.discordapp.net/attachments/819084339992068110/1075180966349381773/logo.jpeg"

BANNER = """
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
    print(RED + BANNER + RESET)

    print(WHITE + "WELCOME BACK: " + RED + username.upper() + RESET)
    print("\n")

    print(
        "\t"
        + "\x1b[1;37;41m"
        + " Select an option or type 00 for exiting "
        + "\x1b[0m"
        + "\n"
    )

    print(TAB + RED + " 01 " + WHITE + "Redirect" + TAB + "Redirect packages (Brt)")

    print(
        TAB
        + RED
        + " 02 "
        + WHITE
        + "Tracker"
        + TAB
        + "Order Tracker (Ups Brt Sda Nike)"
    )

    # print(TAB + RED + " 04 " + WHITE + "Scraper" +
    #       TAB + "Resell payout scraper (Goat Stockx Restock) ==> TO FIX")

    print(TAB + RED + " 03 " + WHITE + "Geocode" + TAB + "Geocode address")
    print(TAB + RED + " 04 " + WHITE + "Csv" + TAB + TAB + "Csv filler Jig")
    print(TAB + RED + " 05 " + WHITE + "Scraper" + TAB + "Scraper Order (New Balance)")

    # print(TAB + RED + " 06 " + WHITE + "Checker" +
    #       TAB + "Combo list accounts (Zalando Gmail) ==> TO FIX")

    print(TAB + RED + " 00 " + WHITE + "Exit" + TAB + "Exit from Uzumaki Tools")

    print("\n")

    option = input(TAB + "> choose: ")
    return option


def checking():
    firstRun = False

    if not os.path.exists("Uzumaki"):
        print_task("creating folder Uzumaki...", GREEN)
        os.makedirs("Uzumaki")

        firstRun = True

    if not os.path.exists("Uzumaki/tracker"):
        os.makedirs("Uzumaki/tracker")

    if not os.path.exists("Uzumaki/redirect"):
        os.makedirs("Uzumaki/redirect")

    if not os.path.exists("Uzumaki/geocode"):
        os.makedirs("Uzumaki/geocode")

    if not os.path.exists("Uzumaki/jigger"):
        os.makedirs("Uzumaki/jigger")

    if not os.path.exists("Uzumaki/scraper"):
        os.makedirs("Uzumaki/scraper")

    # ----settings.json----#

    if not os.path.exists("Uzumaki/settings.json"):
        with open("Uzumaki/settings.json", "w") as f:
            f.write('{\n  "webhook": "WEBHOOK HERE",\n  "key": "KEY HERE"\n}')
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
        print_task("folder created, check " + os.getcwd() , PURPLE)
        time.sleep(5)
        os._exit(1)


def timeTask():
    import datetime

    now = datetime.datetime.now()
    return "[" + now.strftime("%H:%M:%S:%f") + "] "


def Uzumaki():
    return "[Uzumaki 0.0.23] "


def print_task(msg, color):
    print(color + Uzumaki() + timeTask() + msg.upper() + RESET)


def print_file(file):
    print(PURPLE + Uzumaki() + timeTask() + WHITE + file + RESET)


def load_settings():
    import json

    try:
        with open("Uzumaki/settings.json", "r") as f:
            settings = json.load(f)
            f.close()
    except:
        print_task("settings.json not found", RED)
        print_task("please check your folder", RED)
        time.sleep(3)
        os._exit(1)

    return settings
