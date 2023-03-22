import requests
import re
from handler.utils import *
import csv
import threading
from internal.security import processRunning
from urllib.parse import urlparse, parse_qs
from handler.webhook import webhook_dhl_redirect


def dhlRedirect(username):
    processRunning()
    setTitleMode("Redirect DHL")

    os.system("cls" if os.name == "nt" else "clear")

    print(f"{RED}{BANNER}{RESET}")

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    try:
        with open("Uzumaki/redirect_dhl/redirect.csv", "r") as f:
            reader = csv.reader(f)

            try:
                next(reader)
            except StopIteration:
                print_task("file is empty", RED)
                exit_program()

            try:
                row = next(reader)
            except StopIteration:
                print_task("please fill Uzumaki/redirect_dhl/redirect.csv", RED)
                exit_program()

            f.seek(0)
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                url = row[0].strip()
                zipcode = row[1].strip()
                acces_point_client = row[2].strip()
                countryCode = row[3].strip().upper()

                threading.Thread(
                    target=dhl_redirect,
                    args=(url, zipcode, acces_point_client, countryCode),
                ).start()

    except FileNotFoundError:
        print_task("Uzumaki/redirect_dhl/redirect.csv not found", RED)
        time.sleep(3)
        return


# webhook and thread to check the input data
def dhl_redirect(url, zipcode, acces_point_client, countryCode):
    # check if the county code is 2 letters
    data_access = {}

    session = requests.Session()
    print_task("getting session", YELLOW)

    session.headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    response = session.get(url)

    if "AWB=" not in response.url:
        print_task("error getting redirection response", RED)
        exit_program()

    if response.status_code != 200:
        print_task("error getting session", RED)
        exit_program()

    parsed_url = urlparse(response.url)
    query_params = parse_qs(parsed_url.query)

    awb = query_params.get("AWB", [""])[0]
    osva = query_params.get("OSVA", [""])[0]

    regex = re.compile(
        r'javax.faces.ViewState" id="j_id1:javax.faces.ViewState:1" value="(.*)" autocomplete="off"'
    )
    try:
        viewstate = regex.findall(response.text)[0]
    except IndexError:
        print_task("error getting viewstate", RED)
        exit_program()

    data = {
        "skipIndexForm": "skipIndexForm",
        "javax.faces.ViewState": viewstate,
        "javax.faces.source": "skipIndexForm:skipIndexBtn",
        "javax.faces.partial.execute": "skipIndexForm:skipIndexBtn skipIndexForm:skipIndexBtn",
        "javax.faces.partial.render": "updateSVPDelForm getServicePointsForm",
        "ctrycode": "",
        "langcode": "",
        "AWB": awb,
        "token": "",
        "OSVA": osva,
        "client": "",
        "javax.faces.behavior.event": "action",
        "javax.faces.partial.ajax": "true",
    }

    response = session.post(
        "https://del.dhl.com/prg/jsp/redirect_page.xhtml", data=data
    )

    data = {
        "redirectForm": "redirectForm",
        "javax.faces.ViewState": viewstate,
        "redirectForm:redirectBtn": "redirectForm:redirectBtn",
        "DELOPS": "",
        "QAR": "",
        "USRID": "",
        "src": "",
    }

    response = session.post(
        "https://del.dhl.com/prg/jsp/redirect_page.xhtml", data=data
    )
    if response.status_code != 200:
        print("error getting response from redirect")
        exit_program()

    if "Change Delivery Date" not in response.text:
        print_task("redirect not available", RED)
        exit_program()

    print_task("starting to redirect", PURPLE)
    r = session.get(
        "https://del.dhl.com/prg/customer/options/servicepoint_delivery.xhtml",
    )

    try:
        viewstate_2 = re.findall(
            r'javax.faces.ViewState" id="j_id1:javax.faces.ViewState:1" value="(.*)" autocomplete="off"',
            r.text,
        )[0]
    except IndexError:
        print_task("error getting viewstate version-2", RED)
        exit_program()
    try:
        csrfId_2 = re.findall(
            r'<input type="hidden" name="csrfId" value="([^"]+)"\s*/?>', r.text
        )[0]
    except IndexError:
        print_task("error getting csrfId version-2", RED)
        exit_program()

    access_point = {
        "key": "52655c72-cfc7-4147-ac3c-1657941f5746",
        "address": zipcode,
        "countryCode": countryCode,
        "servicePointResults": "300",
        "maxDistance": "50",
        "servicePointTypes": "PRT,247,CTY,STN",
        "capability": "86,87,78,79",
        "weight": "1",
        "weightUom": "kg",
        "length": "23",
        "width": "23",
        "height": "23",
        "dimensionsUom": "CM",
        "pieceCountLimit": "1",
        "importCharges": "N",
        "language": "ita",
    }

    response = session.get(
        "https://wsbexpress.dhl.com/ServicePointLocator/restV3/servicepoints",
        params=access_point,
    )
    if response.status_code != 200:
        print_task("error data regarding access point", RED)
        exit_program()

    try:
        for each in response.json()["servicePoints"]:
            if acces_point_client.upper() in each["localName"]:
                data_access = each
                break
    except:
        print_task("error getting access point", RED)
        exit_program()

    if data_access == {}:
        print_task("access point not found", RED)
        exit_program()

    print_task("access point found", GREEN)

    FacilityId = data_access["facilityId"]
    facilityTypeCode = data_access["facilityTypeCode"]
    servicePointType = data_access["servicePointType"]
    localName = data_access["localName"]
    city = data_access["address"]["city"]
    country = data_access["address"]["country"]
    zipCode = data_access["address"]["zipCode"]
    addressLine1 = data_access["address"]["addressLine1"]
    addressLine2 = data_access["address"]["addressLine2"]
    if addressLine2 == None:
        addressLine2 = ""
    addressLine3 = data_access["address"]["addressLine3"]
    if addressLine3 == None:
        addressLine3 = ""

    distance = data_access["distance"]

    openingHours = data_access["openingHours"]["openingHours"]
    partnerTypeCode = data_access["partner"]["partnerTypeCode"]

    data_before = {
        "service-point-form": "service-point-form",
        "csrfId": csrfId_2,
        "service-point-form:servicePointTable::selection": "",
        "service-point-form:select-btn": "Confirm",
        "service-point-form:selectedServicePointFacilityId": FacilityId,
        "service-point-form:selectedServicePointFacilityTypeCode": facilityTypeCode,
        "service-point-form:selectedServicePointType": servicePointType,
        "service-point-form:selectedServicePointName": localName,
        "service-point-form:selectedServicePointCity": city,
        "service-point-form:selectedServicePointPostcode": zipCode,
        "service-point-form:selectedServicePointOpeningHours": openingHours,
        "service-point-form:selectedServicePointAddr1": addressLine1,
        "service-point-form:selectedServicePointAddr2": addressLine2,
        "service-point-form:selectedServicePointAddr3": addressLine3,
        "service-point-form:selectedServicePartnerTypeCode": partnerTypeCode,
        "javax.faces.ViewState": viewstate_2,
        "javax.faces.source": "service-point-form:select-btn",
        "javax.faces.partial.execute": "service-point-form:select-btn service-point-form:post-number",
        "javax.faces.partial.render": "validationFailedId service-point-form:post-number-message",
        "_openFaces_ajax": "true",
        "javax.faces.partial.ajax": "true",
    }

    response = session.post(
        "https://del.dhl.com/prg/customer/options/servicepoint_delivery.xhtml",
        data=data_before,
    )

    payload_selection = {
        "service-point-form": "service-point-form",
        "csrfId": csrfId_2,
        "service-point-form:servicePointTable::selection": "",
        "service-point-form:j_idt273": "",
        "service-point-form:selectedServicePointFacilityId": FacilityId,
        "service-point-form:selectedServicePointFacilityTypeCode": facilityTypeCode,
        "service-point-form:selectedServicePointType": servicePointType,
        "service-point-form:selectedServicePointName": localName,
        "service-point-form:selectedServicePointCity": city,
        "service-point-form:selectedServicePointPostcode": zipCode,
        "service-point-form:selectedServicePointOpeningHours": openingHours,
        "service-point-form:selectedServicePointAddr1": addressLine1,
        "service-point-form:selectedServicePointAddr2": addressLine2,
        "service-point-form:selectedServicePointAddr3": addressLine3,
        "service-point-form:selectedServicePartnerTypeCode": partnerTypeCode,
        "javax.faces.ViewState": viewstate_2,
    }

    response = session.post(
        "https://del.dhl.com/prg/customer/options/servicepoint_delivery.xhtml",
        data=payload_selection,
    )

    if "errorRef" in response.url:
        print_task(f"selection error {response.url}", RED)
        exit_program()

    print_task("redirect done, check your email", GREEN)
    webhook_dhl_redirect(url, localName, addressLine1, city, zipCode, distance, country)
