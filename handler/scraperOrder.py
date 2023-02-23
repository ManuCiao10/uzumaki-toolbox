# scraper order New Balance
from handler.utils import *
import csv
import threading
import requests
from bs4 import BeautifulSoup
from handler.webhook import webhook_newBalance


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
            print_task("order not found %s %s %s" % (orderNumber, postalCode, orderLastname), RED)
            time.sleep(5)
            return

        print_task(
            "order found %s %s %s" % (orderNumber, postalCode, orderLastname), GREEN
        )

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
        print_task(
            "order not found %s %s %s" % (orderNumber, postalCode, orderLastname), RED
        )
        time.sleep(3)
        os._exit(1)


# def courir(email, zipCode):

def scraperOrder():
    print("ordescraperOrder")
    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

    os.chdir("Uzumaki/scraper")
    files = os.listdir()
    os.chdir("../..")

    files_dict = {}

    for index, file in enumerate(files):
        print_file(str(index) + ". " + file)

        files_dict[str(index)] = file

    print("\n")
    option = input(TAB + "> choose: ")

    try:
        file = files_dict[option]
    except KeyError:
        print_task("invalid option", RED)
        time.sleep(3)
        os._exit(1)

    with open("Uzumaki/scraper/" + file, "r") as f:
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
            print_task("please fill " + file, RED)
            time.sleep(2)
            os._exit(1)

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
                    time.sleep(3)
                    os._exit(1)

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
                    time.sleep(3)
                    os._exit(1)

                threading.Thread(target=courir, args=(email, zipCode)).start()

        else:
            print_task("invalid option", RED)
            time.sleep(3)
            os._exit(1)
