import os
import time
import re

from handler.utils import *
from tls_client import Session
from threading import Thread
from internal.security import processRunning
from names import get_first_name, get_last_name
from os import urandom
from generator.utils.sms import getPhone
import random


def yahoo(username):
    processRunning()
    setTitleMode("GENERATOR YAHOO")

    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    try:
        proxies = open("Uzumaki/proxies.txt", "r").read().splitlines()

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

    print_task("Insert quantity:", WHITE)

    try:
        quantity = int(input(">>> "))
    except:
        print_task("Invalid quantity", RED)
        print_task("using default quantity: 3", WHITE)
        quantity = 3

    for _ in range(quantity):
        Thread(
            target=Yahoo,
            args=(proxies, captcha_key),
        ).start()


class Yahoo:
    def __init__(this, proxy: str = None, captcha_key: str = None):
        this.client = Session(client_identifier="chrome_113")
        this.captcha_key = captcha_key

        proxy = random.choice(proxy).split(":")
        host = proxy[0]
        port = proxy[1]
        username = proxy[2]
        password = proxy[3]

        this.client.proxies = {
            "http": f"http://{username}:{password}@{host}:{port}",
            "https": f"http://{username}:{password}@{host}:{port}",
        }

        this.params = {
            "intl": "it",
            "specId": "yidregsimplified",
            "done": "https://www.yahoo.com",
            "context": "reg",
        }

        this.__start__ = this.__init_client()
        this.account = this.register_account()
        this.message = this.__message()

    def __init_client(this):
        try:
            headers = {
                "authority": "login.yahoo.com",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "sec-ch-ua": '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "none",
                "sec-fetch-user": "?1",
                "sec-gpc": "1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            }

            params = {
                "intl": "it",
                "specId": "yidregsimplified",
                "context": "reg",
                "done": "https://www.yahoo.com",
            }

            response = this.client.get(
                "https://login.yahoo.com/account/create",
                params=params,
                headers=headers,
            )

        except Exception as e:
            print_task("Error loading client" + str(e), RED)
            time.sleep(2)

        try:
            this.crumb = re.findall(
                r'<input type="hidden" value="(.*)" name="crumb">', response.text
            )[0]
        except:
            this.crumb = ""

        try:
            this.acrumb = re.findall(
                r'<input type="hidden" value="(.*)" name="acrumb">', response.text
            )[0]
        except:
            this.acrumb = ""

        this.specData = re.findall(
            r'<input type="hidden" value="(.*)" name="specData">', response.text
        )[0]

        this.password = f"{urandom(10).hex()}@!"
        this.name = get_first_name()
        this.surname = get_last_name()
        this.email = f"{this.name}.{this.surname}{urandom(3).hex()}".lower()
        # this.phone = getPhone()
        this.browser_fp_data = "browser-fp-data=%7B%22language%22%3A%22en-GB%22%2C%22colorDepth%22%3A30%2C%22deviceMemory%22%3A4%2C%22pixelRatio%22%3A2%2C%22hardwareConcurrency%22%3A8%2C%22timezoneOffset%22%3A-120%2C%22timezone%22%3A%22Europe%2FRome%22%2C%22sessionStorage%22%3A1%2C%22localStorage%22%3A1%2C%22indexedDb%22%3A1%2C%22openDatabase%22%3A1%2C%22cpuClass%22%3A%22unknown%22%2C%22platform%22%3A%22MacIntel%22%2C%22doNotTrack%22%3A%22unknown%22%2C%22plugins%22%3A%7B%22count%22%3A4%2C%22hash%22%3A%220b9799dd33522fb458a9aa13bea17079%22%7D%2C%22canvas%22%3A%22canvas+winding%3Ayes%7Ecanvas%22%2C%22webgl%22%3A1%2C%22adBlock%22%3A0%2C%22hasLiedLanguages%22%3A0%2C%22hasLiedResolution%22%3A0%2C%22hasLiedOs%22%3A0%2C%22hasLiedBrowser%22%3A0%2C%22touchSupport%22%3A%7B%22points%22%3A0%2C%22event%22%3A0%2C%22start%22%3A0%7D%2C%22fonts%22%3A%7B%22count%22%3A27%2C%22hash%22%3A%22d52a1516cfb5f1c2d8a427c14bc3645f%22%7D%2C%22audio%22%3A%22122.8735701811529%22%2C%22resolution%22%3A%7B%22w%22%3A%221728%22%2C%22h%22%3A%221117%22%7D%2C%22availableResolution%22%3A%7B%22w%22%3A%221020%22%2C%22h%22%3A%221728%22%7D%2C%22ts%22%3A%7B%22serve%22%3A1680262528711%2C%22render%22%3A1680262529058%7D%7D"

    def register_account(this):
        data = f"{this.browser_fp_data}&specId=yidregsimplified&cacheStored=&crumb{this.crumb}=&acrumb={this.acrumb}&sessionIndex=&done=https%3A%2F%2Fwww.yahoo.com&googleIdToken=&authCode=&attrSetIndex=0&specData={this.specData}&multiDomain=&tos0=oath_freereg%7Cit%7Cit-IT&firstName={this.name}&lastName={this.surname}&userid-domain=yahoo&userId={this.email}&yidDomainDefault=yahoo.com&yidDomain=yahoo.com&password={this.password}&mm=2&dd=1&yyyy=2002&signup="

        this.headers = {
            "authority": "login.yahoo.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://login.yahoo.com",
            "referer": "https://login.yahoo.com/account/create?intl=it&specId=yidregsimplified&done=https%3A%2F%2Fwww.yahoo.com&context=reg",
            "sec-ch-ua": '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        }
        response = this.client.post(
            "https://login.yahoo.com/account/create",
            params=this.params,
            headers=this.headers,
            data=data,
        )

        try:
            this.crumb = re.findall(
                r'<input type="hidden" value="(.*)" name="crumb">', response.text
            )[0]
        except:
            this.crumb = ""

        this.acrumb = re.findall(
            r'<input type="hidden" value="(.*)" name="acrumb">', response.text
        )[0]

        this.spec_data = re.findall(
            r'<input type="hidden" value="(.*)" name="specData">', response.text
        )[0]

        print_task("registering account", YELLOW)

        this.session_index = re.findall(
            r'<input type="hidden" value="(.*)" name="sessionIndex">', response.text
        )[0]

        with open("yahoo.html", "a") as f:
            f.write(response.text)

    def __message(this):
        data = f"{this.browser_fp_data}&specId=yidregsimplified&cacheStored=&crumb={this.crumb}&acrumb={this.acrumb}&sessionIndex={this.session_index}&done=https%3A%2F%2Fwww.yahoo.com&googleIdToken=&authCode=&attrSetIndex=1&specData={this.spec_data}&multiDomain=def&shortCountryCode=IT&phone=3662299421&signup="
        headers = {
            "authority": "login.yahoo.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://login.yahoo.com",
            "referer": "https://login.yahoo.com/account/create?intl=it&specId=yidregsimplified&done=https%3A%2F%2Fwww.yahoo.com&context=reg",
            "sec-ch-ua": '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        }
        # data = f"browser-fp-data=%7B%22language%22%3A%22en-GB%22%2C%22colorDepth%22%3A30%2C%22deviceMemory%22%3A4%2C%22pixelRatio%22%3A2%2C%22hardwareConcurrency%22%3A10%2C%22timezoneOffset%22%3A-120%2C%22timezone%22%3A%22Europe%2FRome%22%2C%22sessionStorage%22%3A1%2C%22localStorage%22%3A1%2C%22indexedDb%22%3A1%2C%22openDatabase%22%3A1%2C%22cpuClass%22%3A%22unknown%22%2C%22platform%22%3A%22MacIntel%22%2C%22doNotTrack%22%3A%22unknown%22%2C%22plugins%22%3A%7B%22count%22%3A4%2C%22hash%22%3A%22b751869d0b6e96ff50b320748f196d80%22%7D%2C%22canvas%22%3A%22canvas+winding%3Ayes%7Ecanvas%22%2C%22webgl%22%3A1%2C%22adBlock%22%3A0%2C%22hasLiedLanguages%22%3A0%2C%22hasLiedResolution%22%3A0%2C%22hasLiedOs%22%3A0%2C%22hasLiedBrowser%22%3A0%2C%22touchSupport%22%3A%7B%22points%22%3A0%2C%22event%22%3A0%2C%22start%22%3A0%7D%2C%22fonts%22%3A%7B%22count%22%3A27%2C%22hash%22%3A%22d52a1516cfb5f1c2d8a427c14bc3645f%22%7D%2C%22audio%22%3A%22123.2905692974673%22%2C%22resolution%22%3A%7B%22w%22%3A%221728%22%2C%22h%22%3A%221117%22%7D%2C%22availableResolution%22%3A%7B%22w%22%3A%221020%22%2C%22h%22%3A%221728%22%7D%2C%22ts%22%3A%7B%22serve%22%3A1683404094898%2C%22render%22%3A1683404094967%7D%7D&specId=yidregsimplified&cacheStored=&crumb=&acrumb={this.acrumb}&sessionIndex=Qg--&done=https%3A%2F%2Fwww.yahoo.com&googleIdToken=&authCode=&attrSetIndex=1&specData={this.spec_data}&multiDomain=def&shortCountryCode=IT&phone=3662299421&signup="

        counter = 0
        while counter < 30:
            response = this.client.post(
                "https://login.yahoo.com/account/create",
                params=this.params,
                headers=headers,
                data=data,
            )

            print(response.text)
            counter += 1
