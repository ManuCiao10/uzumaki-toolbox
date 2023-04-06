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

    quantity = 1

    # try:
    #     quantity = int(input(">>> "))
    # except:

    #     print_task("Invalid quantity", RED)
    #     print_task("using default quantity: 3", WHITE)
    #     quantity = 3
    #     time.sleep(3)

    for _ in range(quantity):
        Thread(
            target=Yahoo,
            args=(proxies, captcha_key),
        ).start()


class Yahoo:
    def __init__(self, proxy: str = None, captcha_key: str = None):
        self.client = Session(client_identifier="chrome_111")
        self.captcha_key = captcha_key

        proxy = random.choice(proxy).split(":")
        host = proxy[0]
        port = proxy[1]
        username = proxy[2]
        password = proxy[3]

        self.client.proxies = {
            "http": f"http://{username}:{password}@{host}:{port}",
            "https": f"http://{username}:{password}@{host}:{port}",
        }

        print_task("Proxy: " + str(proxy), PURPLE)

        self.client.headers = {
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
        self.password = f"{urandom(10).hex()}@!"

        return self.__login__()

    def __error_hanlder(self, code: str) -> str:
        errors = {
            "IDENTIFIER_EXISTS": "Esiste già un account Yahoo con questo indirizzo email. REPLACE_SIGNIN_LINK.",
            "DANGLING_IDENTIFIER_EXISTS": "Esiste già un account Yahoo con questo indirizzo email.",
            "USER_DATA_CORRUPT": "Esiste già un account Yahoo con questo indirizzo email.",
            "IDENTIFIER_NOT_AVAILABLE": "Questo indirizzo email non è disponibile per l'iscrizione, prova con un altro",
            "EXCEEDED_ACCOUNTS_PER_CONTACT": "Il tuo numero di cellulare è presente in troppi account Yahoo. Utilizza un altro numero.",
            "EXCEEDED_ACCOUNTS_PER_EMAIL": "La tua email è presente in troppi account Yahoo. Utilizzane una diversa.",
            "EXCEEDED_ACCOUNTS_PER_PHONE": "Risultano già account associati a questo numero di telefono. Utilizzane un altro.",
            "EXCEEDED_ACCOUNTS_PER_PHONE_MASS_REG": "Limite account raggiunto per questo numero. Utilizzane un altro per continuare",
            "EMAIL_DOMAIN_NOT_ALLOWED": "Non puoi usare questo indirizzo email. Prova invece a creare un indirizzo email Yahoo",
            "RESERVED_WORD_PRESENT": "Esiste già un account Yahoo con questo indirizzo email.",
            "ERROR_NOTFOUND": "Qualcosa non ha funzionato.",
            "ERR_SELECT_GOOGLE_ACCOUNT": "Seleziona un account",
            "ERROR_MISSING_FIELD": "Questa informazione è obbligatoria.",
            "ERROR_MISSING_FIELD_PHONE_ONLY": "Il tuo numero è necessario per la sicurezza dell'account e non verrà visualizzato da altri.",
            "FIELD_EMPTY": "Questo dato è obbligatorio.",
            "SOME_SPECIAL_CHARACTERS_NOT_ALLOWED": "Il nome utente può contenere solo lettere, numeri, punti (“.”) e trattini bassi (“_”).",
            "SOME_SPECIAL_CHARACTERS_NOT_ALLOWED_IN_EMAIL": "Assicurati di utilizzare il tuo indirizzo email completo, che includa una “@” e un dominio.",
            "INVALID_EMAIL": "Assicurati di utilizzare il tuo indirizzo email completo che include un “@” e un dominio.",
            "INVALID_PHONE_NUMBER": "Questa informazione sembra errata. Inserisci nuovamente il numero di telefono.",
            "INVALID_PHONE_TYPE": "Questo numero non è supportato, inseriscine un altro.",
            "INVALID_IDENTIFIER": "Errore: Identificatore non valido.",
            "TOO_MANY_REPEATED_CHARACTERS_IN_PASSWORD": "La password non è sufficientemente complessa? Utilizza una password più complessa.",
            "PASSWORD_LENGTH_INVALID": "La tua password non è abbastanza sicura, usane una più lunga.",
            "PASSWORD_TOO_SHORT": "La tua password non è abbastanza sicura, usane una più lunga.",
            "PASSWORD_CONTAINS_USERNAME": "La password non può contenere il tuo nome utente.",
            "PASSWORD_CONTAINS_NAME": "La password non può includere il tuo nome.",
            "WEAK_PASSWORD": "La password non è abbastanza sicura, usane una più lunga.",
            "INVALID_CHARACTERS_IN_PASSWORD": "Utilizza solo lettere, numeri e segni di punteggiatura standard.",
            "FIELD_TOO_LONG": "Troppo lunga.",
            "CANNOT_END_WITH_SPECIAL_CHARACTER": "Il nome utente deve terminare con una lettera o un numero.",
            "CANNOT_HAVE_MORE_THAN_ONE_PERIOD": "Non puoi avere due o più ”.” nel nome utente.",
            "NEED_AT_LEAST_ONE_ALPHA": "Utilizza almeno una lettera nel nome utente.",
            "CANNOT_START_WITH_SPECIAL_CHARACTER_OR_NUMBER": "Il nome utente deve iniziare con una lettera.",
            "CONSECUTIVE_SPECIAL_CHARACTERS_NOT_ALLOWED": "Non puoi inserire due o più ”.” o ”_” consecutivi.",
            "COMMON_PASSWORD": "Crea una password più sicura. Quella che hai inserito è troppo facile da indovinare.",
            "INVALID_BIRTHDATE": "Questa informazione sembra errata. Inserisci nuovamente la data di nascita.",
            "BIRTHDATE_TOO_OLD": "Questa informazione sembra errata. Inserisci nuovamente la data di nascita.",
            "BIRTHDATE_IN_FUTURE": "Questa informazione sembra errata. Inserisci nuovamente la data di nascita.",
            "UNDERAGE_USER": "L'utente non è maggiorenne.",
            "OVERAGE_USER": "I dati inseriti non sono corretti. Specifica nuovamente la tua data di nascita.",
            "INVALID_NAME_LENGTH": "Il nome è troppo lungo",
            "LENGTH_TOO_SHORT": "L'indirizzo email è troppo corto, utilizza un indirizzo più lungo.",
            "LENGTH_TOO_LONG": "L'indirizzo email è troppo lungo, utilizza un indirizzo più corto.",
            "ERROR_MULTIPLE_AT_SIGN": "Abbiamo capito che ti piace il simbolo “@”! Utilizzane solo uno nel tuo indirizzo email.",
            "ERROR_NO_DOMAIN": "Manca la parte dopo il simbolo ”@”.",
            "NAME_CONTAINS_URL": "Non puoi utilizzare questo nome",
            "SHOW": "mostra",
            "HIDE": "nascondi",
            "LINK_SIGN_IN": "Accedi",
            "DOMAIN_NOT_SUPPORTED": "Questo dominio non è supportato",
            "INVALID_BIRTHYEAR": "I dati inseriti non sono corretti. Indica nuovamente la tua data di nascita.",
            "RISKY_PASSWORD": "Questa password non è sicura. Dei malintenzionati possono facilmente trovarla online e tentare di accedere al tuo account.",
            "ELECTION_SPECIFIC_WORD_PRESENT": "Non disponibile, prova altro.",
        }

        return errors[code]

    def __login__(self):
        print("getting session...")

        try:
            resp = self.client.get(
                "https://login.yahoo.com/account/create",
                allow_redirects=True,
            )

            if resp.status_code != 200:
                # retry if failed
                print("error getting session...")
                time.sleep(3)
                return self.__login__()

            self.data_token = re.search(
                r'<input type="hidden" value="(.*?)" name="specData">', resp.text
            ).group(1)

            # <input type="hidden" value="s0RwWUF2" name="acrumb">
            self.acrumb = re.search(
                r'<input type="hidden" value="(.*?)" name="acrumb">', resp.text
            ).group(1)

            self.crumb = re.search(
                r'<input type="hidden" value="(.*?)" name="crumb">', resp.text
            ).group(1)

            print("Successfull got session...")
        except Exception as e:
            print("error doing request" + str(e))
            time.sleep(3)
            return self.__login__()

        return self.__payload__()

    def __payload__(self):
        print("getting payload...")

        token = urandom(3).hex()
        self.name = get_first_name()
        self.surname = get_last_name()
        self.email = f"{self.name}.{self.surname}{token}".lower()

        params = {
            "intl": "it",
            "specId": "yidregsimplified",
            "context": "reg",
            "done": "https://www.yahoo.com",
        }

        self.browser_fp_data = "browser-fp-data=%7B%22language%22%3A%22en-GB%22%2C%22colorDepth%22%3A30%2C%22deviceMemory%22%3A4%2C%22pixelRatio%22%3A2%2C%22hardwareConcurrency%22%3A8%2C%22timezoneOffset%22%3A-120%2C%22timezone%22%3A%22Europe%2FRome%22%2C%22sessionStorage%22%3A1%2C%22localStorage%22%3A1%2C%22indexedDb%22%3A1%2C%22openDatabase%22%3A1%2C%22cpuClass%22%3A%22unknown%22%2C%22platform%22%3A%22MacIntel%22%2C%22doNotTrack%22%3A%22unknown%22%2C%22plugins%22%3A%7B%22count%22%3A4%2C%22hash%22%3A%220b9799dd33522fb458a9aa13bea17079%22%7D%2C%22canvas%22%3A%22canvas+winding%3Ayes%7Ecanvas%22%2C%22webgl%22%3A1%2C%22adBlock%22%3A0%2C%22hasLiedLanguages%22%3A0%2C%22hasLiedResolution%22%3A0%2C%22hasLiedOs%22%3A0%2C%22hasLiedBrowser%22%3A0%2C%22touchSupport%22%3A%7B%22points%22%3A0%2C%22event%22%3A0%2C%22start%22%3A0%7D%2C%22fonts%22%3A%7B%22count%22%3A27%2C%22hash%22%3A%22d52a1516cfb5f1c2d8a427c14bc3645f%22%7D%2C%22audio%22%3A%22122.8735701811529%22%2C%22resolution%22%3A%7B%22w%22%3A%221728%22%2C%22h%22%3A%221117%22%7D%2C%22availableResolution%22%3A%7B%22w%22%3A%221020%22%2C%22h%22%3A%221728%22%7D%2C%22ts%22%3A%7B%22serve%22%3A1680262528711%2C%22render%22%3A1680262529058%7D%7D"

        data = (
            self.browser_fp_data
            + "&specId=yidregsimplified&cacheStored=&crumb="
            + self.crumb
            + "&acrumb="
            + self.acrumb
            + "&sessionIndex=&done=https%3A%2F%2Fwww.yahoo.com&googleIdToken=&authCode=&attrSetIndex=0&specData="
            + self.data_token
            + "&multiDomain=&tos0=oath_freereg%7Cit%7Cit-IT&firstName="
            + self.name
            + "&lastName="
            + self.surname
            + "&userid-domain=yahoo&userId="
            + self.email
            + "&yidDomainDefault=yahoo.com&yidDomain=yahoo.com"
            + "&password="
            + self.password
            + "&birthYear=2000&signup="
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
                return self.__payload__()

            if (
                "challenge-button pure-button puree-button-primary puree-spinner-button send-code"
                not in response.text
            ):
                print("something went wrong " + str(response.status_code))
                time.sleep(3)
                return self.__payload__()

        except Exception as e:
            print("error doing request " + str(e))
            time.sleep(3)
            return self.__payload__()

        print("Successfull got payload")

        # <input type="hidden" value="QQ--" name="sessionIndex">
        self.sessionIndex = re.search(
            r'<input type="hidden" value="(.*)" name="sessionIndex">', response.text
        ).group(1)

        self.specData = re.search(
            r'<input type="hidden" value="(.*)" name="specData">', response.text
        ).group(1)

        # replace &#x3D; with =
        self.specData = re.sub(r"&#x3D;", "=", self.specData)

        self.acrumb = re.search(
            r'<input type="hidden" value="(.*)" name="acrumb">', response.text
        ).group(1)

        self.crumb = re.search(
            r'<input type="hidden" value="(.*)" name="crumb">', response.text
        ).group(1)

        return self.verify()

    def verify(self):
        print("verifying...")

        self.country = "IT"
        phone_number = "3662299421"

        # get phone number from sms-activate
        # id, phone_number = getPhone()
        # respisne type => 1379189108 79059336349

        # put phone number in the form
        params = {
            "intl": "it",
            "lang": "it-IT",
            "specId": "yidregsimplified",
            "done": "https://www.yahoo.com/",
            "altreg": "1",
            "context": "reg",
        }

        data = (
            "browser-fp-data=%7B%22language%22%3A%22en-GB%22%2C%22colorDepth%22%3A30%2C%22deviceMemory%22%3A2%2C%22pixelRatio%22%3A2%2C%22hardwareConcurrency%22%3A5%2C%22timezoneOffset%22%3A-120%2C%22timezone%22%3A%22Europe%2FRome%22%2C%22sessionStorage%22%3A1%2C%22localStorage%22%3A1%2C%22indexedDb%22%3A1%2C%22openDatabase%22%3A1%2C%22cpuClass%22%3A%22unknown%22%2C%22platform%22%3A%22MacIntel%22%2C%22doNotTrack%22%3A%22unknown%22%2C%22plugins%22%3A%7B%22count%22%3A4%2C%22hash%22%3A%229fa208aa028bfcfdebc6647cf0bb14fb%22%7D%2C%22canvas%22%3A%22canvas+winding%3Ayes%7Ecanvas%22%2C%22webgl%22%3A1%2C%22adBlock%22%3A0%2C%22hasLiedLanguages%22%3A0%2C%22hasLiedResolution%22%3A0%2C%22hasLiedOs%22%3A0%2C%22hasLiedBrowser%22%3A0%2C%22touchSupport%22%3A%7B%22points%22%3A0%2C%22event%22%3A0%2C%22start%22%3A0%7D%2C%22fonts%22%3A%7B%22count%22%3A27%2C%22hash%22%3A%22d52a1516cfb5f1c2d8a427c14bc3645f%22%7D%2C%22audio%22%3A%22123.81775201154232%22%2C%22resolution%22%3A%7B%22w%22%3A%221728%22%2C%22h%22%3A%221117%22%7D%2C%22availableResolution%22%3A%7B%22w%22%3A%221020%22%2C%22h%22%3A%221728%22%7D%2C%22ts%22%3A%7B%22serve%22%3A1680709351913%2C%22render%22%3A1680709351984%7D%7D&specId=yidregsimplified&cacheStored="
            "&crumb="
            + self.crumb
            + "&acrumb="
            + self.acrumb
            + "&sessionIndex=QQ--&done=https%3A%2F%2Fwww.yahoo.com&googleIdToken=&authCode=&attrSetIndex=1&specData="
            + self.specData
            + "&multiDomain=&shortCountryCode=IT&phone="
            + phone_number
            + "&signup="
        )

        response = self.client.post(
            "https://login.yahoo.com/account/create", params=params, data=data
        )


        if "error?code=E500" in response.text:
            print("error getting code " + str(response.status_code))
            time.sleep(5)
            return self.verify()

        # get code from sms-activate
        # put code in the form
