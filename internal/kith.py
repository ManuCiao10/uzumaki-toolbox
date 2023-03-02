import imaplib
from handler.utils import *
import re
import threading
import requests

def kith_handler(my_mail: imaplib.IMAP4_SSL):
    print_task("starting kith unsubscriber...", CYAN)

    kith_email = "newsletter@kith.com"
    key = "FROM"
    _, data = my_mail.search(None, key, kith_email)

    mail_id_list = data[0].split()  # IDs of all emails that we want to fetch

    # create a list of all emails
    emails = []
    for num in mail_id_list:
        try:
            _, data = my_mail.fetch(
                num, "(RFC822)"
            )  # RFC822 returns whole message (BODY fetches just body)
        except:
            print_task("error fetching email", RED)
            continue

        regex = r"To: (.*?)\r"
        data = re.findall(regex, data[0][1].decode("utf-8"))

        regex = r"<(.*?)>"
        data = re.findall(regex, data[1])

        if data[0] not in emails:
            emails.append(data[0])
            try:
                threading.Thread(target=kith, args=(data[0],)).start()
            except:
                print_task("Error starting tasks", RED)
                input("Press enter to exit...")
                return

        
def kith(email : str):
    url = "https://manage.kmail-lists.com/subscriptions/unsubscribe?a=VP3E36"

    print_task("successfully got email {}".format(email), PURPLE)
    
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary6hA7f3Dsr3v2iA7T",
        "Origin": "https://manage.kmail-lists.com",
        "Pragma": "no-cache",
        "Referer": "https://manage.kmail-lists.com/subscriptions/unsubscribe?a=VP3E36",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    params = {
        "a": "VP3E36",
    }

    data = (
        '------WebKitFormBoundary6hA7f3Dsr3v2iA7T\r\nContent-Disposition: form-data; name="$email"\r\n\r\n{%s}\r\n------WebKitFormBoundary6hA7f3Dsr3v2iA7T--\r\n'
        % email
    )

    try:
        response = requests.post(
            "https://manage.kmail-lists.com/subscriptions/unsubscribe",
            params=params,
            headers=headers,
            data=data,
        )
    except:
        print_task("error unsubscribing {}".format(email), RED)
        pass

    if url == response.url:
        print_task("successfully unsubscribed {}".format(email), GREEN)