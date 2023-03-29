import csv
import threading
import requests
from bs4 import BeautifulSoup

from handler.utils import *
from urllib.parse import urlparse
from urllib.parse import parse_qs
from internal.security import processRunning


def glsRedirect(username):
    # processRunning()
    setTitleMode("Redirect GLS")

    print_task("module is locked", YELLOW)
    time.sleep(3)
    return

    os.system("cls" if os.name == "nt" else "clear")

    print(f"{RED}{BANNER}{RESET}")

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    try:
        with open("Uzumaki/redirect_gls/redirect.csv", "r") as f:
            reader = csv.reader(f)

            try:
                next(reader)
            except StopIteration:
                print_task("file redirect_gls/redirect.csv is empty", RED)
                exit_program()

            try:
                row = next(reader)
            except StopIteration:
                print_task("please fill Uzumaki/redirect_gls/redirect.csv", RED)
                exit_program()

            f.seek(0)
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                threading.Thread(
                    target=GLSRedirect,
                    args=(
                        {
                            "url": row[0].strip(),
                            "index": reader.line_num - 1,
                            "access_point": row[1].strip(),
                            "zipcode": row[2].strip(),
                            "countryCode": row[3].strip().upper(),
                        },
                    ),
                ).start()

    except FileNotFoundError:
        print_task("Uzumaki/redirect_gls/redirect.csv not found", RED)
        time.sleep(3)
        return


class GLSRedirect:
    def __init__(self, kwargs):
        self.prefix = "https://gls-italy.com/flexdelivery?"
        self.url = kwargs["url"]
        self.index = kwargs["index"]
        self.access_point = kwargs["access_point"]
        self.zipcode = kwargs["zipcode"]
        self.countryCode = kwargs["countryCode"]

        self.check_input()

    def check_input(self):
        try:
            if not self.url.startswith(self.prefix):
                print_task(f"[{self.index}] url must start with {self.prefix}", RED)
                time.sleep(2)
                return
        except:
            print_task(f"[{self.index}] error getting url", RED)
            time.sleep(2)
            return

        parsed_url = urlparse(self.url)
        try:
            if not parsed_url.query:
                print_task(f"[{self.index}] url must have query", RED)
                time.sleep(2)
                return
        except:
            print_task(f"[{self.index}] url must have query", RED)
            time.sleep(2)
            return

        try:
            self.tkn = parse_qs(parsed_url.query)["tkn"][0]
            self.loc = parse_qs(parsed_url.query)["loc"][0]
            self.num = parse_qs(parsed_url.query)["num"][0]
        except:
            print_task(f"[{self.index}] url must have [tkn] [loc] [num]", RED)
            time.sleep(2)
            return

        self.checker()

    def checker(self):
        """
        check if redirect is possible or not
        """

        print_task(f"[{self.index}] checking...", WHITE)

        session = requests.Session()

        session.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,it;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51",
            "sec-ch-ua": '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
        }

        params = {
            "option": "com_gls",
            "view": "svincola",
            "mode": "flexdelivery",
            "firstspirit": "5",
            "loc": self.loc,
            "num": self.num,
            "tkn": self.tkn,
        }

        try:
            response = session.get("https://gls-italy.com/index.php", params=params)
        except:
            print_task(f"[{self.index}] error getting session", RED)
            time.sleep(2)
            return

        if (
            "Choose a pick-up point between GLS Depot and Parcel Shop"
            not in response.text
        ):
            print_task(f"[{self.index}] redirect not possible", RED)
            time.sleep(2)
            return

        self.redirect()

    def redirect(self):
        """
        the access point is given by the user
        check if the access point is available

        if available, redirect

        """
        print_task(f"[{self.index}] getting session...", PURPLE)

        data = {
            "option": "com_gls",
            "view": "svincola",
            "mode": "flexdelivery_sedeshop_compila",
            "loc": self.loc,
            "num": self.num,
            "tkn": self.tkn,
            "svinm": "",
            "postback": "",
            "svincolo_pre_post": "OKPRE",
        }
        try:
            response = requests.post(
                "https://gls-italy.com/index.php?option=com_gls&amp;lang=it", data=data
            )
        except:
            print_task(f"[{self.index}] error while getting session", RED)
            time.sleep(2)
            return

        bs4 = BeautifulSoup(response.text, "html.parser")
        divs = bs4.find_all("div", {"class": "col-dati"})
        for div in divs:
            print(div.text)


# data = {
#     "option": "com_gls",
#     "view": "svincola",
#     "mode": "flexdelivery_sedeshop_controlla",
#     "loc": "V1",
#     "num": "630225014",
#     "tkn": "pzYbpacv",
#     "backcontrollo": "si",
#     "destinatario": "coffeespecialist",
#     "indirizzo": "via capo di mondo, n. 22/R",
#     "cap": "50136",
#     "localita": "firenze",
#     "provincia": "FI",
#     "destinatario_originale": "emanuele  ardinghi",
#     "anagrafica_sede_punto_shop": "coffeespecialist - via capo di mondo, n. 22/R - 50136 firenze (FI)",
#     "tiposvin": "Shop",
#     "svinm": "",
#     "postback": "",
#     "parcel_shop_id": "18220",
#     "partner_shop_id": "PRP_IT",
#     "barcode": "V1630225014010T1",
#     "email_notifica": "emanuele.ardinghi@gmail.com",
#     "cellulare_notifica": "",
#     "bda": "42707519684",
#     "numero_colli": "1",
#     "peso": "1.0",
#     "peso_volume": "1.0",
#     "tipo_spedizione": "N",
#     "svincolo_pre_post": "OKPRE",
#     "sede_pagante_notifica": "V1",
#     "contratto_pagante_notifica": "1730",
# }

# response = requests.post(
#     "https://gls-italy.com/index.php?option=com_gls&amp;lang=it",
#     cookies=cookies,
#     headers=headers,
#     data=data,
# )
