from handler.utils import *
from internal.security import processRunning
import csv
import threading
import requests
from bs4 import BeautifulSoup
import tls_client

params = {
    "loc": "it_IT",
}


def get_first_token(session: requests.Session) -> dict:
    headers = {
        "authority": "wwwapps.ups.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://wwwapps.ups.com/pickup/processinfo?loc=it_IT",
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

    try:
        response = session.get(
            "https://wwwapps.ups.com/pickup/api/service/option/payment",
            params=params,
            headers=headers,
        )
        data = response.json()
        data = data["otherPaymentOptions"]
        data = data.replace("'", "")

    except Exception as e:
        print_task(e, RED)
        time.sleep
        os._exit(1)

    return data


def pickup(username):
    processRunning()
    setTitlePickup()

    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    try:
        with open("Uzumaki/pickup/ups.csv", "r") as f:
            reader = csv.reader(f)

            try:
                next(reader)
            except StopIteration:
                print_task("file is empty, delete it.", RED)
                time.sleep(3)
                os._exit(1)

            try:
                row = next(reader)
            except StopIteration:
                print_task("please fill Uzumaki/pickup/ups.csv", RED)
                input("Press Enter to exit...")
                os._exit(1)

            f.seek(0)
            reader = csv.reader(f)
            next(reader)

            print_task("Starting pickup ups...", CYAN)
            for row in reader:
                threading.Thread(target=session, args=(row,)).start()

    except FileNotFoundError:
        print_task("Uzumaki/geocode/geocode.csv not found", RED)
        input("Press Enter to exit...")
        return


dict_loc = {
    "IT": "it_IT",
    "FR": "en_FR",
    "ES": "en_ES",
}


def getToken(session: requests.Session, app_id: str, token: str, transaction_id: str):

    headers = {
    'authority': 'wwwapps.ups.com',
    'accept': 'application/json;charset=utf-8',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://wwwapps.ups.com',
    'pragma': 'no-cache',
    'referer': 'https://wwwapps.ups.com/pickup/processinfo?loc=it_IT',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'x-upscpc-rest-api-token': token,
    'x-upscpc-rest-app-id': app_id,
}

    params = {
    'transId': transaction_id,
}

    json_data = {
    'appId': app_id,
    'autoSavePayment': False,
    'showProfileRadio': False,
    'collectAddress': False,
    'validateAvs': False,
    'autoValidate': True,
    'newUPSAccount': False,
    'newPaymentCard': True,
    'newPayPalAccount': True,
    'newHPP': True,
    'existingUPSAccount': False,
    'existingPaymentCard': False,
    'existingPayPalAccount': False,
    'existingHPP': False,
    'numPackages': 0,
    'status': 0,
    'uiType': 1,
    'tAccount': '',
    'iobb': '',
    'ipAddress': '',
    'locale': 'it_IT',
    'token': token,
    'accountKey': '',
    'accountNumber': '',
    'rifAppId': '',
    'rifPrefix': '',
    'serviceLevelCode': '',
    'trackingNumber': '',
    'country': 'IT',
    'contextCountry': '',
    'profileCountry': '',
    'transactionId': transaction_id,
    'transactionSource': '',
    'userId': '',
    'showDefaultFlag': False,
    'returnTo': 'https://wwwapps.ups.com/pickup/processcpcpayment?loc=it_IT',
    'redirectTo': '',
    'cardTypeListFlag': 2,
    'useFloorLimits': True,
    'showBillingName': False,
    'showShipFrom': True,
    'useBillingAddress': False,
    'repop': False,
    'requiresRedirect': False,
    'showVatId': False,
    'showCashOption': True,
    'newCash': True,
}

    try:
        response = session.post(
            "https://wwwapps.ups.com/cpcws/api/v2/upsclients/init",
            params=params,
            headers=headers,
            json=json_data,
        )
        data = response.json()
        token = data["token"]
    except Exception as e:
        print_task("error getting token", RED)
        time.sleep(3)
        os._exit(1)

    return token


def checkout(session: requests.Session, row: list, dropoffdate: str):
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
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        # 'cookie': 'com.ups.pickup.cb.sData=15aca0690da64883a2e42738c6ab5fdf:xTVCseg/VRsHQv5Nwl1NAJXtGRw7WnXPp7b6Zl/6FMc=; bm_sz=7CB471EA39F68D5E740FF2723CB65745~YAAQgTRoaH+NKb6GAQAANPpdxBOsNmh/9RNYBc717hfbelE1XyqbtSOyneLvwQxpiCyNptLR27VGh74OiZJH2fIUyEjgMhcalv3Gj4E9v77hqeeAsbt01FsWFxr2jG0642TLd9htbRKXFsGRjaZ59EFqL6uEb3YgTLuCsiG2pV+ZOYbXXkCOOrDmhMqhbF75hRfIevqYqj/enL8W/HQETGsqwCASVHNuEojFj0YNqf9ZAgxMK3FPUrVBeUkay61u2roPF5QngAOLr++wmsZWxWx+HfvJIEXzHjwNTSQLP3k=~4339769~3747908; PIM-SESSION-ID=e9kDwp7iEzl9fBxS; com.ups.com_ups_GDOL.sData=99f51414df7d49b3b16c3591c669f54e:tDvKqc06ILw7Y0hob3CZPmwy8dQs/q5+lxnlq0alhgU=; sharedsession=4f874a9c-a142-47c1-8728-f85df1e1e5bc:w; s_fid=60E726A4E6DEA787-341517BABFA85A09; s_vnum=1680300000126%26vn%3D1; s_invisit=true; dayssincevisit_s=First%20Visit; s_cc=true; s_vi=[CS]v1|3204A825D6934D70-60000B0FC195765C[CE]; CONSENTMGR=consent:true%7Cts:1678332400820%7Cc1:1%7Cc3:0%7Cc5:1%7Cc6:1%7Cc7:0%7Cc8:1%7Cc9:1; GPC_cookie_corrected=true, ts:1678332400820,c3: 0,c7: 0; ups_language_preference=it_IT; _abck=0DD47936455CC42A2AB14DF31AB65E3B~0~YAAQgTRoaGDQKb6GAQAAlf3QxAmGr7w3tv9LdQ6FdZ5lrwDAMrhCRy5Pdv/7F4qQh9tBwrY3mpVdGIn8iOLsDLqERChBc3RkXxvKBepPa+Hq9KGsGUPEob+eHfZdUQ0TU7c4Tzg11604QD/eND5gtf+gNB8tCAXzYc7seHcBNDx/2QOtLuR63S08gkXPDDlDqprH1OwuuaDGYgJGrlN+xQM6YGLvoq/IzL6EGOtsacrPvEgwEOJTOx8xuuMPssM6ykR5rWL7M8/YZInfnc91gKB8J0ZvFlXGb+zS4IWRB26YjdBKNxHJ0nAsrpuQPaqG/U/UdtCVzIOIf5+187vJN0D1Gq58Od3qksN6RGNbOzT9SFpYtKVDFJvk5PV9JxFNkNc2dX4uYm8/zToY6jVKFCjp/NEN~-1~-1~1678342788; ak_bmsc=2EB40EAD13475EBDE58E4EB59301E1EB~000000000000000000000000000000~YAAQgTRoaGHQKb6GAQAAv//QxBP4wj8XU9G/WHthaM089ITyQ89aedTBpcCKxXv5YmOvCQFkxknZ41GJQ89hUx2Df03PJXf9JefM01UXLj9xTlUHnhp0Qy5T4EIiX1VIZx3XXG6v3pasz99svmsnNaA0t9MvSFHXUf14fCIrjXkYWY3Omuxyu+dZw4dV98OxDhAedq7rZv6LX2BplxUBDFz9l4M3rpMtv/3xwYRnJDyDhe6J7lKhprQp3p6p/++8X/qozAD57hINOLYk+nh0JMLiVZjWlfezlgd9wIIxMtwqtzN90yjpGyR6Oubfv2RRZcC0cd4hBeSVg1uxk4FfhzISzcuazt9gLdyoooJoah3wCuFmLC8W/DFnZsimDvWcrTKenEr3MBM5cAV6ZG9v6cxIQc9Nrw6EavumR2tDo2kGNaL1KL/SHCT84Gww0njsG2NlCWgT2OoVYjJJwJZr7dPNgsJh44EPlLscrzimqxbCTBOu3uGgmw==; AKA_A2=A; utag_main=v_id:0186c45dfc1a00016a91badd772b04075003106d0093c$_sn:3$_se:4$_ss:0$_st:1678341312886$dc_visit:3$vapi_domain:ups.com$_prevpageid:shipping%2FIntPickup%2Fpic(1sch).html%3Bexp-1678343113298$_prevpage:wwwapps%3Ait%3Ait%3Apickup%3Aschedule%3Bexp-1678343113297$ses_id:1678339275871%3Bexp-session$_pn:4%3Bexp-session$fs_sample_user:false%3Bexp-session$dc_event:4%3Bexp-session; s_nr=1678339556710-New; dayssincevisit=1678339556711',
        "origin": "https://wwwapps.ups.com",
        "pragma": "no-cache",
        "referer": "https://wwwapps.ups.com/pickup/schedule?loc=it_IT",
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
    standard_service = "007#001"
    weight = "2"
    numberOfPackages = "1"
    numberOfPallets = "1"

    payload = {
        "loc": "it_IT",
        "gotoapp": "",
        "acctInfoDetails": "",
        "pickupInfoPageScheme": "",
        "selectedServices": "null",
        "EDITABLE_ACCTNUM": "FALSE",
        "localeValue": "it_IT",
        "showPopup": "false",
        "facclosed": "false",
        "destslic": "null",
        "radioShipping": "Y",
        "tracknumlist": "",
        "accountnumber": "",
        "paramAcctZip": "",
        "company": name + " " + surname,
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
        "numberOfPackages": numberOfPackages,
        "weight": weight,
        "numberOfPallets": numberOfPallets,
        "palletweight": "",
        "pallettotweight": "",
        "length": "",
        "width": "",
        "height": "",
        "palletSizeOpts": "0",
        "paramServices": standard_service,
        "radioWeight70": "N",
        "radioComDocs": "N",
        "exppickup": "0",
        "dropoffdate": dropoffdate,
        "dropHour": "11",
        "dropMin": "00",
        "dropAMPM": "AM",
        "pickupdate": dropoffdate,
        "readyHours": "6",
        "readyMinutes": "30",
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
            "https://wwwapps.ups.com/pickup/processinfo",
            params=params,
            headers=headers,
            data=payload,
        )
        soup = BeautifulSoup(response.text, "html.parser")

        payment = soup.find("div", {"class": "appHead clearfix"}).text

    except Exception as e:
        print_task("Error: " + str(e), RED)
        return

    if payment.strip() not in response.text:
        print_task("Error: " + payment, RED)
        time.sleep(3)
        return

    print_task("Submitting payment...", YELLOW)

    data = get_first_token(session)
    data = json.loads(data)
    token = data["token"]
    transaction_id = data["transactionId"]
    app_id = data["appId"]

    rest_api_token = getToken(session, app_id, token, transaction_id)

    headers = {
        "authority": "wwwapps.ups.com",
        "accept": "application/json;charset=utf-8",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://wwwapps.ups.com",
        "pragma": "no-cache",
        "referer": "https://wwwapps.ups.com/pickup/processinfo?loc=it_IT",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "x-upscpc-rest-api-token": rest_api_token,
        "x-upscpc-rest-app-id": app_id,
    }

    json_data = {
        "@type": "Card",
        "options": {
            "transactionId": transaction_id,
            "rifAppId": "CPC",
            "rifPrefix": "cpcWidget",
            "storeBA": False,
            "defaultPaymentMethod": False,
            "storePaymentMethod": False,
            "uuid": "",
            "destinationAddress": {},
            "originAddress": {},
            "userId": "",
            "iobb": "",
            "validateAddress": False,
        },
        "paymentMediaTypeCode": "02",
        "chargeTypeCode": "06",
        "validateAVS": False,
        "billingAddress": {
            "firstName": "emanuele",
            "lastName": "ardinghi",
            "addressLine1": "via orcagna 66",
            "addressLine2": "",
            "addressLine3": "",
            "city": "firenze",
            "state": "Agrigento",
            "country": "IT",
            "postalCode": "50121",
        },
        "cardNumber": "5354564980010000",
        "cardType": "02_06",
        "cvv": "199",
        "expiryMonth": 2,
        "expiryYear": 2026,
        "taxId": "RDNMNL02T07D612C",
        "pecEmailAddress": "",
        "sdiSystemCode": "",
        "taxIdTypeCode": "0005",
    }

    response = session.post(
        f"https://wwwapps.ups.com/cpcws/api/v2/payments/{transaction_id}/store",
        headers=headers,
        json=json_data,
    )
    print(response.url)
    print(response.text)


def schedule(row: list, session: requests.Session):
    print_task("Scheduling pickup...", PURPLE)

    name = row[0].strip()
    surname = row[1].strip()
    phone = row[2].strip()
    address = row[3].strip()
    city = row[4].strip()
    zip_code = row[5].strip()
    country = row[6].strip()
    email = row[7].strip()

    loc = dict_loc[country.upper()]

    headers = {
        "authority": "wwwapps.ups.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://wwwapps.ups.com",
        "pragma": "no-cache",
        "referer": "https://wwwapps.ups.com/pickup/schedule?loc=en_IT",
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
    standard_service = "007#001"
    weight = "2"
    numberOfPackages = "1"
    numberOfPallets = "1"

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

    payload = {
        "loc": "it_IT",
        "gotoapp": "",
        "acctInfoDetails": "",
        "pickupInfoPageScheme": "",
        "selectedServices": "null",
        "EDITABLE_ACCTNUM": "FALSE",
        "localeValue": "it_IT",
        "showPopup": "false",
        "facclosed": "false",
        "destslic": "null",
        "radioShipping": "Y",
        "tracknumlist": "",
        "accountnumber": "",
        "paramAcctZip": "",
        "company": name + " " + surname,
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
        "numberOfPackages": numberOfPackages,
        "weight": weight,
        "numberOfPallets": numberOfPallets,
        "palletweight": "",
        "pallettotweight": "",
        "length": "",
        "width": "",
        "height": "",
        "palletSizeOpts": "0",
        "paramServices": standard_service,
        "radioWeight70": "N",
        "radioComDocs": "N",
        "exppickup": "0",
        "dropoffdate": dropoffdate,
        "dropHour": "11",
        "dropMin": "00",
        "dropAMPM": "AM",
        "pickupdate": dropoffdate,
        "readyHours": "4",
        "readyMinutes": "55",
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

    if data["valid"] == True:
        print_task("Starting booking...", PURPLE)
        return checkout(session, row, dropoffdate)
    else:
        print_task("Unknown error", RED)
        time.sleep(3)
        return


def session(row: list):
    country = row[6].strip()

    session = tls_client.Session(client_identifier="chrome_105")
    print_task("Getting session...", PURPLE)

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
        loc_len = len(country)
        if loc_len != 2:
            print_task(f"{country} country must be 2 characters", RED)
            time.sleep(3)
            return
    except TypeError:
        print_task(f"{country} country must be 2 characters", RED)
        time.sleep(3)
        return

    try:
        loc = dict_loc[country.upper()]
    except KeyError:
        print_task(f"{country.upper()} country not supported", RED)
        time.sleep(3)
        return

    params = {
        "loc": loc,
    }

    try:
        response = session.get(
            "https://wwwapps.ups.com/pickup/schedule", params=params, headers=headers
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

    if "Inserimento dei dati sul ritiro" in response.text:
        return schedule(row, session)
    else:
        print_task("Error getting session", RED)
        time.sleep(3)
        return


# remember to change ==>dropoffdate
