import os
from handler.utils import *
import csv
import time
import threading
import tls_client
import requests

zalandoAPI = "rRo4r3bdjx5uPqcoZq8lo4b4ZoJtNG4B2ZG7I9Hx"

# add proxies
# add product sku cartable


def zalandoHandler(username):
    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    try:
        with open("Uzumaki/zalando/accounts.csv") as f:
            reader = csv.reader(f)

            try:
                next(reader)
            except StopIteration:
                print_task("file is empty", RED)
                time.sleep(3)
                return

            try:
                row = next(reader)
            except StopIteration:
                print_task(f"Please Fill Uzumaki/zalando/accounts.csv", RED)
                time.sleep(3)
                return

            f.seek(0)
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                email = row[0].strip()
                password = row[1].strip()

                try:
                    threading.Thread(target=zalando, args=(email, password)).start()
                except:
                    print_task("Error starting tasks", RED)
                    input("Press enter to exit...")
                    return

    except FileNotFoundError:
        print_task("file accounts.csv not found", RED)
        input("Press Enter to exit...")
        return


class zalando(threading.Thread):
    def __init__(self, email, password):
        threading.Thread.__init__(self)
        self.email = email
        self.password = password

        self.session()

    def session(self):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

        print_task(f"getting session for {self.email}:{self.password}", PURPLE)
        session = tls_client.Session(client_identifier="chrome_110")

        proxy = "localhost:8080"

        session.proxies = {
            "http": "http://" + proxy,
            "https": "https://" + proxy,
        }

        headers = {
            "authority": "accounts.zalando.com",
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

        response = session.get(
            "https://accounts.zalando.com/authenticate", headers=headers
        )
        bm_sz = response.cookies.get_dict()["bm_sz"]

        # ------GET to the script endpoint------#

        response = session.get(
            "https://accounts.zalando.com/Uhpi5/U/N5/C_Ka/Bw9QKi6u/z5aESh0wLu/QFJ-eUU/XhUFZ/0AuQRQ",
            headers=headers,
        )
        _abck = response.cookies.get_dict()["_abck"]

        # ------POST to get the akamai payload------#

        api_headers = {
            "x-api-key": zalandoAPI,
        }

        body = {
            "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "pageUrl": "https://accounts.zalando.com/authenticate",
            "version": "2",
            "abck": _abck,
            "bmsz": bm_sz,
        }

        akamai_session = tls_client.Session(client_identifier="chrome_110")
        response = akamai_session.post(
            "https://api.justhyped.dev/sensor", headers=api_headers, json=body
        )

        payload = response.json()["payload"]

        # ------POST sensor data to the script endpoint (1)------#
        headers = {
            "authority": "accounts.zalando.com",
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "text/plain;charset=UTF-8",
            "origin": "https://accounts.zalando.com",
            "pragma": "no-cache",
            "referer": "https://accounts.zalando.com/authenticate",
            "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        }

        response = session.post(
            "https://accounts.zalando.com/Uhpi5/U/N5/C_Ka/Bw9QKi6u/z5aESh0wLu/QFJ-eUU/XhUFZ/0AuQRQ",
            headers=headers,
            data=payload,
        )
        print(response.text)
