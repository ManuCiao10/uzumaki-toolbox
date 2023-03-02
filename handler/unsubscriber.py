# • JD Sports 
# • Size?
# • Footpatrol
# • Wellgosh
# • Hipstore
# • Kickz
# • Kith EU
# • Stress
# • Footshop
# • VEVE
# • Zalando
# • Snipes
# • END
# • Starcow

import imaplib
import os
import json
from handler.utils import *
import threading
from internal.kith import kith_handler

def unsubscriber():
    try:
        os.chdir("Uzumaki/unsubscriber")
    except:
        print_task("error finding unsubscriber folder...", RED)
        input("Press Enter to exit...")
        return

    print_task("starting unsubscriber...", PURPLE)
    # Get credentials from file
    try:
        with open("unsubscriber.json", "r") as f:
            credentials = json.load(f)

        if not validate(credentials):
            print_task("please fill unsubscriber.json", RED)
            input("Press Enter to exit...")
            return

    except:
        print_task("error getting credentials", RED)
        input("Press Enter to exit...")
        return

    user = credentials["userGmail"]
    password = credentials["passwordGmail"]

    # connect to email
    imap_url = "imap.gmail.com"
    try:
        my_mail = imaplib.IMAP4_SSL(imap_url)
        my_mail.login(user, password)
        my_mail.select("Inbox")

    except:
        print_task("error connecting to email", RED)
        input("Press Enter to exit...")
        return
    
    #threading that handles all the websites modules
    try:
        threading.Thread(target=kith_handler, args=(my_mail,)).start()
        threading.Thread(target=jd_handler, args=(my_mail,)).start()
    except:
        print_task("Error starting tasks", RED)
        input("Press enter to exit...")
        return

def jd_handler(my_mail: imaplib.IMAP4_SSL):
    print_task("starting jd unsubscriber...", CYAN)

    jd_email = "news@email-jdsports.com"


