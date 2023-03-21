from handler.utils import *
from internal.security import processRunning
import csv
import threading
import requests
import tls_client


class PickupUps:
    def __init__(self, row: list):
        self.country_dict = {
            "it": "en_IT",
            "es": "en_ES",
        }
        self.name = row[0].strip()
        self.surname = row[1].strip()
        self.phone = row[2].strip()
        self.address = row[3].strip()
        self.city = row[4].strip()
        self.zip_code = row[5].strip()
        self.country = row[6].strip()
        self.email = row[7].strip()
        self.loc = self.country_dict[self.country.lower()]

        return self.session()

    def session(self):
        self.session = tls_client.Session(client_identifier="chrome_105")

        print_task("Getting session...", PURPLE)

        try:
            if len(self.country) > 2:
                print_task("country must be 2 letters", RED)
                time.sleep(3)
                return
        except IndexError:
            print_task("country must be 2 letters", RED)
            time.sleep(3)
            return

        except Exception as e:
            print_task("Error: " + str(e), RED)
            time.sleep(3)
            return

        params_coutry = {
            "loc": self.loc,
        }

        headers = {
            "authority": "wwwapps.ups.com",
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
            response = self.session.get(
                "https://wwwapps.ups.com/pickup/schedule",
                params=params_coutry,
                headers=headers,
            )

        except requests.exceptions.ConnectionError:
            print_task("Connection Error", RED)
            time.sleep(3)
            return

        except requests.exceptions.Timeout:
            print_task("Timeout Error", RED)
            time.sleep(3)
            return

        if response.status_code != 200:
            print_task("Error getting session", RED)
            time.sleep(3)
            return

        if "Enter Collection Information" not in response.text:
            print_task("Error getting session response", RED)
            time.sleep(3)
            return

        return self.schedule()

    def schedule(self):
        print_task("Scheduling pickup...", YELLOW)

        headers = {
            "authority": "wwwapps.ups.com",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://wwwapps.ups.com",
            "pragma": "no-cache",
            "referer": "https://wwwapps.ups.com/pickup/schedule",
            "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

        data = f"operation=getAvailableDaysAndServices&address={self.address}&pd1=&pd2={self.city}&postalcode={self.zip_code}"
        try:
            response = self.session.post(
                "https://wwwapps.ups.com/pickup/ipajax", headers=headers, data=data
            )

        except requests.exceptions.ConnectionError:
            print_task("Connection error", RED)
            time.sleep(3)
            return

        pickup_data = response.text
        pickup_data = pickup_data[5:-2]

        try:
            pickup_dict = json.loads(pickup_data)
            self.dropoffdate = pickup_dict["PickupDates"][0]["DateValue"]

        except json.JSONDecodeError:
            print_task("JSONDecodeError", RED)
            time.sleep(3)
            return

        except KeyError:
            print_task("Keyerror check your address", RED)
            time.sleep(3)
            return

        self.payload = {
            "loc": self.loc,
            "gotoapp": "",
            "acctInfoDetails": "",
            "pickupInfoPageScheme": "",
            "selectedServices": "null",
            "EDITABLE_ACCTNUM": "FALSE",
            "localeValue": self.loc,
            "showPopup": "false",
            "facclosed": "false",
            "destslic": "null",
            "radioShipping": "Y",
            "tracknumlist": "",
            "accountnumber": "",
            "paramAcctZip": "",
            "company": self.name,
            "custname": self.name + " " + self.surname,
            "address": self.address,
            "room": "",
            "ROOM": "",
            "floor": "",
            "FLOOR": "",
            "pd2": self.city,
            "pd1": self.address,
            "postalcode": self.zip_code,
            "phone": self.phone,
            "extension": "",
            "addrSuggestRadio": "",
            "repl_name": "",
            "numberOfPackages": "1",
            "weight": "2",
            "numberOfPallets": "1",
            "palletweight": "",
            "pallettotweight": "",
            "length": "",
            "width": "",
            "height": "",
            "palletSizeOpts": "0",
            "paramServices": "011#002",
            "radioWeight70": "N",
            "radioComDocs": "N",
            "exppickup": "0",
            "dropoffdate": self.dropoffdate,
            "dropHour": "11",
            "dropMin": "00",
            "dropAMPM": "AM",
            "pickupdate": self.dropoffdate,
            "readyHours": "9",
            "readyMinutes": "0",
            "readyAMPM": "AM",
            "closeHours": "5",
            "closeMinutes": "0",
            "closeAMPM": "PM",
            "pickuppoint": "",
            "paramPickupReference": "",
            "specialinstructions": "",
            "expdeliver": "0",
            "dc1": "",
            "phoneList": "0",
            "email1": self.email,
            "email2": "",
            "email3": "",
            "email4": "",
            "email5": "",
            "emailmessage": self.email,
            "failedemail": self.email,
        }

        try:
            response = self.session.post(
                "https://wwwapps.ups.com/pickup/api/service/validate/create",
                headers=headers,
                data=self.payload,
            )
            data = response.json()
        except requests.exceptions.ConnectionError:
            print_task("Connection error", RED)
            time.sleep(3)
            return

        except Exception as e:
            print_task("Error: " + str(e), RED)
            time.sleep(3)
            return

        try:
            if data["valid"] == False:
                invalidFields = data["invalidFields"]
                for field in invalidFields:
                    print_task(f"{field} is invalid", RED)
                time.sleep(3)
                return

        except KeyError:
            pass

        if data["valid"] != True:
            print_task("Request Unknown error", RED)
            time.sleep(3)
            return

        return self.pre_payment()

    def pre_payment(self):
        headers = {
            "authority": "wwwapps.ups.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://wwwapps.ups.com",
            "pragma": "no-cache",
            "referer": "https://wwwapps.ups.com/pickup/request?loc=" + self.loc,
            "sec-ch-ua": '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        }

        params = {
            "loc": self.loc,
        }

        try:
            response = self.session.post(
                "https://wwwapps.ups.com/pickup/processinfo",
                params=params,
                headers=headers,
                data=self.payload,
            )
            if response.status_code != 200:
                print_task("Error: " + str(response.status_code), RED)
                time.sleep(3)
                return
        except Exception as e:
            print_task("Error: " + str(e), RED)
            time.sleep(3)
            return

        if "Verify Collection Request Details" in response.text:
            return self.payment()

    def payment(self):
        headers = {
            "authority": "wwwapps.ups.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "origin": "https://wwwapps.ups.com",
            "pragma": "no-cache",
            "referer": "https://wwwapps.ups.com/pickup/processinfo?loc=en_IT",
            "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        }

        params = {
            "loc": self.loc,
            "IP_schType": "ns",
        }

        data = {
            "loc": self.loc,
            "initiatingPage": "verification",
            "email1opt": "true",
            "addToAddressBook": "false",
            "email2opt": "true",
            "SUBMIT_BUTTON": "Next",
        }

        response = self.session.post(
            "https://wwwapps.ups.com/pickup/processverification",
            params=params,
            headers=headers,
            data=data,
        )

        if (
            "The UPS On Call Collection service is temporarily unavailable."
            in response.text
        ):
            print_task("Service is temporarily unavailable", RED)
            time.sleep(3)
            return

        if "Collection Request Number" in response.text:
            print_task("Scheduled pickup!", GREEN)


def pickup(username):
    processRunning()
    setTitleMode("Pickup ups")

    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    try:
        with open("Uzumaki/pickup/pickup_ups.csv", "r") as f:
            reader = csv.reader(f)

            try:
                next(reader)
            except StopIteration:
                print_task("file is empty, you must delete it.", RED)
                exit_program()

            try:
                row = next(reader)
            except StopIteration:
                print_task("please fill Uzumaki/pickup/pickup_ups.csv", RED)
                exit_program()

            f.seek(0)
            reader = csv.reader(f)
            next(reader)

            print_task("Starting pickup ups...", CYAN)
            for row in reader:
                threading.Thread(target=PickupUps, args=(row,)).start()

    except FileNotFoundError:
        print_task("Uzumaki/pickup/pickup_ups not found", RED)
        time.sleep(3)
        return
