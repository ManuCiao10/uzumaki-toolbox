from handler.utils import *
from handler.redirect import redirect
from handler.geocode import geocode
from handler.tracker import tracker
from handler.scraper import scraper
from handler.auth import auth
import time
import colorama


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
    username = auth()

    option = banner(username)
    handler_option(option)

# TODO:
# - add dhl tracker
# - auto update
