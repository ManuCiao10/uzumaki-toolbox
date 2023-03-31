import os
import time

from handler.utils import *
from tls_client import Session
from threading import Thread
from internal.security import processRunning


def yahoo(username):
    processRunning()
    setTitleMode("GENERATOR YAHOO")

    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    try:
        proxies = open("Uzumaki/proxies.txt", "r").read().splitlines()
        # check if file is empty
        if len(proxies) == 0:
            print_task("Please fill uzumaki/proxies.txt or yahoo will fuck us", RED)
            time.sleep(2)
            return
    except Exception as e:
        print_task("Error loading proxies" + str(e), RED)
        time.sleep(2)
        return

    try:
        settings = load_settings()
        captcha_key = settings["capsolver_key"]

    except Exception as e:
        print_task("Error loading settings" + str(e), RED)
        time.sleep(2)
        return

    # insert quantity
    print_task("Insert quantity:", WHITE)

    try:
        quantity = int(input(">>> "))
    except:
        print_task("Invalid quantity", RED)
        print_task("using default quantity: 3", WHITE)
        quantity = 3
        time.sleep(3)

    for _ in range(quantity):
        Thread(
            target=Yahoo,
            args=(
                proxies,
                captcha_key,
            ),
        ).start()


class Yahoo:
    def __init__(self, proxy: str = None, captcha_key :str = None):
        self.client = Session(client_identifier="chrome_108")

        self.headers = {
            "authority": "login.yahoo.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://login.yahoo.com",
            "pragma": "no-cache",
            "referer": "https://login.yahoo.com/account/create",
            "sec-ch-ua": '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        }

        self.data_token = ""

        return self.login()

    def login(self):
        print("getting session...")

        try:
            resp = self.client.get(
                "https://login.yahoo.com/account/create",
                headers=self.headers,
                allow_redirects=True,
            )

            if resp.status_code != 200:
                # retry if failed
                print("error getting session...")
                time.sleep(3)
                return self.login()

            match = re.search(
                r'<input type="hidden" value="(.*?)" name="specData">', resp.text
            )

            if match:
                self.data_token = match.group(1)

            print("Successfull got session...")
        except Exception as e:
            print("error doing request" + str(e))
            time.sleep(3)
            return self.login()

        return self.payload()

    def payload(self):
        print("getting payload...")

        params = {
            "intl": "it",
            "specId": "yidregsimplified",
            "context": "reg",
            "done": "https://www.yahoo.com",
        }

        data = (
            "browser-fp-data=%7B%22language%22%3A%22en-GB%22%2C%22colorDepth%22%3A24%2C%22deviceMemory%22%3A1%2C%22pixelRatio%22%3A2%2C%22hardwareConcurrency%22%3A7%2C%22timezoneOffset%22%3A-120%2C%22timezone%22%3A%22Europe%2FRome%22%2C%22sessionStorage%22%3A1%2C%22localStorage%22%3A1%2C%22indexedDb%22%3A1%2C%22openDatabase%22%3A1%2C%22cpuClass%22%3A%22unknown%22%2C%22platform%22%3A%22MacIntel%22%2C%22doNotTrack%22%3A%22unknown%22%2C%22plugins%22%3A%7B%22count%22%3A4%2C%22hash%22%3A%222d8b4607a01680e3ff172e1ccd83a02a%22%7D%2C%22canvas%22%3A%22canvas+winding%3Ayes%7Ecanvas%22%2C%22webgl%22%3A1%2C%22webglVendorAndRenderer%22%3A%22Google+Inc.+%28Google%29%7EANGLE+%28Google%2C+Vulkan+1.3.0+%28SwiftShader+Device+%28Subzero%29+%280x0000C0DE%29%29%2C+SwiftShader+driver%29%22%2C%22adBlock%22%3A0%2C%22hasLiedLanguages%22%3A0%2C%22hasLiedResolution%22%3A0%2C%22hasLiedOs%22%3A0%2C%22hasLiedBrowser%22%3A0%2C%22touchSupport%22%3A%7B%22points%22%3A0%2C%22event%22%3A0%2C%22start%22%3A0%7D%2C%22fonts%22%3A%7B%22count%22%3A27%2C%22hash%22%3A%22d52a1516cfb5f1c2d8a427c14bc3645f%22%7D%2C%22audio%22%3A%22123.30898461164907%22%2C%22resolution%22%3A%7B%22w%22%3A%221440%22%2C%22h%22%3A%22900%22%7D%2C%22availableResolution%22%3A%7B%22w%22%3A%22816%22%2C%22h%22%3A%221440%22%7D%2C%22ts%22%3A%7B%22serve%22%3A1680035449265%2C%22render%22%3A1680035449771%7D%7D&specId=yidregsimplified&cacheStored=&crumb=&acrumb=X3z3MBBy&sessionIndex=&done=https%3A%2F%2Fwww.yahoo.com&googleIdToken=&authCode=&attrSetIndex=0&specData="
            + self.data_token
            + "&multiDomain=&tos0=oath_freereg%7Cit%7Cit-IT&firstName=emanuele&lastName=ardinghid&userid-domain=yahoo&userId=dcfgdddddddvhb&yidDomainDefault=yahoo.com&yidDomain=yahoo.com&password=jJ%23NK%2Bee%26sMDE5C&birthYear=2000&signup="
        )
        try:
            response = self.client.post(
                "https://login.yahoo.com/account/create",
                params=params,
                data=data,
            )
            if response.status_code != 200:
                print("error getting payload " + str(response.status_code))
                time.sleep(2)
                return self.payload()

            if "It looks like something went" in response.text:
                print("something went wrong " + str(response.status_code))
                time.sleep(2)
                return self.payload()

            print("Successfull got payload")
            # print(response.text)

        except Exception as e:
            print("error doing request " + str(e))
            time.sleep(2)
            return self.payload()
