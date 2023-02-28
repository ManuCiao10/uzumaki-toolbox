from handler.utils import *
from handler.redirect import redirect
from handler.geocode import geocode
from handler.tracker import tracker
from handler.auth import auth, update
from handler.jigger import jigger
from handler.scraperOrder import scraperOrder
from handler.presence import reachPresence
from handler.restock import restockPayout

import time
import colorama


OPTIONS = {
    "01": redirect,
    "02": tracker,
    "03": geocode,
    "04": jigger,
    "05": scraperOrder,
    "06": restockPayout,
    "00": bye,
}


def handler_option(option):
    try:
        OPTIONS[option]()
    except KeyError:
        print_task("invalid option", RED)
        time.sleep(3)
        os._exit(1)


def main():
    colorama.init(wrap=True)

    update()
    checking()
    username = auth()
    reachPresence(username)

    option = banner(username)
    handler_option(option)


if __name__ == "__main__":
    main()


# ups redirect => opt bot

# scraper SKU nike
# zalando account checker
# price checker goat stock
# revolut Business
