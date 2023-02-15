from handler.utils import *


def send_webhook_sda(tracking_number, date, city, status):
    settings = load_settings()
    webhook = settings["webhook"]

    import requests
    import json
    url: str = ""

    url = "https://www.sda.it/wps/portal/Servizi_online/dettaglio-spedizione?locale=it&tracing.letteraVettura=" + tracking_number

    data = {
        "username": "Uzumaki Tools",
        "avatar_url": LOGO,
        "content": " ",
        "embeds": [
            {
                "title": "Tracking Number",
                "url": url,
                "color": 5529714,
                "footer": {
                    "text": "Powered by Uzumaki Tools",
                    "icon_url": LOGO
                },
                "thumbnail": {
                    "url": "https://media.discordapp.net/attachments/819084339992068110/1075180966349381773/logo.jpeg"
                },
                "fields": [
                    {
                        "name": "Company",
                        "value": "SDA",
                        "inline": True
                    },
                    {
                        "name": "Date",
                        "value": date,
                        "inline": True
                    },
                    {
                        "name": "City",
                        "value": city,
                        "inline": False
                    },
                    {
                        "name": "Status",
                        "value": status,
                        "inline": True
                    }
                ]
            }
        ]
    }

    result = requests.post(webhook, data=json.dumps(
        data), headers={"Content-Type": "application/json"})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)


def send_webhook_brt(company, tracking_number, date, time, location, status):
    settings = load_settings()
    webhook = settings["webhook"]

    import requests
    import json
    url: str = ""

    if company == "brt":
        url = "https://www.mybrt.it/it/mybrt/my-parcels/search?lang=en&parcelNumber=" + tracking_number

    data = {
        "username": "Uzumaki Tools",
        "avatar_url": LOGO,
        "content": " ",
        "embeds": [
            {
                "title": "Tracking Number",
                "url": url,
                "color": 16731177,
                "footer": {
                    "text": "Powered by Uzumaki Tools",
                    "icon_url": LOGO
                },
                "thumbnail": {
                    "url": "https://media.discordapp.net/attachments/1074041462460784701/1074456541480095845/logo.jpg?width=1410&height=846"
                },
                "fields": [
                    {
                        "name": "Company",
                        "value": "BRT",
                        "inline": True
                    },
                    {
                        "name": "Status",
                        "value": status,
                        "inline": True
                    },
                    {
                        "name": "Date",
                        "value": date,
                        "inline": True
                    },
                    {
                        "name": "Time",
                        "value": time,
                        "inline": True
                    },
                    {
                        "name": "Branch",
                        "value": location,
                        "inline": True
                    }
                ]
            }
        ]
    }

    result = requests.post(webhook, data=json.dumps(
        data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)


def send_webhook(company, tracking_number, status, simplifiedText, streetAddress1, city, country, zipCode, attentionName):
    # https://www.mathsisfun.com/hexadecimal-decimal-colors.html

    settings = load_settings()
    webhook = settings["webhook"]

    import requests
    import json
    url: str = ""

    if company == "ups":
        url = "https://www.ups.com/track?loc=en_IT&tracknum=" + \
            tracking_number + "&requester=ST/trackdetails"
    data = {
        "username": "Uzumaki Tools",
        "avatar_url": LOGO,
        "content": " ",
        "embeds": [
            {
                "title": "Tracking Number",
                "url": url,
                "color": 16731177,
                "footer": {
                    "text": "Powered by Uzumaki Tools",
                    "icon_url": LOGO
                },
                "thumbnail": {
                    "url": LOGO
                },
                "fields": [
                    {
                        "name": "Company",
                        "value": company,
                        "inline": True
                    },
                    {
                        "name": "Tracking Number",
                        "value": tracking_number,
                        "inline": True
                    },
                    {
                        "name": "Status",
                        "value": status,
                        "inline": True
                    },
                    {
                        "name": "Text",
                        "value": simplifiedText,
                        "inline": True
                    },
                    {
                        "name": "Street Address",
                        "value": streetAddress1,
                        "inline": True
                    },
                    {
                        "name": "City",
                        "value": city,
                        "inline": True
                    },
                    {
                        "name": "Country",
                        "value": country,
                        "inline": True
                    },
                    {
                        "name": "Zip Code",
                        "value": zipCode,
                        "inline": True
                    },
                    {
                        "name": "Name",
                        "value": attentionName,
                        "inline": True
                    }
                ]
            }
        ]
    }
    result = requests.post(
        webhook, data=json.dumps(data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
