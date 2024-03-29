from handler.utils import *
import csv
import threading
import requests
from bs4 import BeautifulSoup
from handler.webhook import webhook_newBalance, webhook_courir
import time
from internal.security import processRunning
from datetime import datetime


def newBalance(orderNumber, postalCode, orderLastname):
    headers = {
        "authority": "www.newbalance.it",
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

    params = {
        "trackOrderNumber": orderNumber,
        "trackOrderPostalCode": postalCode,
        "trackOrderLastname": orderLastname,
    }

    url_request = "https://www.newbalance.it/track/"

    if orderNumber[:2] == "nk":
        url_request = "https://www.newbalance.co.uk/track/"

    response = requests.get(url_request, params=params, headers=headers)

    if "Indirizzo di spedizione" or "Shipping Address" in response.text:
        trackingLink = response.url

        soup = BeautifulSoup(response.text, "html.parser")

        try:
            date = soup.find("div", {"class": "col-8 col-lg-8"}).text

        except:
            print_task(f"[newBalance {orderNumber}] error", RED)
            time.sleep(2)
            return

        print_task(f"[newBalance {orderNumber}] order found", PURPLE)

        style = soup.find("p", {"class": "font-body-small mb-0"}).text
        style = style.split(":")[1].strip()

        price = soup.find(
            "span", {"class": "font-body-large bold grand-total-sum"}
        ).text

        image = soup.find("img", {"class": "img-fluid order-img"})["src"]
        title = soup.find("img", {"class": "img-fluid order-img"})["title"]

        email = soup.find("span", {"class": "pl-2 order-summary-email"}).text

        firstName = soup.find("span", {"class": "firstName font-body"}).text.strip()
        secondName = soup.find("span", {"class": "lastName font-body"}).text.strip()

        addy = soup.find("span", {"class": "address1 font-body"}).text.strip()

        zipCode = soup.find("span", {"class": "postalCode font-body"}).text.strip()

        status = soup.find("div", {"class": "d-flex mb-0"})["data-status"]

        webhook_newBalance(
            orderNumber,
            date,
            style,
            price,
            image,
            title,
            email,
            firstName,
            secondName,
            addy,
            zipCode,
            status,
            trackingLink,
        )

    else:
        print_task(f"[newBalance {orderNumber}] error", RED)
        time.sleep(2)
        return


API_ENDPOINT = "https://api.shipup.co/v1/orders/tracking_page_order"
AUTH_TOKEN = "psjuWukt7xZALCREwhUgYg"


def courir(email, zipCode):
    headers = {
        "authority": "api.shipup.co",
        "accept": "application/vnd.api+json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "authorization": f"Bearer {AUTH_TOKEN}",
        "cache-control": "no-cache",
        "content-type": "application/vnd.api+json",
        "origin": "https://www.courir.com",
        "pragma": "no-cache",
        "referer": "https://www.courir.com/",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }

    try:
        with requests.get(
            f"{API_ENDPOINT}?address_zip={zipCode}&email={email}",
            headers=headers,
        ) as response:
            response.raise_for_status()
            data = response.json()

            print_task(f"[courir {email}] order found", PURPLE)

            orderNumber = data["data"][0]["attributes"]["orderNumber"]
            image = data["included"][1]["attributes"]["thumbnail"]["src"]
            utc_time = datetime.fromisoformat(
                data["data"][0]["attributes"]["orderedAt"]
            )
            orderedAt = utc_time.strftime("%H:%M:%S.%f")
            title = data["included"][1]["attributes"]["title"]

            # loop through included to get lineItems, start at the end of the list
            for i in reversed(data["included"]):
                if i["type"] == "expectedDeliveries":
                    expectedDelivery = i["attributes"]["date"]
                    break
                else:
                    expectedDelivery = "N/A"

            for i in data["included"]:
                if i["type"] == "trackers":
                    attributes = i["attributes"]
                    status = attributes["deliveryStatusCode"]
                    trackingLink = attributes["trackingLink"]
                    trackingNumber = attributes["trackingNumber"]
                    carrierCode = attributes["carrierCode"]
                    break
                else:
                    status = "N/A"
                    trackingLink = "https://www.courir.com/en/track-my-orders"
                    trackingNumber = "N/A"
                    carrierCode = "N/A"

            if status == "N/A":
                status = data["included"][0]["attributes"]["statusCode"]

            webhook_courir(
                email,
                zipCode,
                title,
                orderNumber,
                image,
                orderedAt,
                expectedDelivery,
                status,
                trackingLink,
                trackingNumber,
                carrierCode,
            )

            with open(f"Uzumaki/scraper/courir_output.csv", "a", newline="") as f:
                if os.stat(f"Uzumaki/scraper/courir_output.csv").st_size == 0:
                    f.write(
                        "status,email,zipCode,orderNumber,title,orderedAt,expectedDelivery,trackingLink,trackingNumber,carrierCode"
                        + "\n"
                    )
                if orderNumber not in open(f"Uzumaki/scraper/courir_output.csv").read():
                    f.write(
                        f"{status},{email},{zipCode},{orderNumber},{title},{orderedAt},{expectedDelivery},{trackingLink},{trackingNumber},{carrierCode}"
                        + "\n"
                    )

    except requests.exceptions.HTTPError:
        print_task(f"[courir {email}] HTTPError", RED)
        time.sleep(3)
    except json.decoder.JSONDecodeError:
        print_task(f"[courir {email}] JSONDecodeError", RED)
        time.sleep(3)
    except Exception as e:
        print_task(f"[courir {email}] {e}", RED)
        time.sleep(3)


def scraperOrder(username):
    processRunning()
    setTitleMode("scraper")
    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print(f"{RED}{BANNER}{RESET}")

        print(
            f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n"
        )

        os.chdir("Uzumaki/scraper")
        files = os.listdir()
        os.chdir("../..")

        files_dict = {}

        for index, file in enumerate(files):
            if file != "courir_output.csv":
                print_file(str(index) + ". " + file)
                files_dict[str(index)] = file

        print("\n")
        option = input(TAB + "> choose: ")

        try:
            file = files_dict[option]
            break
        except KeyError:
            print_task("invalid option", RED)
            time.sleep(1)

    with open("Uzumaki/scraper/" + file, "r") as f:
        reader = csv.reader(f)

        try:
            next(reader)
        except StopIteration:
            print_task("file is empty", RED)
            exit_program()

        try:
            row = next(reader)
        except StopIteration:
            print_task("please fill " + file, RED)
            exit_program()

        f.seek(0)
        reader = csv.reader(f)
        next(reader)

        if file == "newBalance.csv":
            for row in reader:
                try:
                    orderNumber = row[0].strip().lower()
                    postalCode = row[1].strip().lower()
                    orderLastname = row[2].strip().lower()

                except IndexError:
                    print_task("invalid file", RED)
                    exit_program()

                threading.Thread(
                    target=newBalance,
                    args=(orderNumber, postalCode, orderLastname),
                ).start()

        elif file == "courir.csv":
            for row in reader:
                try:
                    email = row[0].strip().lower()
                    zipCode = row[1].strip().lower()

                except IndexError:
                    print_task("invalid file", RED)
                    exit_program()

                threading.Thread(target=courir, args=(email, zipCode)).start()

        else:
            print_task("invalid option", RED)
            exit_program()
