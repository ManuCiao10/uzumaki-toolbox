from handler.utils import *
from internal.security import processRunning
import csv
import threading
import requests


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
    "IT": "en_IT",
    "FR": "en_FR",
    "ES": "en_ES",
}


def checkout(session: requests.Session, payload: dict, loc: str):
    headers = {
        "authority": "wwwapps.ups.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        # 'cookie': 'com.ups.pickup.cb.sData=15aca0690da64883a2e42738c6ab5fdf:xTVCseg/VRsHQv5Nwl1NAJXtGRw7WnXPp7b6Zl/6FMc=; bm_sz=7CB471EA39F68D5E740FF2723CB65745~YAAQgTRoaH+NKb6GAQAANPpdxBOsNmh/9RNYBc717hfbelE1XyqbtSOyneLvwQxpiCyNptLR27VGh74OiZJH2fIUyEjgMhcalv3Gj4E9v77hqeeAsbt01FsWFxr2jG0642TLd9htbRKXFsGRjaZ59EFqL6uEb3YgTLuCsiG2pV+ZOYbXXkCOOrDmhMqhbF75hRfIevqYqj/enL8W/HQETGsqwCASVHNuEojFj0YNqf9ZAgxMK3FPUrVBeUkay61u2roPF5QngAOLr++wmsZWxWx+HfvJIEXzHjwNTSQLP3k=~4339769~3747908; PIM-SESSION-ID=e9kDwp7iEzl9fBxS; ak_bmsc=1E4482440C87BC23FCF7B2E24F7EACF4~000000000000000000000000000000~YAAQgTRoaIONKb6GAQAAGf9dxBNRqrd/w8KCU+Cw6Xqf7QqxH93ZY0+aCoXdvVUUIWD9A9g+kOp0hLAqvtJrBnMyIvzGCC0KPyjNeutY8Z+SytiufvMhSsqxkZ7hDcw4pILdxW0AlKd9hFuofJwA9myzUzl/Gu+MFxE+/CChx58LbUr+Gbmo5Kf5GKxoBoCefhV3o3IUSGY3y1MRAsKITZiIfdiXn5EYIVTPTeuqjDon91eEY7+PNr8j6lTr78M4FX4ICbY050kNEWWixDo3XXqKbmMA48XFoBT9QRBmHLMQrvoukuHdf7lcPxlenGN78+ttHe4t+8Ps6U01OoTRtsKPPLS4rvGCTdCrZvvVfnr7NjfLUDSjtsHUBSXN17cXNRtnfU9hWo+iVnF6hH+v1NkF1X/xovYI8aq3zxFtkN4jC0zBMnnraIGrtKh6ozI5aulwhk9w7B/aBgW03ejNUdWGPZ8zRKP0iZZjAEZ6pVH64psyCFn/lQ==; com.ups.com_ups_GDOL.sData=99f51414df7d49b3b16c3591c669f54e:tDvKqc06ILw7Y0hob3CZPmwy8dQs/q5+lxnlq0alhgU=; sharedsession=4f874a9c-a142-47c1-8728-f85df1e1e5bc:w; s_fid=60E726A4E6DEA787-341517BABFA85A09; s_vnum=1680300000126%26vn%3D1; s_invisit=true; dayssincevisit_s=First%20Visit; s_cc=true; s_vi=[CS]v1|3204A825D6934D70-60000B0FC195765C[CE]; CONSENTMGR=consent:true%7Cts:1678332400820%7Cc1:1%7Cc3:0%7Cc5:1%7Cc6:1%7Cc7:0%7Cc8:1%7Cc9:1; GPC_cookie_corrected=true, ts:1678332400820,c3: 0,c7: 0; _abck=0DD47936455CC42A2AB14DF31AB65E3B~0~YAAQgTRoaFqqKb6GAQAAu3yWxAmXP0JluZYiQJCGN72euIAXi3/I04KgRjKTCpT8LpEi/Goy1PIT0wxK/MVCWI/T2hRE/qdi9iVVooLp4cvWomAQG1uFzDEtsR9GaHcTn9Vidox1Jwp4JiAftSvYp4wD3uKTG4y+00+7WKMg63XA+2jJ7/9oO7Mp7u2v28Rdp7Yni5n3IGgPUYCNemLlCQQGr+qEP002OuIXtnIY5yOIJEdpd7CC1hXebnGodb1CR8wff44GO8WagkqFOS3qmd9CfqvTzOUM0JfLMz7LIZkThZijZPMPegpnlt6/ZXS4X7QzGFCCMu6qOQ2AnQqFX7Sl/S8pTF4qGpfF6HSHuZAmU95UX6VPVtfwXiLgx1ftk2b8CXDQUHC1Q0nCAloiVMHFkOQ9~-1~-1~1678338965; AKA_A2=A; ups_language_preference=en_IT; utag_main=v_id:0186c45dfc1a00016a91badd772b04075003106d0093c$_sn:2$_se:14$_ss:0$_st:1678338581419$dc_visit:2$vapi_domain:ups.com$_prevpageid:shipping%2FIntPickup%2Fpic(0not).html%3Bexp-1678340381543$_prevpage:wwwapps%3Ait%3Aen%3Apickup%3Aprocessinfo%3Bexp-1678340381542$ses_id:1678335918198%3Bexp-session$_pn:11%3Bexp-session$fs_sample_user:false%3Bexp-session$dc_event:14%3Bexp-session; s_nr=1678336786083-New; dayssincevisit=1678336786084',
        "origin": "https://wwwapps.ups.com",
        "pragma": "no-cache",
        "referer": "https://wwwapps.ups.com/pickup/schedule?loc=it_IT",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }

    params = {
        "loc": loc,
    }

    response = session.post(
        "https://wwwapps.ups.com/pickup/processinfo",
        params=params,
        headers=headers,
        data=payload,
    )


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
        "loc": loc,
        "gotoapp": "",
        "acctInfoDetails": "",
        "pickupInfoPageScheme": "",
        "selectedServices": "null",
        "EDITABLE_ACCTNUM": "FALSE",
        "localeValue": loc,
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
        # return checkout(session, payload,loc)

        headers = {
            "authority": "wwwapps.ups.com",
            "accept": "application/json;charset=utf-8",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/json;charset=UTF-8",
            # 'cookie': 'JSESSIONID=F29FE51F9E41EB24C9A6409946366842; bm_sz=7CB471EA39F68D5E740FF2723CB65745~YAAQgTRoaH+NKb6GAQAANPpdxBOsNmh/9RNYBc717hfbelE1XyqbtSOyneLvwQxpiCyNptLR27VGh74OiZJH2fIUyEjgMhcalv3Gj4E9v77hqeeAsbt01FsWFxr2jG0642TLd9htbRKXFsGRjaZ59EFqL6uEb3YgTLuCsiG2pV+ZOYbXXkCOOrDmhMqhbF75hRfIevqYqj/enL8W/HQETGsqwCASVHNuEojFj0YNqf9ZAgxMK3FPUrVBeUkay61u2roPF5QngAOLr++wmsZWxWx+HfvJIEXzHjwNTSQLP3k=~4339769~3747908; PIM-SESSION-ID=e9kDwp7iEzl9fBxS; ak_bmsc=1E4482440C87BC23FCF7B2E24F7EACF4~000000000000000000000000000000~YAAQgTRoaIONKb6GAQAAGf9dxBNRqrd/w8KCU+Cw6Xqf7QqxH93ZY0+aCoXdvVUUIWD9A9g+kOp0hLAqvtJrBnMyIvzGCC0KPyjNeutY8Z+SytiufvMhSsqxkZ7hDcw4pILdxW0AlKd9hFuofJwA9myzUzl/Gu+MFxE+/CChx58LbUr+Gbmo5Kf5GKxoBoCefhV3o3IUSGY3y1MRAsKITZiIfdiXn5EYIVTPTeuqjDon91eEY7+PNr8j6lTr78M4FX4ICbY050kNEWWixDo3XXqKbmMA48XFoBT9QRBmHLMQrvoukuHdf7lcPxlenGN78+ttHe4t+8Ps6U01OoTRtsKPPLS4rvGCTdCrZvvVfnr7NjfLUDSjtsHUBSXN17cXNRtnfU9hWo+iVnF6hH+v1NkF1X/xovYI8aq3zxFtkN4jC0zBMnnraIGrtKh6ozI5aulwhk9w7B/aBgW03ejNUdWGPZ8zRKP0iZZjAEZ6pVH64psyCFn/lQ==; com.ups.com_ups_GDOL.sData=99f51414df7d49b3b16c3591c669f54e:tDvKqc06ILw7Y0hob3CZPmwy8dQs/q5+lxnlq0alhgU=; sharedsession=4f874a9c-a142-47c1-8728-f85df1e1e5bc:w; s_fid=60E726A4E6DEA787-341517BABFA85A09; s_vnum=1680300000126%26vn%3D1; s_invisit=true; dayssincevisit_s=First%20Visit; s_cc=true; s_vi=[CS]v1|3204A825D6934D70-60000B0FC195765C[CE]; CONSENTMGR=consent:true%7Cts:1678332400820%7Cc1:1%7Cc3:0%7Cc5:1%7Cc6:1%7Cc7:0%7Cc8:1%7Cc9:1; GPC_cookie_corrected=true, ts:1678332400820,c3: 0,c7: 0; _abck=0DD47936455CC42A2AB14DF31AB65E3B~0~YAAQgTRoaFqqKb6GAQAAu3yWxAmXP0JluZYiQJCGN72euIAXi3/I04KgRjKTCpT8LpEi/Goy1PIT0wxK/MVCWI/T2hRE/qdi9iVVooLp4cvWomAQG1uFzDEtsR9GaHcTn9Vidox1Jwp4JiAftSvYp4wD3uKTG4y+00+7WKMg63XA+2jJ7/9oO7Mp7u2v28Rdp7Yni5n3IGgPUYCNemLlCQQGr+qEP002OuIXtnIY5yOIJEdpd7CC1hXebnGodb1CR8wff44GO8WagkqFOS3qmd9CfqvTzOUM0JfLMz7LIZkThZijZPMPegpnlt6/ZXS4X7QzGFCCMu6qOQ2AnQqFX7Sl/S8pTF4qGpfF6HSHuZAmU95UX6VPVtfwXiLgx1ftk2b8CXDQUHC1Q0nCAloiVMHFkOQ9~-1~-1~1678338965; AKA_A2=A; ups_language_preference=it_IT; utag_main=v_id:0186c45dfc1a00016a91badd772b04075003106d0093c$_sn:2$_se:15$_ss:0$_st:1678338587626$dc_visit:2$vapi_domain:ups.com$_prevpageid:shipping%2FIntPickup%2Fpic(3pic).html%3Bexp-1678340387960$_prevpage:wwwapps%3Ait%3Ait%3Apickup%3Aprocessinfo%3Bexp-1678340387959$ses_id:1678335918198%3Bexp-session$_pn:12%3Bexp-session$fs_sample_user:false%3Bexp-session$dc_event:15%3Bexp-session; s_nr=1678336947971-New; dayssincevisit=1678336947972',
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
            "x-upscpc-rest-api-token": "YKxzYAA/mvHCQhsFyA6uv+1uQaf+Bt7hmcoX/kQDsV5qixzT9myRRVk6XkKeeJYEgIQd16vzP52fWe6Rwj1Pb3IaGC6Rq8RCRNGwaN4x+wx+dnYGIvjU7Wlo0jymTKxl8h9WZsUcc+upADGqOzFCbC6bt+GWRmbwV2paL/tElfdLhB0uHGKvueoyD+jKIFXm54GwEtly1gA6ui144eSScsQxFPApqVsCQOvZ3aEKpEKJbIRdA50nFhFWpRYQj//FGzxkt1BRYBq9P+wi/C7QDEbQX1NM4XUJ3kU3V+DIbMwF2qTdYOuca+NqSDbfUeDjKkj/DdSDxTw4vaC550uiaw==",
            "x-upscpc-rest-app-id": "50GxoUTjsoOf45QW",
        }

        json_data = {
            "@type": "Card",
            "options": {
                "transactionId": "258391174",
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
            "https://wwwapps.ups.com/cpcws/api/v2/payments/258391174/store",
            headers=headers,
            json=json_data,
        )
        print(response.status_code)
        print(response.text)


def session(row: list):
    country = row[6].strip()

    session = requests.Session()
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
        response.raise_for_status()
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

    if "Enter Collection Information" in response.text:
        return schedule(row, session)
