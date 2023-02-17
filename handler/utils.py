import os

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
  //// / // :    : ---              │  WELCOME TO HUZUMAKI TOOLS    │
 // /   /  /'    '--                │      https://Uzumaki.eu       │
//           /..\                   │           v.0.0.23            │
       ====UU====UU====             └───────────────────────────────┘
            ./||\.
             ''''
"""


def banner():
    print(RED + BANNER + RESET)

    print(WHITE + "Author: " +
          RED + "@MANUCIAO|YΞ\n" + RESET)

    print('\t' + "\x1b[1;37;41m" +
          " Select an option or type exit for exiting " + "\x1b[0m" + "\n")

    print(TAB + RED + " 01 " + WHITE + "Redirect" +
          TAB + "Redirect packages (Brt)")

    # print(TAB + RED + " 02 " + WHITE + "Csv" + TAB +
    #       TAB + "Csv filler Jig ==> TO FIX")

    print(TAB + RED + " 03 " + WHITE + "Tracker" +
          TAB + "Order Tracker (Ups Brt Sda)")

    # print(TAB + RED + " 04 " + WHITE + "Scraper" +
    #       TAB + "Resell payout scraper (Goat Stockx Restock) ==> TO FIX")
    
    print(TAB + RED + " 05 " + WHITE + "Geocode" +
            TAB + "Geocode address")

    # print(TAB + RED + " 06 " + WHITE + "Checker" +
    #       TAB + "Combo list accounts (Zalando Gmail) ==> TO FIX")

    print(TAB + RED + " 00 " + WHITE + "Exit" +
          TAB + "Exit from Uzumaki Tools")

    print("\n")

    option = input(TAB + RED + ">" + WHITE + " choose: " + RESET)
    return option


def checking():

    print(PURPLE + "checking folders...")
    desktop_path = os.path.expanduser("~/Desktop")

    os.chdir(desktop_path)

    if not os.path.exists("Uzumaki"):
        print(GREEN + "creating folder Uzumaki in " +
              os.getcwd() + RESET)
        os.makedirs("Uzumaki")
        os.makedirs("Uzumaki/tracker")
        os.makedirs("Uzumaki/redirect")
        os.makedirs("Uzumaki/geocode")

        with open("Uzumaki/settings.json", "w") as f:
            f.write(
                '{\n  "webhook": "WEBHOOK HERE",\n  "key": "KEY HERE"\n}')
            f.close()

        with open("Uzumaki/tracker/tracker.csv", "w") as f:
            f.write(
                "company,tracking_number")
            f.close()

        with open("Uzumaki/tracker/ups.csv", "w") as f:
            f.write(
                "tracking_number,packageStatus,simplifiedText,streetAddress1,city,country,zipCode,attentionName")
            f.close()

        with open("Uzumaki/tracker/brt.csv", "w") as f:
            f.write(
                "tracking_number,date,time,location,status")
            f.close()

        with open("Uzumaki/redirect/redirect.csv", "w") as f:
            #add email
            f.write(
                "company(brt),tracking_number(V1698244423),OrderZipcode,name,phone,address,city,state(FI),zip,email")
            f.close()

        with open("Uzumaki/geocode/geocoding.csv", "w") as f:
            f.write(
                "zip_code")
            f.close()


def time():
    import datetime
    now = datetime.datetime.now()
    return "[" + now.strftime("%H:%M:%S") + "] "


def Uzumaki():
    return "[Uzumaki 0.0.23] "


def print_task(msg, color):
    print(color + Uzumaki() + time() + msg.upper() + RESET)


def load_settings():
    import json
    with open("Uzumaki/settings.json", "r") as f:
        settings = json.load(f)
        f.close()

    return settings
