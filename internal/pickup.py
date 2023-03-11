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

    headers = {
        "authority": "wwwapps.ups.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
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
        "x-requested-with": "XMLHttpRequest",
    }

    payload_cc = {
        "loc": "it_IT",
        "op": "NEXT",
        "billingindicator": hargeTypeCode,
        "paymentYourUPSAccountNumber": "",
        "paymentUPSPostalCode": "",
        "paymentThirdPartybillingIndicator": "billThirdForPickupCharges",
        "paymentThirdPartyAccountNumber": "",
        "paymentReceiverCountry": "IT",
        "paymentThirdPartyCountry": "IT",
        "paymentThirdPartyPostalCode": "",
        "paymentMethodValidated": "true",
        "paymentCard": "",
        "otherPaymentType": "Card",
        "pre": "cpcWidget",
        "rapp": "CPC",
        "cct": f"{paymentMediaTypeCode}_{hargeTypeCode}",
        "pmt": "2",
        "apy": "true",
        "ptr": "false",
        "spm": "",
        "dpm": "",
        "epm": "false",
        "is3d": "",
        "accountNumber": "",
        "accountName": "",
        "IT": "IT",
        "null": "",
        "cpcWidgetCountryCashCountry": "IT",
        "cpcWidgetCountryCashPostalCode": "",
        "cpcWidgetCountryCashCity": "",
        "cpcWidgetCountryCashStates": "",
        "ccn": credit_card,
        "sccn": "",
        "svc": month,
        "exm": month,
        "exy": year,
        "eba": "",
        "cba": "",
        "sba": "",
        "baid": "",
        "pid": "",
        "pem": "",
        "ppan": "",
        "cpcWidgetCountryCountry": "IT",
        "cpcWidgetCountryPostalCode": "",
        "cpcWidgetCountryCity": "",
        "cpcWidgetCountryStates": "",
        "addressSelect": "newAddress",
        "cpcWidgetFirstName": name,
        "cpcWidgetLastName": surname,
        "cpcWidgetCountry": "IT",
        "cpcWidgetAddress1": address,
        "cpcWidgetAddress2": "",
        "cpcWidgetAddress3": "",
        "cpcWidgetPostalCode": zip_code,
        "cpcWidgetCity": city,
        "cpcWidgetStates": city,
        "taxIdTypeCode": "0005",
        "taxId": tax_id,
        "pecId": tax_id,
        "sdiId": tax_id,
        "tracknumlist": "",
    }

    response = session.post(
        "https://wwwapps.ups.com/pickup/api/service/validate/payment",
        headers=headers,
        data=payload_cc,
    )

    data_ = response.json()
    if data_["valid"] != True:
        print_task("Error checkout: " + data["errorList"], RED)
        time.sleep(3)
        return

    headers = {
        "authority": "wwwapps.ups.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://wwwapps.ups.com",
        "pragma": "no-cache",
        "referer": "https://wwwapps.ups.com/pickup/processinfo?loc=it_IT",
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

    response = session.post(
        "https://wwwapps.ups.com/pickup/processpaymentdetail",
        headers=headers,
        data=payload_cc,
    )

    if "Nome referente:" not in response.text:
        print_task("Error checkout: " + response.text, RED)
        time.sleep(3)
        return

    headers = {
        "authority": "wwwapps.ups.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://wwwapps.ups.com",
        "pragma": "no-cache",
        "referer": "https://wwwapps.ups.com/pickup/processpaymentdetail",
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

    pay = {
        "loc": "it_IT",
        "IP_schType": "ns",
    }

    data = {
        "loc": "it_IT",
        "initiatingPage": "verification",
        "email1opt": "true",
        "addToAddressBook": "false",
        "email2opt": "true",
        "SUBMIT_BUTTON": "Avanti",
    }

    response = session.post(
        "https://wwwapps.ups.com/pickup/processverification",
        params=pay,
        headers=headers,
        data=data,
    )

    headers = {
        "authority": "www.ups.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-site",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }

    check = {
        "type": "3d",
        "transactionId": transaction_id,
        "returnTo": "https://wwwapps.ups.com/pickup/processcpcpayment?loc=it_IT",
    }

    response = session.get(
        "https://www.ups.com/cpcws/redirect", params=check, headers=headers
    )

    print_task("Payment submitted!", GREEN)


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
