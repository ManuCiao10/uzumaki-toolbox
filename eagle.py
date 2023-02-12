PURPLE = "\033[95m"
CYAN = "\033[96m"
DARKCYAN = "\033[36m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
TAB = "\t"
WHITE = "\033[97m"


BANNER = """
      .---.        .-----------
     /     \  __  /    ------
    / /     \(  )/    -----
   //////   ' \/ '   ---            ┏───────────────────────────────┓
  //// / // :    : ---              │     WELCOME TO EAGLE TOOLS    │
 // /   /  /'    '--                │      https://eaglebot.eu      │
//           /..\                   │           v.0.0.23            │
       ====UU====UU====             └───────────────────────────────┘
            ./||\.
             ''''
"""


def checking():
    print(PURPLE + "checking folders...")

    import os
    if not os.path.exists("eagleTools"):
        print(GREEN + "creating folder eagleTools...")
        os.makedirs("eagleTools")
        os.makedirs("eagleTools/tracker")
        os.makedirs("eagleTools/modules")
        os.makedirs("eagleTools/redirect")

        with open("eagleTools/tracker/tracker.csv", "w") as f:
            f.write(
                "company,tracking_number")
            f.close()

        with open("eagleTools/redirect/redirect.csv", "w") as f:
            f.write(
                "company,tracking_number,name,phone,address,city,state,zip,country")
            f.close()


def banner():
    print(RED + BANNER + RESET)

    print(WHITE + "Author: " +
          RED + "@MANUCIAO|YΞ\n" + RESET)

    print(TAB + "\x1b[1;37;41m" +
          " Select an option or type exit for exiting " + "\x1b[0m" + "\n")

    print(TAB + RED + " 01 " + WHITE + "Redirect" +
          TAB + "Redirect packages ups dhl")

    print(TAB + RED + " 02 " + WHITE + "Csv" + TAB +
          TAB + "Csv filler Jig")

    print(TAB + RED + " 03 " + WHITE + "Tracker" +
          TAB + "Order Tracker ups dhl")

    print(TAB + RED + " 04 " + WHITE + "Modules" +
          TAB + "Modules Nike Adidas")

    print(TAB + RED + " 00 " + WHITE + "Exit" +
          TAB + "Exit from Eagle Tools")

    print("\n")

    option = input(TAB + RED + ">" + WHITE + " choose: " + RESET)
    return option


def time():
    import datetime
    now = datetime.datetime.now()
    return "[" + now.strftime("%H:%M:%S") + "] "


def eagle():
    return "[EagleTool 0.0.23] "


def print_task(msg, color):
    print(color + eagle() + time() + msg.upper() + RESET)


def ups(tracking_number):
    print_task("checking <|%s|>..." % tracking_number, YELLOW)


def tracker():
    import csv
    print_task("starting tracker.csv...", PURPLE)
    with open("eagleTools/tracker/tracker.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            company = row[0].lower().strip()
            tracking_number = row[1].strip()
            if company == "ups":
                ups(tracking_number)
            # elif company == "dhl":
            #     from modules.tracker import dhl
            #     dhl(tracking_number)
            else:
                print_task("invalid company", RED)
                exit()


def handler_option(option):
    if option == "03":
        # from modules.redirect import redirect
        tracker()
    elif option == "00":
        exit()
    else:
        print(RED + "Invalid option" + RESET)
        exit()


if __name__ == "__main__":
    checking()

    option = banner()
    handler_option(option)
