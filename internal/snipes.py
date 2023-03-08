import re
import requests
import threading
import imaplib
from handler.utils import *


def snipes_handler(my_mail: imaplib.IMAP4_SSL):
    print_task("starting snipes unsubscriber...", CYAN)

    snipes_email = "no-reply@mail.snipes.com"
    key = "FROM"
    _, data = my_mail.search(None, key, snipes_email)

    mail_id_list = data[0].split()

    # create a list of all emails
    emails = []
    for num in mail_id_list:
        try:
            _, data = my_mail.fetch(num, "(RFC822)")
        except:
            print_task("error fetching email", RED)
            continue

        pattern = "<([^>]+)>"

        data = re.findall(pattern, data[0][1].decode("utf-8"))
        url = None

        for i in data:
            if "api/unsubscribe/" in i:
                url = i
                break

        if url and url not in emails:
            emails.append(url)

            try:
                threading.Thread(target=snipes, args=(url,)).start()
            except:
                print_task("Error starting tasks", RED)
                input("Press enter to exit...")
                return


def snipes(url: str):
    print_task(f"got email to unsubscribe...", PURPLE)

    headers = {
        "authority": "list-unsubscribe.eservice.emarsys.net",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }

    try:
        response = requests.get(
            url,
            headers=headers,
        )
    except:
        print_task(f"error unsubscribing...", RED)

    try:
        data = response.json()
        if data["success"] == True:
            print_task(f"successfully unsubscribed...", GREEN)

    except:
        print_task(f"error unsubscribing...", RED)
