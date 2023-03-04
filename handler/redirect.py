from handler.utils import *
from handler.webhook import checker_brt_discord, redirect_webhook_brt
import os
import time
import requests
from bs4 import BeautifulSoup
import csv
import threading

REDIRECT_PATH = "Uzumaki/redirect"


def brt_tracking_checker(tracking, zip_code):
    print_task(f"[brt {tracking}] checking tracking info...", PURPLE)

    headers = {
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
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    params = {
        "docmit": tracking,
        "ksu": "1664282",
        "lang": "it",
    }

    try:
        session = requests.Session()

        response = session.get(
            "https://vas.brt.it/vas/sped_ricdocmit_load.hsm",
            params=params,
            headers=headers,
        )

        if "errori riscontrati" in response.text.lower():
            print_task(f"[brt {tracking}] Shipment not found...", RED)
            time.sleep(4)
            return

        if "non è possibile fornire indicazioni di consegna" in response.text.lower():
            print_task(f"[brt {tracking}] Shipment not redirectable...", RED)
            time.sleep(3)
            input("press enter to exit...")
            return

        if "n. spedizione" in response.text.lower():
            print_task(f"[brt {tracking}] Shipment found...", GREEN)

            soup = BeautifulSoup(response.text, "html.parser")
            for table in soup.find_all("table", class_="table_dati_spedizione"):
                for td in table.find_all("td"):
                    if td.text[:3] == "166":
                        spedizione = td.text
                        break

            if spedizione == "":
                print_task(
                    "[brt %s] %s" % (tracking, "Redirect not available"),
                    RED,
                )
                input("Press enter to exit...")
                return

            headers = {
                "authority": "www.mybrt.it",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "cross-site",
                "sec-fetch-user": "?1",
                "sec-gpc": "1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            }

            params = {
                "lang": "it",
                "parcelNumber": "23" + spedizione,
            }

            try:
                response = session.get(
                    "https://www.mybrt.it/it/mybrt/my-parcels/search",
                    params=params,
                    headers=headers,
                )

                if "Protezione dei dati":
                    print_task(
                        "[brt %s] %s" % (tracking, "Filling info..."),
                        PURPLE,
                    )

                soup = BeautifulSoup(response.text, "html.parser")
                csrf = soup.find("meta", attrs={"name": "_csrf"})["content"]

                headers = {
                    "authority": "www.mybrt.it",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                    "cache-control": "no-cache",
                    "origin": "https://www.mybrt.it",
                    "pragma": "no-cache",
                    "referer": "https://www.mybrt.it/it/mybrt/my-parcels/search?lang=it&parcelNumber="
                    + "23"
                    + spedizione,
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

                data = {
                    "_csrf": csrf,
                    "verificationCode": zip_code,
                    "recaptchaResponse": "",
                    "number": "23" + spedizione,
                    "shipmentType": "PARCEL_DETAILS",
                    "sourceUrl": "",
                    "validate": "Conferma",
                }

                response = session.post(
                    "https://www.mybrt.it/it/mybrt/my-parcels/search/protection",
                    headers=headers,
                    data=data,
                )

                if "Il CAP inserito non corrisponde alla spedizione" in response.text:
                    print_task("[brt %s] %s" % (tracking, "Wrong ZipCode"), RED)
                    input("Press enter to exit...")
                    return

                if (
                    "della richiesta si è verificato un problema tecnico."
                    in response.text
                ):
                    print_task(
                        "[brt %s] %s" % (tracking, "problema tecnico."),
                        RED,
                    )
                    input("Press enter to exit...")
                    return

                if (
                    "CAPTCHA mancante o non valido, si prega di riprovare."
                    in response.text
                ):
                    print_task("[brt %s] %s" % (tracking, "CAPTCHA hit."), RED)
                    input("Press enter to exit...")
                    return

                try:
                    brt_number = response.url.split("parcelNumber=")[1]
                    brt_tracking_response = response.url
                except:
                    print_task(
                        "[brt %s] %s" % (tracking, "Error getting BRT number"),
                        RED,
                    )
                    time.sleep(5)
                    return

                print_task(
                    "[brt %s] %s" % (tracking, "successfull got BRT number"), GREEN
                )

                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Origin": "https://vas.brt.it",
                    "Pragma": "no-cache",
                    "Referer": "https://vas.brt.it/vas/sped_det_show.htm",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-User": "?1",
                    "Sec-GPC": "1",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                    "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"macOS"',
                }

                data = {
                    "refererBolla": "sped_det_show.htm",
                    "referer": "sped_numspe_par.htm",
                    "reqid": "",
                    "pagina": "",
                    "ksu": "",
                    "annoSpedizione": "2023",
                    "nSpediz": spedizione,
                    "brtCode": brt_number,
                    "BRTCODE": brt_number,
                }

                session_brt_tracking = requests.Session()

                response = session_brt_tracking.post(
                    "https://vas.brt.it/vas/istruzioni_consegna_form.htm",
                    headers=headers,
                    data=data,
                )

                redictable = "NO"
                if "Referente consegna" in response.text:
                    redictable = "YES"

                checker_brt_discord(
                    brt_number,
                    brt_tracking_response,
                    redictable,
                    zip_code,
                    tracking,
                )

            except Exception as e:
                print_task(f"[brt {tracking}] error filling the form", RED)
                print_task(f"[brt {tracking}] {e}", RED)
                time.sleep(5)
                return

    except Exception as e:
        print_task(f"[brt {tracking}] error checking tracking info", RED)
        print_task(f"[brt {tracking}] {e}", RED)
        time.sleep(5)
        return

    print_task(f"[brt {tracking}] finished", GREEN)
    time.sleep(5)


def handle_brt_request_success(
    tracking, name, phone, address, city, state, zipcode, url, email
):
    print_task("[brt %s] %s" % (tracking, "Successful redirect"), GREEN)

    redirect_webhook_brt(
        "BRT",
        tracking,
        name,
        phone,
        address,
        city,
        state,
        zipcode,
        url,
        email,
    )


def brt_tracking_redirect(tracking, name, phone, address, city, state, zip_code, email):
    base_url = "https://vas.brt.it/vas/"
    print_task(f"[brt {tracking}] getting tracking info", PURPLE)

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Origin": "https://vas.brt.it",
        "Pragma": "no-cache",
        "Referer": f"{base_url}sped_numspe_par.htm",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    data = {
        "brtCode": tracking,
        "RicercaBrtCode": "Ricerca",
        "referer": "sped_numspe_par.htm",
        "nSpediz": tracking[2:],
    }

    session = requests.Session()

    response = session.post(
        "https://vas.brt.it/vas/sped_det_show.htm", headers=headers, data=data
    )

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Origin": "https://vas.brt.it",
        "Pragma": "no-cache",
        "Referer": "https://vas.brt.it/vas/sped_det_show.htm",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    data = {
        "refererBolla": "sped_det_show.htm",
        "referer": "sped_numspe_par.htm",
        "reqid": "",
        "pagina": "",
        "ksu": "",
        "annoSpedizione": "2023",
        "nSpediz": "",
        "brtCode": tracking,
        "BRTCODE": tracking,
    }
    session2 = requests.Session()
    response = session2.post(
        "https://vas.brt.it/vas/istruzioni_consegna_form.htm",
        headers=headers,
        data=data,
    )

    if "Referente consegna" in response.text:
        soup = BeautifulSoup(response.text, "html.parser")

        try:
            dateValue = soup.find("input", {"name": "dataConsegna"})["value"]
        except:
            dateValue = ""

        try:
            locationValue = soup.find("input", {"name": "desLoc"})["value"]
        except:
            locationValue = ""

        try:
            provValue = soup.find("input", {"name": "desProv"})["value"]
        except:
            provValue = ""

        try:
            emailValue = soup.find("input", {"name": "email"})["value"]
        except:
            emailValue = ""

        time.sleep(1)

        bigGipServer = response.cookies.get_dict()["BIGipServerAS777-Pool"]

        TS01ef7a66 = response.cookies.get_dict()["TS01ef7a66"]

        cookies = {
            "BIGipServerAS777-Pool": bigGipServer,
            "iduser": "",
            "lstaut": "0000000000100",
            "usrname": "",
            "ksu": "",
            "lang": "en",
            "TS01ef7a66": TS01ef7a66,
        }

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Origin": "https://vas.brt.it",
            "Pragma": "no-cache",
            "Referer": "https://vas.brt.it/vas/istruzioni_consegna_form.htm",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
        }

        client_timestamp = int(time.time() * 1000)
        new_state = state.upper()

        data: dict = {
            "newReferenteConsegna": name,
            "newTelefonoFisso": phone,
            "newEmail": email,
            "newCellulare": "",
            "tipoIstruzione": "3",
            "newDataConsegna": dateValue,
            "newOraConsegna": "",
            "newNominativo1Consegna": name,
            "newNominativo2Consegna": "",
            "newIndirizzoConsegna": address,
            "newCapConsegna": zip_code,
            "newLocalitaConsegna": city,
            "newProvinciaConsegna": new_state,
            "newDataConsegnaNewInd": "",
            "newOraConsegnaNewInd": "",
            "altre": "",
            "inputConferma": "Confirm",
            "annoSpedizione": "2023",
            "nSpediz": "",
            "brtCode": tracking,
            "clientTimeStamp": client_timestamp,
            "referenteConsegna": "",
            "telefonoFisso": "",
            "email": emailValue,
            "cellulare": "",
            "destinat": "",
            "destinat2": "",
            "desIndir": "",
            "desCap": "",
            "desLoc": locationValue,
            "desProv": provValue,
            "dataConsegna": dateValue,
            "oraConsegna": "",
            "urlReferer": "istruzioni_consegna_form.htm",
            "refererBolla": "sped_det_show.htm",
            "referer": "sped_numspe_par.htm",
            "reqid": "",
            "pagina": "",
            "newPudoId": "",
            "oldPudoId": "",
            "pudoData": "",
        }

        response = session2.post(
            "https://vas.brt.it/vas/istruzioni_consegna_conferma.htm",
            cookies=cookies,
            headers=headers,
            data=data,
        )
        url = (
            "https://www.mybrt.it/it/mybrt/my-parcels/incoming?parcelNumber=" + tracking
        )
        form_response_text = response.text.lower()

        if "request submitted successfully" in form_response_text:
            handle_brt_request_success(
                tracking, name, phone, address, city, state, zip_code, url, email
            )
            return

        if (
            "ti confermiamo di aver preso in carico la tua richiesta del"
            in form_response_text
        ):
            handle_brt_request_success(
                tracking, name, phone, address, city, state, zip_code, url, email
            )
            return

        else:
            print_task("[brt %s] %s" % (tracking, "Failed to redirect"), RED)
            input("Press enter to exit...")
            return

    else:
        print_task("[brt %s] %s" % (tracking, "No Redirect possible"), RED)
        input("Press enter to exit...")
        return


def redirect(username):
    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print(RED + BANNER + RESET)

        print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

        # Use with statement to open file and change directory
        with os.scandir(REDIRECT_PATH) as dir_entries:
            files_dict = {}
            for index, entry in enumerate(dir_entries):
                if entry.is_file():
                    print_file(f"{index}. {entry.name}")
                    files_dict[str(index)] = entry.name

        print("\n")
    
        option = input(TAB + "> choose: ")

        try:
            file = files_dict[option]
            break
        except KeyError:
            print_task("invalid option", RED)
            time.sleep(2)

    # Use with statement to open file
    with open(os.path.join(REDIRECT_PATH, file), "r") as f:
        reader = csv.reader(f)

        try:
            next(reader)
        except StopIteration:
            print_task("file is empty", RED)
            time.sleep(2)
            os._exit(1)

        try:
            row = next(reader)
        except StopIteration:
            print_task(f"Please Fill {REDIRECT_PATH}/{file}", RED)
            time.sleep(2)
            os._exit(1)

        f.seek(0)
        reader = csv.reader(f)
        next(reader)

        if file == "brt_checker.csv":
            for row in reader:
                tracking = row[0].lower().strip()
                zip_code = row[1].lower().strip()

                try:
                    threading.Thread(
                        target=brt_tracking_checker, args=(tracking, zip_code)
                    ).start()
                except:
                    print_task("Error starting tasks", RED)
                    input("Press enter to exit...")
                    return

        if file == "brt_redirect.csv":
            for row in reader:
                tracking = row[0].lower().strip()
                name = row[1].lower().strip()
                phone = row[2].lower().strip()
                address = row[3].lower().strip()
                city = row[4].lower().strip()
                state = row[5].lower().strip()
                zip_code = row[6].lower().strip()
                email = row[7].lower().strip()

                try:
                    threading.Thread(
                        target=brt_tracking_redirect,
                        args=(
                            tracking,
                            name,
                            phone,
                            address,
                            city,
                            state,
                            zip_code,
                            email,
                        ),
                    ).start()
                except:
                    print_task("Error starting tasks", RED)
                    input("Press enter to exit...")
                    return
