from handler.utils import *
from handler.redirect import redirect
from handler.geocode import geocode
from handler.tracker import tracker
from handler.scraper import scraper
from handler.auth import auth
import os
import time
import colorama


def handler_option(option):
    if option == "01":
        redirect()
    elif option == "03":
        tracker()
    elif option == "04":
        scraper()
    elif option == "05":
        geocode()
    elif option == "00":
        print_task("bye bye...", RED)
        time.sleep(1)
        os._exit(1)
    else:
        print_task("invalid option", RED)
        time.sleep(1)
        os._exit(1)


if __name__ == "__main__":
    colorama.init(wrap=True)
    checking()
    auth()
    option = banner()
    handler_option(option)

# TODO:
# - add a checekr to check when a file scraper run is empty
# - add more companies and features
# - compile to exe for windows
# - compile to app for mac
# - authentication
# - fix GLS
# - add scraper tracking email gls
# - maybe nike-instore monitor
