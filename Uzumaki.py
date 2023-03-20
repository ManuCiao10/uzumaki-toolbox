from handler.utils import *
from handler.redirect import redirect
from handler.geocode import geocode
from tracker.tracker import tracker
from handler.auth import auth, update
from handler.jigger import jigger
from handler.scraperOrder import scraperOrder
from handler.presence import reachPresence
from handler.restock import restockPayout
from handler.unsubscriber import unsubscriber
from handler.gls import glsRedirect

from internal.security import processRunning
from internal.pickup import pickup

from payout.payout import payout
from monitor.wethenew import wethenew

import colorama
import time

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
    "00": bye,
}


def main():
    colorama.init(wrap=True)

    # update()
    checking()
    # processRunning()
    # username = auth()
    # reachPresence(username)
    # setTitle()
    username = "dev"

    while True:
        option = banner(username)
        try:
            OPTIONS[option](username)
            break
        except KeyError:
            print_task("invalid option ", RED)
            time.sleep(1)


if __name__ == "__main__":
    main()


# --------TO-IMPLEMENT-----------
# loopback-ip-address
# macOs Version
# goat stockx scraper

# --------TO-FIX-----------
# gls redirect by reading the email
