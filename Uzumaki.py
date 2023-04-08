from handler.utils import *
from handler.redirect import redirect
from handler.geocode import geocode
from handler.auth import update, authWhop
from handler.jigger import jigger
from handler.scraperOrder import scraperOrder
from handler.presence import reachPresence
from handler.restock import restockPayout
from handler.unsubscriber import unsubscriber
from handler.gls import glsRedirect
from handler.dhlRedirect import dhlRedirect

from tracker.tracker import tracker
from internal.security import processRunning
from internal.pickup import pickup

from proxy.proxy import proxy
from payout.payout import payout
from monitor.wethenew import wethenew
from multiprocessing import freeze_support
from generator.outlook import Inizialize
from generator.yahoo import yahoo

import colorama

OPTIONS = {
    "01": redirect,
    "02": tracker,
    "03": geocode,
    "04": jigger,
    "05": scraperOrder,
    "06": restockPayout,
    "07": unsubscriber,
    "08": glsRedirect,
    "09": pickup,
    "10": payout,
    "11": wethenew,
    "12": proxy,
    "13": dhlRedirect,
    "14": Inizialize,
    "15": yahoo,
    # "16": gmail,
    "00": bye,
}


def main():
    colorama.init(wrap=True)

    # update()
    # checking()
    # processRunning()
    # username = auth()
    username = authWhop()
    # reachPresence(username)
    # setTitle()
    # username = "dev"

    while True:
        option = banner(username)
        try:
            OPTIONS[option](username)
            break
        except KeyError:
            print_task("invalid option", RED)
            time.sleep(0.5)


if __name__ == "__main__":
    freeze_support()
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        print_task("Key Interrupt", YELLOW)
        exit_program()


# ----monitor----#
# -freebies-#
# -nike-#
# -kith-#
# -ticketmaster-#
# -wethenew-#
# -ssense-#

# ----generator----#
# -gmail-#
# -yahoo-#
# -icloud-#

# ----platform----#
# -MacOs-#

# ----dashboard----#
# -ChangeDashboard-#

# fix security bot stuff
