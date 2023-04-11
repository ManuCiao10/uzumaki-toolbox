import time
import requests
import json

from master.masterTypes import Thread
from bs4 import BeautifulSoup

Logo = "https://media.discordapp.net/attachments/819084339992068110/1083492784146743416/Screenshot_2023-03-09_at_21.53.23.png"


def BackendLinkFlow(URL: str, parentThread: Thread):
    first = True
    data_list = list()
    sku = URL.split("-")[-1].split(".")[0]

    print("[{}] Starting thread.".format(sku))

    headers = {
        "authority": "shop.ticketmaster.it",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Chromium";v="112", "Brave";v="112", "Not:A-Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }

    while True:
        session = requests.Session()
        print("getting data...")
        try:
            response = session.get(
                "https://webcache.googleusercontent.com/search?q=cache:https://shop.ticketmaster.it/biglietti/acquista-biglietti-travis-scott-i-days-milano-coca-cola-30-giugno-2023-ippodromo-snai-la-maura-milano-4996.html&strip=0&vwsrc=0",
                headers=headers,
            )
        except:
            print("Error getting session")
            print("Retrying in 20 seconds...")
            time.sleep(20)
            continue

        if response.status_code != 200:
            print("Error getting data {}".format(response.status_code))
            print("Retrying in 20 seconds...")
            time.sleep(20)
            continue

        if "Request unsuccessful. Incapsula incident ID" in response.text:
            print("Request unsuccessful. Incapsula incident ID")
            print("Retrying in 20 seconds...")
            time.sleep(20)
            continue

        print("successfull got data {}".format(response.status_code))

        if first:
            print("First running")

            # remove <!-- TMWEB7 (31ms) --> from the end of the response

            # response_data = response.text[:-26]

            response_data = response.text  # for testing purposes
            first = False
            # break
        else:
            print("checking for changes...")

            if response_data != response.text[:-26]:
                print("data has changed")

                response_data = response.text[:-26]

                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.content, "html.parser")

                # Find the script tag with type "application/ld+json"
                script = soup.find("script", {"type": "application/ld+json"})

                # Extract the JSON data from the script tag
                # print(response_data)
                json_data = json.loads(script.string)

                image = json_data["image"]["url"]
                title = json_data["name"]
                location = json_data["location"]["name"]
                endDate = json_data["endDate"].split("T")[0]

                dict_data = list()

                for ticket_type in json_data["offers"]["offers"]:
                    name = ticket_type["name"]
                    dict_data.append({"name": name})

                for ticket_type in json_data["offers"]["offers"]:
                    price = ticket_type["price"]
                    price = f"{price} € "

                    dict_data.append({"price": price})

                rows = soup.find_all("tr", {"class": "tr-1-2"})
                for row in rows:
                    values = row.find_all("td")

                    soup = BeautifulSoup(str(values), "html.parser")

                    if "Attualmente non disponibile" in soup.get_text():
                        stock = "OOS"
                    else:
                        select_tag = soup.find(
                            "select", {"name": lambda x: x and "idProductItemQta" in x}
                        )
                        stock = select_tag["qtqtymax"]

                    # data_list.append([price, stock, name])
                    dict_data.append({"stock": stock})

                print(dict_data)
                # webhook(data_list, image, title, location, endDate, URL)

            else:
                print("data has not changed...")
                time.sleep(20)
                continue


def webhook(
    ticket_info: list, image: str, title: str, location: str, endDate: str, URL: str
):
    webhook_uzumaki = "WEBHOOK_HERE"

    embee = []

    print(ticket_info)

    for ticket in ticket_info:
        print(ticket)
        embee.append(
            {
                "name": ticket[0],
                "value": ticket[1] + "[" + ticket[2] + "]",
                "inline": False,
            }
        )

    embee.append({"name": "Location", "value": location, "inline": True})
    embee.append({"name": "Date", "value": endDate, "inline": True})

    webhook_data = {
        "username": "Ticket Master",
        "avatar_url": Logo,
        "embeds": [
            {
                "title": title,
                "url": URL,
                "description": "> STOCK HAS CHANGED",
                "color": 12298642,
                "thumbnail": {"url": image},
                "fields": embee,
                "footer": {
                    "text": "Ticket Master | Uzumaki",
                    "icon_url": Logo,
                },
            }
        ],
    }

    response = requests.post(webhook_uzumaki, json=webhook_data)

    try:
        response.raise_for_status()
        print("[{}] - success".format(response.status_code))
    except requests.exceptions.HTTPError as err:
        print(err)
    except:
        print("An unexpected error occurred")


# add row to the table
