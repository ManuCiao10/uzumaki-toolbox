import requests
import time
from handler.utils import *
import os
import csv
import threading
from internal.security import processRunning
from generator.utils.crypto import Crypto
from tls_client import Session


def Inizialize(username):
    processRunning()
    setTitleMode("GENERATOR OUTLOOK")

    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print(RED + BANNER + RESET)

        print(
            f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n"
        )


class Outlook:
    def __init__(this, proxy: str = None):
        this.client = Session(client_identifier="chrome_108")
        this.client.proxies = (
            {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        )

        this.Key = None
        this.randomNum = None
        this.SKI = None
        this.uaid = None
        this.tcxt = None
        this.apiCanary = None
        this.encAttemptToken = ""
        this.dfpRequestId = ""

        this.siteKey = "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA"
        this.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

        this.__start__ = this.__init_client()
        this.account_info = this.__account_info()

        this.cipher = Crypto.encrypt(
            this.account_info["password"], this.randomNum, this.Key
        )
