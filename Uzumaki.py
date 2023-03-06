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
from handler.zalando import zalandoHandler


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
    "08": zalandoHandler,
    "00": bye,
}


def main():
    colorama.init(wrap=True)

    # update()
    # checking()
    # username = auth()
    # reachPresence(username)
    username = "dev"

    while True:
        option = banner(username)

        try:
            OPTIONS[option](username)
            break
        except KeyError:
            print_task("invalid option", RED)
            time.sleep(2)


if __name__ == "__main__":
    main()


# add logs
# ups redirect => opt bot
# restock and goat scraper
# zalando account checker
# gls redirect
# nike scraper with pid
# zalando scraper
