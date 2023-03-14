from handler.utils import *
from internal.security import processRunning
import csv
import threading
import requests
import tls_client


def payment(session: tls_client.Session):
    # cookies = {
    #     "com.ups.pickup.cb.sData": "ddc9f477d3da496ab2a416e82f31b7fc:sMvXgD0s1ojIWYFELWlpMYYm0DH3p59mp2cBaea8M/0=",
    #     "sharedsession": "1730106f-a55f-4ff8-86a9-51044248540f:w",
    #     "ups_language_preference": "en_IT",
    #     "AKA_A2": "A",
    #     "bm_sz": "FE6D4DC1E492FB3ADB8025D80A0354C2~YAAQgTRoaK7okb6GAQAA0XqR0hNmimpjiUdae+jXO9V6idY3Zbus2RcxJSi9p04TYqCk4MAcscocsVr1HpIHy9zT9/2d0P2+5PY+RIHNSm6IEstsgT8v1wYk8WpSalM/x3bK9mKw/IzCdkk82H16EwndvsdQ9YENuQY1k+4nPzbtUR+mRFkRekpLz87K/dhTTD688aL8JNqPkIApU7TTq0uWKSXTizyPFK+SzG/kpMBBgoeLlllB2ceIxz+/NylX8aVOtCkNXMXLDuUsZ9U5y6D0/hVmwQB3uL2mQ9yyt7U=~4342084~4538679",
    #     # "PIM-SESSION-ID": session_id,
    #     "_abck": "464E8396C1C205CDC96959B94060869C~0~YAAQgTRoaMvokb6GAQAAP3+R0gkEmmAXNsepUP9D9X3tSwHdobNNN3dY0uECGbzgUw+ad6aryvJTtr+pwavRXfAR0OQv/sYe+J/FeESkrmgICkXvNQBXtEFyYpNiUtJkXlkQjRKLIaC7wjasoq0q30iUcoI9Njoc5HBcADg7//MIJJo0s09fpMJb/ZtAjEzdAVITdNsWq+BiHKfdwgUMd0dsGYgEQVwQOoZXO4RYdfkQg/ZAtBU5YbPFD8tMMVohmvZlXENEIHh6y1rzcA9r1P1cUmC0agfUpT7DEQSmo19FzYnlOxcV8l6FcWzsQzPnRqOJDfw5n2X0x4si0/kwpEQA6Ym52/DAVpVzYjxRrRGuScVW/P00/G/DiZ32w+efBpD1mLxgcQI06r1Fw6CmW+4G3SYR~-1~-1~1678573511",
    #     "ak_bmsc": "4584D6539B066A9321B81D4FB02D786B~000000000000000000000000000000~YAAQgTRoaN3okb6GAQAALYGR0hPzuLnSR0K27XeXfdkiAyes0yvnOTx/oyo8Menk4WG7jqodTpPxKD1g3lts3RX5oj9u0rqE7kocjn0tlLrO80HKMHDsdLmZGO8KkJpIo5KUWSXP0iAIr555bmjtKijC8Lv6+Yrm0ZVLy4PZG8X/slGdyN5O4o/u0NVOjfF4xxBbfQ5KGsBWCTN1tCcwe+lNCrzUeAbSqAOSi+XsiC50YdzXx+1gkg6BccASQPjVeR7WxFxraOgUh+K3MUhtelZ1pvqjqug4YdF8rbsidN1lD+2ii307nY1uwRyxsXy41w7qJ6Y1bl4r9dvCb/yqHxSbtR4XC4PEWZGOirQryW7i6EcYvYjR3f3p815dMF3abzZvuk95wu826eT4aMeX3RWI7vzG8qD4aMRy0Crz9PtT4ecYMXlyJrfn591KsWiv0hOxq3rR+HL1lkgIf9tmrTxvuTjaIduK77CqSVLzsXi5C6JNoO7IpA==",
    #     "CONSENTMGR": "c1:0%7Cc3:0%7Cc5:0%7Cc6:0%7Cc7:0%7Cc8:0%7Cc9:1%7Cts:1678571379088%7Cconsent:true",
    #     "GPC_cookie_corrected": "true, ts:1678571379088,c3: 0,c7: 0,preferences",
    #     "utag_main": "v_id:0186d2917df90071d0c63c494a9402075003006d0093c$_sn:1$_se:8$_ss:0$_st:1678573775964$ses_id:1678569995774%3Bexp-session$_pn:8%3Bexp-session$fs_sample_user:false%3Bexp-session$dc_visit:1$dc_event:8%3Bexp-session$dc_region:eu-central-1%3Bexp-session",
    #     "RT": '"z=1&dm=ups.com&si=54a273ce-c7b5-4f23-a586-66c340c8811a&ss=lf4cnk6c&sl=w&tt=nwof&bcn=%2F%2F02179915.akstat.io%2F&ld=5rfdv&nu=4qf1pml7&cl=5v2u0&ul=5v2u4"',
    # }
    print(session.cookies.get_dict())
    return
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
        "loc": "en_IT",
        "IP_schType": "ns",
    }

    data = {
        "loc": "en_IT",
        "initiatingPage": "verification",
        "email1opt": "true",
        "addToAddressBook": "false",
        "email2opt": "true",
        "SUBMIT_BUTTON": "Next",
    }

    response = session.post(
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


def schedule(row: list, session: tls_client.Session):
    print_task("Scheduling pickup...", YELLOW)

    name = row[0].strip()
    surname = row[1].strip()
    phone = row[2].strip()
    address = row[3].strip()
    city = row[4].strip()
    zip_code = row[5].strip()
    country = row[6].strip()
    email = row[7].strip()

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

    data = f"operation=getAvailableDaysAndServices&address={address}&pd1=&pd2={city}&postalcode={zip_code}"
    try:
        response = session.post(
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
        dropoffdate = pickup_dict["PickupDates"][0]["DateValue"]

    except json.JSONDecodeError:
        print_task("JSONDecodeError", RED)
        time.sleep(3)
        return

    except KeyError:
        print_task("Keyerror check your address", RED)
        time.sleep(3)
        return

    payload = {
        "loc": country_dict[country.lower()],
        "gotoapp": "",
        "acctInfoDetails": "",
        "pickupInfoPageScheme": "",
        "selectedServices": "null",
        "EDITABLE_ACCTNUM": "FALSE",
        "localeValue": country_dict[country.lower()],
        "showPopup": "false",
        "facclosed": "false",
        "destslic": "null",
        "radioShipping": "Y",
        "tracknumlist": "",
        "accountnumber": "",
        "paramAcctZip": "",
        "company": name,
        "custname": name + " " + surname,
        "address": address,
        "room": "",
        "ROOM": "",
        "floor": "",
        "FLOOR": "",
        "pd2": city,
        "pd1": address,
        "postalcode": zip_code,
        "phone": phone,
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
        "dropoffdate": dropoffdate,
        "dropHour": "11",
        "dropMin": "00",
        "dropAMPM": "AM",
        "pickupdate": dropoffdate,
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
        "email1": email,
        "email2": "",
        "email3": "",
        "email4": "",
        "email5": "",
        "emailmessage": email,
        "failedemail": email,
    }

    try:
        response = session.post(
            "https://wwwapps.ups.com/pickup/api/service/validate/create",
            headers=headers,
            data=payload,
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

    return payment(session)


def session(row: list):
    session = tls_client.Session(client_identifier="chrome_105")

    print_task("Getting session...", PURPLE)

    try:
        if len(row[6]) > 2:
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
        "loc": country_dict[row[6].lower()],
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
        response = session.get(
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

    return schedule(row, session)


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
                time.sleep(3)
                os._exit(1)

            try:
                row = next(reader)
            except StopIteration:
                print_task("please fill Uzumaki/pickup/pickup_ups.csv", RED)
                input("Press Enter to exit...")
                os._exit(1)

            f.seek(0)
            reader = csv.reader(f)
            next(reader)

            print_task("Starting pickup ups...", CYAN)
            for row in reader:
                threading.Thread(target=session, args=(row,)).start()

    except FileNotFoundError:
        print_task("Uzumaki/pickup/pickup_ups not found", RED)
        input("Press Enter to exit...")
        return


country_dict = {
    "it": "en_IT",
    "es": "en_ES",
}
