from handler.utils import *


def scraper():
    print(RED + BANNER + RESET)

    print(WHITE + "Author: " +
          RED + "@MANUCIAO|YΞ\n" + RESET)
    print(TAB + "\x1b[1;37;41m" +
          " Scraper usage: " + "\x1b[0m" + "\n")
    print(TAB + RED + " 01 " + WHITE + "Goat" +
          TAB + "!goat < sku > or < key words >" + RESET)

    print(TAB + RED + " 02 " + WHITE + "Restock" +
          TAB + "!restock < sku > or < key words >" + RESET)

    print("\n")
    option = input(TAB + RED + ">" + WHITE +
                   " your option (ex. !goat DZ5485-410): " + RESET)
    print(option)
