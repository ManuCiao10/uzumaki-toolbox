from handler.utils import *
import imaplib
import re
import threading
import requests
from internal.security import processRunning


def get_gls_mails(user, password):
    try:
        # setup imap
        imap_url = "imap.gmail.com"
        with imaplib.IMAP4_SSL(imap_url) as my_mail:
            my_mail.login(user, password)
            my_mail.select("Inbox")

            key = "FROM"
            value = "noreply@gls-italy.com"

            _, data = my_mail.search(None, key, value)

            mail_id_list = data[0].split()
            print_task(f"found {len(mail_id_list)} gls mails...", PURPLE)
            msgs = []
            # Iterate through messages and extract data into the msgs list
            for num in mail_id_list:
                _, data = my_mail.fetch(num, "(RFC822)")

                if "tkn=3D" in str(data):
                    # print(str(data))
                    raw_tracking = re.search(
                        "(?P<url>https?://[^\s]+)", str(data)
                    ).group("url")
                    if "flexdelivery" in raw_tracking:
                        msgs.append(raw_tracking)

            return msgs

    except Exception as e:
        print_task(str(e), RED)
        exit_program()


def glsRedirect(username):
    processRunning()
    setTitleMode("gls redirect")
    print_task("gls redirect is locked", RED)
    exit_program()

    os.chdir("Uzumaki/gls")
    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    print_task("starting gls redirect...", PURPLE)

    # Get credentials from file
    try:
        with open("gls.json", "r") as f:
            credentials = json.load(f)

        if not validate(credentials):
            print_task("please fill credentials.json", RED)
            exit_program()

    except:
        print_task("error getting credentials", RED)
        exit_program()

    userGmail = credentials["userGmail"]
    passwordGmail = credentials["passwordGmail"]

    print_task("getting gls tracking...", CYAN)

    try:
        gls_mails = get_gls_mails(userGmail, passwordGmail)
        if not gls_mails:
            print_task("no gls redirectable gls tracking found", RED)
            exit_program()

    except Exception as e:
        print_task(f"error getting gls mails: {str(e)}", RED)
        exit_program()

    quantity = len(gls_mails) if isinstance(gls_mails, list) else 0
    print_task(f"found {quantity} redirectable gls tracking", GREEN)

    for mail in gls_mails:
        try:
            threading.Thread(
                target=redirectingGls, args=(mail, gls_mails.index(mail))
            ).start()
        except:
            print_task("Error starting tasks", RED)
            time.sleep(3)
            return


def redirectingGls(url, index):
    url = url.split("?")[1]

    replacements = [("tkn=3D", "tkn="), ("loc=3D", "loc="), ("num=3D", "num=")]
    for old, new in replacements:
        url = url.replace(old, new)
    url = "https://gls-italy.com/flexdelivery?" + url

    # from each mail get the tracking
    # print_task(f"redirecting [{index}] package...", PURPLE)
    print_task(f"redirecting [{index}] the package...", PURPLE)

    cookies = {
        "0c73b3f6168197b4a0547b472c2dfd1f": "u6a813787dmbtlurr67rcjqcrn",
        "joomsef_lang": "it",
        "browserLanguage": "en",
        "STunn": "BRvURPABOgo0PuIE2mGBHg$$",
        "5b7108f43b147774a7dd742a6bcdf08a": "sdoog682v2fc6obilfjfi9kioo",
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        # 'Cookie': '0c73b3f6168197b4a0547b472c2dfd1f=u6a813787dmbtlurr67rcjqcrn; joomsef_lang=it; browserLanguage=en; STunn=BRvURPABOgo0PuIE2mGBHg$$; 5b7108f43b147774a7dd742a6bcdf08a=sdoog682v2fc6obilfjfi9kioo',
        "Origin": "https://gls-italy.com",
        "Pragma": "no-cache",
        "Referer": "https://gls-italy.com/index.php?option=com_gls&amp;lang=it",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    data = {
        "option": "com_gls",
        "view": "svincola",
        "mode": "flexdelivery_sedeshop_controlla",
        "loc": "V1",
        "num": "630225014",
        "tkn": "pzYbpacv",
        "backcontrollo": "si",
        "destinatario": "coffeespecialist",
        "indirizzo": "via capo di mondo, n. 22/R",
        "cap": "50136",
        "localita": "firenze",
        "provincia": "FI",
        "destinatario_originale": "emanuele  ardinghi",
        "anagrafica_sede_punto_shop": "coffeespecialist - via capo di mondo, n. 22/R - 50136 firenze (FI)",
        "tiposvin": "Shop",
        "svinm": "",
        "postback": "",
        "parcel_shop_id": "18220",
        "partner_shop_id": "PRP_IT",
        "barcode": "V1630225014010T1",
        "email_notifica": "emanuele.ardinghi@gmail.com",
        "cellulare_notifica": "",
        "bda": "42707519684",
        "numero_colli": "1",
        "peso": "1.0",
        "peso_volume": "1.0",
        "tipo_spedizione": "N",
        "svincolo_pre_post": "OKPRE",
        "sede_pagante_notifica": "V1",
        "contratto_pagante_notifica": "1730",
    }

    response = requests.post(
        "https://gls-italy.com/index.php?option=com_gls&amp;lang=it",
        cookies=cookies,
        headers=headers,
        data=data,
    )
