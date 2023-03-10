from handler.utils import *
from handler.redirect import redirect
from handler.geocode import geocode
from handler.tracker import tracker
from handler.auth import auth, update
from handler.jigger import jigger
from handler.scraperOrder import scraperOrder
from handler.presence import reachPresence
from handler.restock import restockPayout
from handler.unsubscriber import unsubscriber
from handler.gls import glsRedirect

from internal.security import processRunning
from internal.pickup import pickup

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
    "00": bye,
    # "08": zalandoHandler,
    # "09": ups,
}


def main():
    colorama.init(wrap=True)

    update()
    checking()
    processRunning()
    username = auth()
    reachPresence(username)
    setTitle()

    while True:
        option = banner(username)
        try:
            OPTIONS[option](username)
            break
        except KeyError:
            print_task("invalid option ", RED)
            time.sleep(2)


if __name__ == "__main__":
    main()


# --------TO-IMPLEMENT-----------
# ups redirect => call bot
# zalando account checker
# dhl tracker using their API
# ups programma un ritiro

# --------TO-FIX-----------
# gls redirect by reading the email

# --------DISCORD-TOOL-----------
# nike scraper with pid
# restock and goat stockx scraper
