import os
import json
import time
from handler.utils import *
import imaplib
import email
from restocks.client import Client
import csv
from internal.security import processRunning


def create_csv(restocks_sales, wise_mails):
    missing_payout_count = 0

    try:
        with open("output.csv", "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(["ID", "PAYOUT"])

            for sale in restocks_sales:
                payout = any(str(sale.id) in str(mail) for mail in wise_mails)
                if payout:
                    writer.writerow([sale.id, "True"])
                else:
                    writer.writerow([sale.id, "False"])
                    missing_payout_count += 1

    except Exception as e:
        print_task(str(e), RED)
        exit_program()

    return missing_payout_count


def get_restocks_sales(restocks_user, restocks_password):
    # Initialize client
    try:
        restocks_client = Client()
        restocks_client.login(restocks_user, restocks_password)

        # Get history sales
        sales_history = restocks_client.get_sales_history()
        history_filtered = [sale for sale in sales_history if sale.date.year >= 2022]

    except Exception as e:
        print_task(str(e), RED)
        exit_program()

    return history_filtered


def get_wise_mails(user, password, wise_mail):
    try:
        # setup imap
        imap_url = "imap.gmail.com"
        with imaplib.IMAP4_SSL(imap_url) as my_mail:
            my_mail.login(user, password)
            my_mail.select("Inbox")

            key = "FROM"
            value = wise_mail
            _, data = my_mail.search(None, key, value)

            mail_id_list = data[0].split()  # IDs of all emails that we want to fetch

            msgs = []  # empty list to capture all messages
            # Iterate through messages and extract data into the msgs list
            for num in mail_id_list:
                typ, data = my_mail.fetch(
                    num, "(RFC822)"
                )  # RFC822 returns whole message (BODY fetches just body)
                msgs.append(data)

        raw_mail_text = []
        for msg in msgs[::-1]:
            for response_part in msg:
                if isinstance(response_part, tuple):
                    my_msg = email.message_from_bytes(response_part[1])
                    for part in my_msg.walk():
                        if part.get_content_type() == "text/html":
                            raw_text = part.get_payload(decode=True).decode("utf-8")
                            raw_mail_text.append(raw_text)

        return raw_mail_text

    except Exception as e:
        print_task(str(e), RED)
        exit_program()


def validate_credentials(credentials):
    required_fields = ["userGmail", "passwordGmail", "userRestock", "passwordRestock"]
    for field in required_fields:
        if credentials.get(field, "").strip() == "":
            return False
    return True


def restockPayout(username):
    processRunning()
    setTitleMode("restock payout")

    os.chdir("Uzumaki/restock")

    os.system("cls" if os.name == "nt" else "clear")

    print(f"{RED}{BANNER}{RESET}")

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    print_task("starting restock payout...", PURPLE)

    # Get credentials from file
    try:
        with open("credentials.json", "r") as f:
            credentials = json.load(f)

        if not validate_credentials(credentials):
            print_task("please fill credentials.json", RED)
            exit_program()

    except:
        print_task("error getting credentials", RED)
        exit_program()

    userGmail = credentials["userGmail"]
    passwordGmail = credentials["passwordGmail"]
    userRestock = credentials["userRestock"]
    passwordRestock = credentials["passwordRestock"]
    wise_mail = "noreply@wise.com"

    try:
        print_task("getting wise mails...", CYAN)
        wise_mails = get_wise_mails(userGmail, passwordGmail, wise_mail)
        print_task(f"wise mails: {len(wise_mails)}", GREEN)
    except Exception as e:
        print_task(f"error getting wise mails: {str(e)}", RED)
        exit_program()

    try:
        print_task("getting restock sales...", CYAN)
        restocks_sales = get_restocks_sales(userRestock, passwordRestock)
        print_task(f"restocks sales: {len(restocks_sales)}", GREEN)
    except Exception as e:
        print_task(f"error getting restock sales: {str(e)}", RED)
        exit_program()

    # Create CSV and get missing payout count
    missing_payout_count = create_csv(restocks_sales, wise_mails)
    print_task(f"missing payout count: {missing_payout_count}", YELLOW)

    # check output.csv
    print_task("check restock/output.csv", PURPLE)
    time.sleep(3)
