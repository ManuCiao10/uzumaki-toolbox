import re
import requests
import threading
import imaplib
from handler.utils import *


def zalando_handler(my_mail: imaplib.IMAP4_SSL):
    print_task("starting jd unsubscriber...", CYAN)

    zalando_email = "ciao@my.zalando-prive.it"
    key = "FROM"
    _, data = my_mail.search(None, key, zalando_email)

    mail_id_list = data[0].split()

    # create a list of all emails
    emails = []
    for num in mail_id_list:
        try:
            _, data = my_mail.fetch(num, "(RFC822)")
        except:
            print_task("error fetching email", RED)
            continue

        regex = r"List-Unsubscribe: <(https://click.email.zalando-prive.com/subscription_center.aspx.*?)[\s>]"
        data = re.findall(regex, data[0][1].decode("utf-8"))

        if data and data[0] not in emails:
            emails.append(data[0])

            try:
                threading.Thread(target=zalando, args=(data[0],)).start()
            except:
                print_task("Error starting tasks", RED)
                time.sleep(3)
                return


def zalando(url: str):
    print_task("getting zalando email...", PURPLE)

    params = {
        "jwt": url.split("jwt=")[1],
    }

    try:
        response = requests.post(
            "https://click.email.zalando-prive.com/subscription_center.aspx",
            params=params,
            headers=headers,
            data=data,
        )
        if "Your subscriptions have been updated." in response.text:
            print_task("unsubscribed from zalando", GREEN)

        else:
            print_task("error unsubscribing from zalando", RED)
    except:
        print_task("error getting session zalando", RED)
        return


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Origin": "null",
    "Pragma": "no-cache",
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
    "__EVENTTARGET": "_ctl14",
    "__EVENTARGUMENT": "",
    "__VIEWSTATE": "",
    "_objUnsubAllChk": "on",
}
