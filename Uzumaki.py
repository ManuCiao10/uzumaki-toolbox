from handler.utils import *
from handler.redirect import redirect
from handler.geocode import geocode
from handler.tracker import tracker
from handler.auth import auth
from handler.jigger import jigger
from handler.scraperOrder import scraperOrder
from handler.presence import reachPresence
from handler.restock import restockPayout
import time
import colorama


def handler_option(option):
    if option == "01":
        redirect()
    elif option == "02":
        tracker()
    elif option == "03":
        geocode()
    elif option == "04":
        jigger()
    elif option == "05":
        scraperOrder()
    elif option == "06":
        restockPayout()
    elif option == "00":
        print_task("bye bye...", RED)
        time.sleep(2)
        os._exit(1)
    else:
        print_task("invalid option", RED)
        time.sleep(2)
        os._exit(1)


if __name__ == "__main__":
    colorama.init(wrap=True)

    checking()
    username = auth()
    reachPresence(username)

    option = banner(username)
    handler_option(option)


# ups redirect => opt bot
# courir checker
# twitter account

# scraper SKU nike
# zalando account checker
# price checker goat stock
# revolut Business
# bot directly on discord
