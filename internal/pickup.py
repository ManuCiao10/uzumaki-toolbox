from handler.utils import *
from internal.security import processRunning


def pickup(username):
    processRunning()
    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    #reading csv file and get the info
    #book a pickup ups