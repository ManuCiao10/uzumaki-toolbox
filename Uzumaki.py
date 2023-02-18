from handler.utils import *
from handler.redirect import redirect
from handler.geocode import geocode
from handler.tracker import tracker
from handler.scraper import scraper
from handler.auth import auth
import os
import time
import colorama

#https://www.remote.tools/remote-work/discord-text-formatting

def handler_option(option):
    if option == "01":
        redirect()
    elif option == "02":
        tracker()
    elif option == "03":
        geocode()
    # elif option == "04":
    #     scraper()
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
    auth()
    
    option = banner()
    handler_option(option)

# TODO:
# - add more companies and features
# - authentication
# - maybe nike-instore monitor
# - do brt only for the brt tracking instant
