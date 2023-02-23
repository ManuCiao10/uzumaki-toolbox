import os
import json
import time
from handler.utils import *
import imaplib
import email

def get_wise_mails(user, password, wise_mail):
    try:
        # setup imap
        imap_url = 'imap.gmail.com'
        with imaplib.IMAP4_SSL(imap_url) as my_mail:
            my_mail.login(user, password)
            my_mail.select('Inbox')

            key = 'FROM'
            value = wise_mail
            _, data = my_mail.search(None, key, value)

            mail_id_list = data[0].split()  # IDs of all emails that we want to fetch

            msgs = []  # empty list to capture all messages
            # Iterate through messages and extract data into the msgs list
            for num in mail_id_list:
                typ, data = my_mail.fetch(num, '(RFC822)')  # RFC822 returns whole message (BODY fetches just body)
                msgs.append(data)

        raw_mail_text = []
        for msg in msgs[::-1]:
            for response_part in msg:
                if isinstance(response_part, tuple):
                    my_msg = email.message_from_bytes(response_part[1])
                    for part in my_msg.walk():
                        if part.get_content_type() == 'text/html':
                            raw_text = part.get_payload(decode=True).decode('utf-8')
                            raw_mail_text.append(raw_text)

        return raw_mail_text

    except Exception as e:
        print_task(str(e), RED)
        time.sleep(5)
        os._exit(1)

def restockPayout():
    #url: https://www.youtube.com/watch?v=hXiPshHn9Pw

    os.chdir("Uzumaki/restock")

    print_task("starting restock payout...", CYAN)

    # Get credentials from file
    try:
        with open("credentials.json", "r") as f:
            credentials = json.load(f)
            userGmail = credentials["userGmail"]
            passwordGmail = credentials["passwordGmail"]

            userRestock = credentials["userRestock"]
            passwordRestock = credentials["passwordRestock"]

            wise_mail = "noreply@wise.com"
            
            f.close()

        if userGmail == "userGmail here" or passwordGmail == "passwordGmail here" or userRestock == "userRestock here" or passwordRestock == "passwordRestock here":
            print_task("please fill credentials.json", RED)
            time.sleep(5)
            os._exit(1)

        if len(userGmail) == 0 or len(passwordGmail) == 0 or len(userRestock) == 0 or len(passwordRestock) == 0:
            print_task("please fill credentials.json", RED)
            time.sleep(5)
            os._exit(1)

        
        wise_mails = get_wise_mails(userGmail, passwordGmail, wise_mail)
        print_task("wise mails: " + str(len(wise_mails)), GREEN)
        
    except:
        print_task("error getting credentials", RED)
        time.sleep(5)
        os._exit(1)
    