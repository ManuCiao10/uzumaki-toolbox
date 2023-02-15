from handler.utils import *
from handler.redirect import redirect
from handler.tracker import tracker
from handler.scraper import scraper
from handler.auth import auth


def handler_option(option):
    if option == "01":
        redirect()
    elif option == "03":
        tracker()
    elif option == "04":
        scraper()
    elif option == "00":
        print_task("bye bye...", RED)
        exit()
    else:
        print_task("invalid option", RED)
        exit()


if __name__ == "__main__":
    checking()
    auth()
    option = banner()
    handler_option(option)

# TODO:
# - add more companies and features
# - compile to exe for windows
# - compile to app for mac
# - authentication
# - fix GLS
# - add scraper tracking email gls
# - maybe nike-instore monitor
