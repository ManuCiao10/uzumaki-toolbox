from handler.utils import *
from internal.security import processRunning
import csv
import threading
import requests
from bs4 import BeautifulSoup
import tls_client
from codicefiscale import codicefiscale

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


def getToken(session: requests.Session, app_id: str, token: str, transaction_id: str):
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
        "x-upscpc-rest-api-token": token,
        "x-upscpc-rest-app-id": app_id,
    }

    params = {
        "transId": transaction_id,
    }

    json_data = {
        "appId": app_id,
        "autoSavePayment": False,
        "showProfileRadio": False,
        "collectAddress": False,
        "validateAvs": False,
        "autoValidate": True,
        "newUPSAccount": False,
        "newPaymentCard": True,
        "newPayPalAccount": True,
        "newHPP": True,
        "existingUPSAccount": False,
        "existingPaymentCard": False,
        "existingPayPalAccount": False,
        "existingHPP": False,
        "numPackages": 0,
        "status": 0,
        "uiType": 1,
        "tAccount": "",
        "iobb": "",
        "ipAddress": "",
        "locale": "it_IT",
        "token": token,
        "accountKey": "",
        "accountNumber": "",
        "rifAppId": "",
        "rifPrefix": "",
        "serviceLevelCode": "",
        "trackingNumber": "",
        "country": "IT",
        "contextCountry": "",
        "profileCountry": "",
        "transactionId": transaction_id,
        "transactionSource": "",
        "userId": "",
        "showDefaultFlag": False,
        "returnTo": "https://wwwapps.ups.com/pickup/processcpcpayment?loc=it_IT",
        "redirectTo": "",
        "cardTypeListFlag": 2,
        "useFloorLimits": True,
        "showBillingName": False,
        "showShipFrom": True,
        "useBillingAddress": False,
        "repop": False,
        "requiresRedirect": False,
        "showVatId": False,
        "showCashOption": True,
        "newCash": True,
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
        print_task("error getting token" + str(e), RED)
        time.sleep(3)
        os._exit(1)

    return token


def checkout(session: requests.Session, row: list, dropoffdate: str):
    print_task("Starting booking...", PURPLE)

    name = row[0].strip()
    surname = row[1].strip()
    phone = row[2].strip()
    address = row[3].strip()
    city = row[4].strip()
    zip_code = row[5].strip()
    email = row[6].strip()
    credit_card = row[7].strip()
    month = row[8].strip()
    year = row[9].strip()
    cvv = row[10].strip()

    if month[0] == "0":
        month = month[1]

    headers = {
        "authority": "wwwapps.ups.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
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

    if credit_card[0] == "4":
        hargeTypeCode = "06"
    else:
        hargeTypeCode = "04"

    tax_id = codicefiscale.encode(
        surname=surname, name=name, sex="M", birthdate="03/04/1985", birthplace=city
    )

    paymentMediaTypeCode = "02"
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
        "paymentMediaTypeCode": paymentMediaTypeCode,
        "chargeTypeCode": hargeTypeCode,
        "validateAVS": False,
        "billingAddress": {
            "firstName": name,
            "lastName": surname,
            "addressLine1": address,
            "addressLine2": "",
            "addressLine3": "",
            "city": city,
            "state": city,
            "country": "IT",
            "postalCode": zip_code,
        },
        "cardNumber": credit_card,
        "cardType": f"{paymentMediaTypeCode}_{hargeTypeCode}",
        "cvv": cvv,
        "expiryMonth": month,
        "expiryYear": year,
        "taxId": tax_id,
        "pecEmailAddress": "",
        "sdiSystemCode": "",
        "taxIdTypeCode": "0005",
    }
    try:
        response = session.post(
            f"https://wwwapps.ups.com/cpcws/api/v2/payments/{transaction_id}/store",
            headers=headers,
            json=json_data,
        )
        data = response.json()
    except Exception as e:
        print_task("Error checkout: " + str(e), RED)
        time.sleep(3)
        return

    try:
        if data["status"] == 400:
            message = data["processingError"]["message"]
            print_task("Error checkout: " + message, RED)
            time.sleep(3)
            return
    except:
        pass

    print_task("Payment submitted!", GREEN)

    headers = {
    'authority': 'wwwapps.ups.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
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
    'x-requested-with': 'XMLHttpRequest',
}

    data = {
    'loc': 'it_IT',
    'op': 'NEXT',
    'billingindicator': '04',
    'paymentYourUPSAccountNumber': '',
    'paymentUPSPostalCode': '',
    'paymentThirdPartybillingIndicator': 'billThirdForPickupCharges',
    'paymentThirdPartyAccountNumber': '',
    'paymentReceiverCountry': 'IT',
    'paymentThirdPartyCountry': 'IT',
    'paymentThirdPartyPostalCode': '',
    'paymentMethodValidated': 'true',
    'paymentCard': '',
    'otherPaymentType': 'Card',
    'pre': 'cpcWidget',
    'rapp': 'CPC',
    'cct': '02_04',
    'pmt': '2',
    'apy': 'true',
    'ptr': 'false',
    'spm': '',
    'dpm': '',
    'epm': 'false',
    'is3d': '',
    'accountNumber': '',
    'accountName': '',
    'IT': 'IT',
    'null': '',
    'cpcWidgetCountryCashCountry': 'IT',
    'cpcWidgetCountryCashPostalCode': '',
    'cpcWidgetCountryCashCity': '',
    'cpcWidgetCountryCashStates': '',
    'ccn': '5354564980016154',
    'sccn': '',
    'svc': '199',
    'exm': '2',
    'exy': '2026',
    'eba': '',
    'cba': '',
    'sba': '',
    'baid': '',
    'pid': '',
    'pem': '',
    'ppan': '',
    'cpcWidgetCountryCountry': 'IT',
    'cpcWidgetCountryPostalCode': '',
    'cpcWidgetCountryCity': '',
    'cpcWidgetCountryStates': '',
    'addressSelect': 'newAddress',
    'cpcWidgetFirstName': 'emanuele',
    'cpcWidgetLastName': 'ardinghi',
    'cpcWidgetCountry': 'IT',
    'cpcWidgetAddress1': 'via orcagna 66',
    'cpcWidgetAddress2': '',
    'cpcWidgetAddress3': '',
    'cpcWidgetPostalCode': '50121',
    'cpcWidgetCity': 'firenze',
    'cpcWidgetStates': 'Agrigento',
    'taxIdTypeCode': '0005',
    'taxId': 'RDNMNL02T07D612C',
    'pecId': 'emanuele.ardinghi@gmail.com',
    'sdiId': 'emanuele.ardinghi@gmail.com',
    'tracknumlist': '',
}

    response = session.post(
    'https://wwwapps.ups.com/pickup/api/service/validate/payment',
    headers=headers,
    data=data,
)

    data_ = response.json()
    if data_["valid"] != True:
        print_task("Error checkout: " + data["errorList"], RED)
        time.sleep(3)
        return

    headers = {
    'authority': 'wwwapps.ups.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    # 'cookie': 'com.ups.pickup.cb.sData=9c4b5ebaedfc40e8bb1896b25fa2d71f:kfVr0QH3Tq2cPNbfivAKyQYD8xiiMtBq3bxdYbyhWQg=; ups_language_preference=it_IT; PIM-SESSION-ID=HsQVb9cxHucp9q5C; bm_sz=CB528A049C34C35AA336F4F481F94470~YAAQVH4ZuAkDbcKGAQAAbX0ByBPyoIoTZnu/39L1YkPmNPRUcIZ7abFdk/ueeqywKwnRlamiVQ9rbRgyg+pJUB12lKlGzoytkbhwPTrBLpjI5kksbDd1wERQo6whFF9UywLcPs9zxLo5dSVnW4FCoTqYuiAgE0nkKC+lhZceW25u+ckr246yQvBM48b++L41xL1obqrseL1bv4TM+gJW8PqeC0BgwCRACbHgM6hseCPkvZoiCjVfFwNG94ObMD/tBQIYmt6jT5+7U1IMKB1Mn5D0UstStxRtuJCafUW9jqE=~3485763~4605497; sharedsession=b897e593-da08-4f11-bfdd-28c2ea292c92:w; AKA_A2=A; _abck=22D48C5448777CF224D9F73DA0194E17~0~YAAQgTRoaKVcRL6GAQAAtfOFyAlfx/iQletw42iEWhgltvhdWx/CXzkL5pBP4Cr0dGr8xN759vplmKyE9dscOcsO0arpoDFMWEQmdMLR8pcpfNKz2EZxKjsf0Hmq5AkHz3rRIRg3p0+IoLezIrH9DbO9vFP5t6hlLJ6NXLjJCTQ+M+chGoMFu0M3i4elF+nuY2kY+jwS0GCDYHI9Fufq8Fh+3+wjQnk3NIWjCMEJdTvikZhF9a6BCkgl3BN3uoH7fLP0jKUbRi3Vf08wam0E6ifQBNGDyL7f27SqON6cZZdRn7l64rrA5tp6jgyWh4Wq94kKCYepLVJ2D7rrjPHHIofdjK7Ubr7yjltCMw7ntfiJG87KGRTV6Z4GFSiNHgkUYCSmIjN99RYGnJVIxotwqNhoPtIf~-1~-1~1678404971; utag_main=v_id:0186c50a393b00385f9fcffc36b004075003106d0093c$_sn:5$_se:9$_ss:0$_st:1678403267081$dc_visit:5$ses_id:1678397910882%3Bexp-session$_pn:9%3Bexp-session$fs_sample_user:false%3Bexp-session$dc_event:9%3Bexp-session; ak_bmsc=D99B98E3557651362E083AB119BA059D~000000000000000000000000000000~YAAQgTRoaMpcRL6GAQAAYf6FyBNkX970HqSDcemq0Bblh3ovbHm38IqmOTU15wPPxXy6G3jPbPk5hlosGHI37hlensidQ6L1qf7NdeLBRCGizvqSqfdp2u9BPnm5ujKX6HEcJL7Ab8v7yvVSdxsLlQxiPdbm6jqJz2IEknJVw/s8wuE7b8D2GV1PynzBgfl0Jl4JSjxK9XO3GNdXie+L3pWTTPFW+sQw1P3E9nB0FbKuVsutMYovWQ3+RgEJDOQiQ3AUYIW0T/JcTGYYN8eGe9kvVmKd9/zyTJPhiYwK98OtkZfpXylaqo81x3rcdD9iSrMBOUT8C4h9DaGCwgC8VGaWhZJ0AULf6T82EtBf6i4RZLYPU5skLUKGIkdLAjlxLvC1QcDe+6TNsjtoppEMglvyLhkSH2PlVEoUC7KO5U/9OQggle1Z7BTrUbZJ4RXpWFuNF5vaCEl6nSS+9aEmT4PsPfVzjolhiFbj2sdcJB0CCu7P4WwtsA==',
    'origin': 'https://wwwapps.ups.com',
    'pragma': 'no-cache',
    'referer': 'https://wwwapps.ups.com/pickup/processinfo?loc=it_IT',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

    data = {
    'loc': 'it_IT',
    'op': 'NEXT',
    'billingindicator': '04',
    'paymentYourUPSAccountNumber': '',
    'paymentUPSPostalCode': '',
    'paymentThirdPartybillingIndicator': 'billThirdForPickupCharges',
    'paymentThirdPartyAccountNumber': '',
    'paymentReceiverCountry': 'IT',
    'paymentThirdPartyCountry': 'IT',
    'paymentThirdPartyPostalCode': '',
    'paymentMethodValidated': 'true',
    'paymentCard': '',
    'otherPaymentType': 'Card',
    'pre': 'cpcWidget',
    'rapp': 'CPC',
    'cct': '02_04',
    'pmt': '2',
    'apy': 'true',
    'ptr': 'false',
    'spm': '',
    'dpm': '',
    'epm': 'false',
    'is3d': '',
    'accountNumber': '',
    'accountName': '',
    'IT': 'IT',
    'null': '',
    'cpcWidgetCountryCashCountry': 'IT',
    'cpcWidgetCountryCashPostalCode': '',
    'cpcWidgetCountryCashCity': '',
    'cpcWidgetCountryCashStates': '',
    'ccn': '5354564980016154',
    'sccn': '',
    'svc': '199',
    'exm': '2',
    'exy': '2026',
    'eba': '',
    'cba': '',
    'sba': '',
    'baid': '',
    'pid': '',
    'pem': '',
    'ppan': '',
    'cpcWidgetCountryCountry': 'IT',
    'cpcWidgetCountryPostalCode': '',
    'cpcWidgetCountryCity': '',
    'cpcWidgetCountryStates': '',
    'addressSelect': 'newAddress',
    'cpcWidgetFirstName': 'emanuele',
    'cpcWidgetLastName': 'ardinghi',
    'cpcWidgetCountry': 'IT',
    'cpcWidgetAddress1': 'via orcagna 66',
    'cpcWidgetAddress2': '',
    'cpcWidgetAddress3': '',
    'cpcWidgetPostalCode': '50121',
    'cpcWidgetCity': 'firenze',
    'cpcWidgetStates': 'Agrigento',
    'taxIdTypeCode': '0005',
    'taxId': 'RDNMNL02T07D612C',
    'pecId': 'emanuele.ardinghi@gmail.com',
    'sdiId': 'emanuele.ardinghi@gmail.com',
    'tracknumlist': '',
}

    response = session.post('https://wwwapps.ups.com/pickup/processpaymentdetail', headers=headers, data=data)
    # print(response.text)
    if "Nome referente:" in response.text:
        print("OK")
    else:
        print("ERROR")
        return 
    
    headers = {
    'authority': 'wwwapps.ups.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'origin': 'https://wwwapps.ups.com',
    'pragma': 'no-cache',
    'referer': 'https://wwwapps.ups.com/pickup/processpaymentdetail',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

    ciao = {
    'loc': 'it_IT',
    'IP_schType': 'ns',
}

    data = {
    'loc': 'it_IT',
    'initiatingPage': 'verification',
    'email1opt': 'true',
    'addToAddressBook': 'false',
    'email2opt': 'true',
    'SUBMIT_BUTTON': 'Avanti',
}

    response = session.post(
    'https://wwwapps.ups.com/pickup/processverification',
    params=ciao,
    headers=headers,
    data=data,
)

    headers = {
    'authority': 'www.ups.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    # 'cookie': 'JSESSIONID=AC1FB2B53FF8D6BECAB2B7FB78079ED3; .AspNetCore.Antiforgery.XlURHxPT8_I=CfDJ8H1SCHo8oO5Ascce1J42d2D6fIPzHeg3ZFicAqZ8baHosXPMw0t1rDtl6sSO7xkEyhWiyDSorPHWdfleYbdWcA7DH4Hgy2OaQxsg10unKw5kchiVupZSbnisXHtIEXxUjfS-AVYPVfXrsX95xVTTT-A; .AspNetCore.Antiforgery.pKFBCrPAOmA=CfDJ8H1SCHo8oO5Ascce1J42d2Cgfn0OxlXNuFNMWE5cJZFkZ5PBRNxfAnechdZcNqTJJj8cuDIn8SUAUmBnSrjUKn2sV1CmZM9snEOfzlVwEjJwCBSgzRmQfrOJSeswJcDa1YhIldb2ASoco-YPPiVwPuA; gig_canary=false; gig_canary_ver=13549-3-27869190; GPC_cookie_corrected=true, ts:1678332400820,c3: 0,c7: 0,preferences; ups_language_preference=it_IT; PIM-SESSION-ID=HsQVb9cxHucp9q5C; bm_sz=CB528A049C34C35AA336F4F481F94470~YAAQVH4ZuAkDbcKGAQAAbX0ByBPyoIoTZnu/39L1YkPmNPRUcIZ7abFdk/ueeqywKwnRlamiVQ9rbRgyg+pJUB12lKlGzoytkbhwPTrBLpjI5kksbDd1wERQo6whFF9UywLcPs9zxLo5dSVnW4FCoTqYuiAgE0nkKC+lhZceW25u+ckr246yQvBM48b++L41xL1obqrseL1bv4TM+gJW8PqeC0BgwCRACbHgM6hseCPkvZoiCjVfFwNG94ObMD/tBQIYmt6jT5+7U1IMKB1Mn5D0UstStxRtuJCafUW9jqE=~3485763~4605497; sharedsession=b897e593-da08-4f11-bfdd-28c2ea292c92:w; JSESSIONID=D0A48FDE522AA84A9538F9F684003C21; _abck=22D48C5448777CF224D9F73DA0194E17~0~YAAQgTRoaKVcRL6GAQAAtfOFyAlfx/iQletw42iEWhgltvhdWx/CXzkL5pBP4Cr0dGr8xN759vplmKyE9dscOcsO0arpoDFMWEQmdMLR8pcpfNKz2EZxKjsf0Hmq5AkHz3rRIRg3p0+IoLezIrH9DbO9vFP5t6hlLJ6NXLjJCTQ+M+chGoMFu0M3i4elF+nuY2kY+jwS0GCDYHI9Fufq8Fh+3+wjQnk3NIWjCMEJdTvikZhF9a6BCkgl3BN3uoH7fLP0jKUbRi3Vf08wam0E6ifQBNGDyL7f27SqON6cZZdRn7l64rrA5tp6jgyWh4Wq94kKCYepLVJ2D7rrjPHHIofdjK7Ubr7yjltCMw7ntfiJG87KGRTV6Z4GFSiNHgkUYCSmIjN99RYGnJVIxotwqNhoPtIf~-1~-1~1678404971; ak_bmsc=D99B98E3557651362E083AB119BA059D~000000000000000000000000000000~YAAQgTRoaMpcRL6GAQAAYf6FyBNkX970HqSDcemq0Bblh3ovbHm38IqmOTU15wPPxXy6G3jPbPk5hlosGHI37hlensidQ6L1qf7NdeLBRCGizvqSqfdp2u9BPnm5ujKX6HEcJL7Ab8v7yvVSdxsLlQxiPdbm6jqJz2IEknJVw/s8wuE7b8D2GV1PynzBgfl0Jl4JSjxK9XO3GNdXie+L3pWTTPFW+sQw1P3E9nB0FbKuVsutMYovWQ3+RgEJDOQiQ3AUYIW0T/JcTGYYN8eGe9kvVmKd9/zyTJPhiYwK98OtkZfpXylaqo81x3rcdD9iSrMBOUT8C4h9DaGCwgC8VGaWhZJ0AULf6T82EtBf6i4RZLYPU5skLUKGIkdLAjlxLvC1QcDe+6TNsjtoppEMglvyLhkSH2PlVEoUC7KO5U/9OQggle1Z7BTrUbZJ4RXpWFuNF5vaCEl6nSS+9aEmT4PsPfVzjolhiFbj2sdcJB0CCu7P4WwtsA==; AKA_A2=A; utag_main=v_id:0186c50a393b00385f9fcffc36b004075003106d0093c$_sn:5$_se:11$_ss:0$_st:1678403887471$dc_visit:5$ses_id:1678397910882%3Bexp-session$_pn:11%3Bexp-session$fs_sample_user:false%3Bexp-session$dc_event:11%3Bexp-session',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-site',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

    ciao3 = {
    'type': '3d',
    'transactionId': '1913693053',
    'returnTo': 'https://wwwapps.ups.com/pickup/processcpcpayment?loc=it_IT',
}
    print(transaction_id)
    response = session.get('https://www.ups.com/cpcws/redirect', params=ciao3, headers=headers)
    print(response.url)
    print(response.status_code)
    print(response.text)


def schedule(row: list, session: requests.Session):
    print_task("Scheduling pickup...", YELLOW)

    name = row[0].strip()
    surname = row[1].strip()
    phone = row[2].strip()
    address = row[3].strip()
    city = row[4].strip()
    zip_code = row[5].strip()
    email = row[6].strip()

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

    except KeyError:
        print_task("Keyerror check your address", RED)
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

    if data["valid"] != True:
        print_task("Unknown error", RED)
        time.sleep(3)
        return

    return checkout(session, row, dropoffdate)


def session(row: list):
    session = tls_client.Session(client_identifier="chrome_105")
    print_task("Getting session...", PURPLE)

    try:
        len_month = len(row[8].strip())
        if len_month != 2:
            print_task("month must be 2 digits", RED)
            time.sleep(3)
            return
    except:
        pass

    try:
        len_year = len(row[9].strip())
        if len_year != 4:
            row[9] = "20" + row[9]
    except:
        pass

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

    if "Inserimento dei dati sul ritiro" not in response.text:
        print_task("Error getting session response[2]", RED)
        time.sleep(3)
        return

    return schedule(row, session)


# remember to change ==>dropoffdate
