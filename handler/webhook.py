from handler.utils import *
import requests
import json


def redirect_webhook_brt(
    company, tracking_number, name, phone, address, city, state, zip, url, email
):
    settings = load_settings()
    webhook = settings["webhook"]

    url_ = url

    data = {
        "username": "Uzumaki™",
        "avatar_url": LOGO,
        "content": " ",
        "embeds": [
            {
                "title": "Tracking Number",
                "url": url_,
                "color": 3128760,
                "description": "> Successfully redirect your parcel!",
                "footer": {"text": "by Uzumaki Tools", "icon_url": LOGO},
                "fields": [
                    {"name": "Company", "value": company.upper(), "inline": True},
                    {
                        "name": "Tracking Number",
                        "value": tracking_number,
                        "inline": False,
                    },
                    {"name": "Name", "value": name, "inline": True},
                    {"name": "Phone", "value": phone, "inline": True},
                    {"name": "Address", "value": address, "inline": True},
                    {"name": "City", "value": city, "inline": True},
                    {"name": "State", "value": state, "inline": True},
                    {"name": "Zip", "value": zip, "inline": True},
                    {"name": "Email", "value": email, "inline": True},
                ],
            }
        ],
    }

    result = requests.post(
        webhook, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)


def send_webhook_sda(tracking_number, date, city, status):
    settings = load_settings()
    webhook = settings["webhook"]

    url: str = ""

    url = (
        "https://www.sda.it/wps/portal/Servizi_online/dettaglio-spedizione?locale=it&tracing.letteraVettura="
        + tracking_number
    )

    data = {
        "username": "Uzumaki™",
        "avatar_url": LOGO,
        "content": " ",
        "embeds": [
            {
                "title": "Tracking Number",
                "url": url,
                "color": 3128760,
                "footer": {"text": "Powered by Uzumaki Tools", "icon_url": LOGO},
                "fields": [
                    {"name": "Company", "value": "SDA", "inline": True},
                    {"name": "Date", "value": date, "inline": True},
                    {"name": "City", "value": city, "inline": False},
                    {"name": "Status", "value": status, "inline": True},
                ],
            }
        ],
    }

    result = requests.post(
        webhook, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )

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
        url = (
            "https://www.mybrt.it/it/mybrt/my-parcels/search?lang=en&parcelNumber="
            + tracking_number
        )

    data = {
        "username": "Uzumaki™",
        "avatar_url": LOGO,
        "content": " ",
        "embeds": [
            {
                "title": "Tracking Number",
                "url": url,
                "color": 3128760,
                "footer": {"text": "Powered by Uzumaki Tools", "icon_url": LOGO},
                "fields": [
                    {"name": "Company", "value": "BRT", "inline": True},
                    {"name": "Status", "value": status, "inline": True},
                    {"name": "Date", "value": date, "inline": True},
                    {"name": "Time", "value": time, "inline": True},
                    {"name": "Branch", "value": location, "inline": True},
                ],
            }
        ],
    }

    result = requests.post(
        webhook, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)


def send_webhook(
    company,
    tracking_number,
    status,
    simplifiedText,
    streetAddress1,
    city,
    country,
    zipCode,
    attentionName,
):
    # https://www.mathsisfun.com/hexadecimal-decimal-colors.html

    settings = load_settings()
    webhook = settings["webhook"]

    import requests
    import json

    url: str = ""

    if company == "ups":
        url = (
            "https://www.ups.com/track?loc=en_IT&tracknum="
            + tracking_number
            + "&requester=ST/trackdetails"
        )
    data = {
        "username": "Uzumaki™",
        "avatar_url": LOGO,
        "content": " ",
        "embeds": [
            {
                "title": "Tracking Number",
                "url": url,
                "color": 3128760,
                "footer": {"text": "Powered by Uzumaki Tools", "icon_url": LOGO},
                "thumbnail": {"url": LOGO},
                "fields": [
                    {"name": "Company", "value": company, "inline": True},
                    {
                        "name": "Tracking Number",
                        "value": tracking_number,
                        "inline": True,
                    },
                    {"name": "Status", "value": status, "inline": True},
                    {"name": "Text", "value": simplifiedText, "inline": True},
                    {"name": "Street Address", "value": streetAddress1, "inline": True},
                    {"name": "City", "value": city, "inline": True},
                    {"name": "Country", "value": country, "inline": True},
                    {"name": "Zip Code", "value": zipCode, "inline": True},
                    {"name": "Name", "value": attentionName, "inline": True},
                ],
            }
        ],
    }
    result = requests.post(
        webhook, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)


def webhook_nike(
    price: str,
    name: str,
    url_image: str,
    size: str,
    lineItemStatus: str,
    address: str,
    city: str,
    country: str,
    zip: str,
    tracklink: str,
    tracking_number: str,
):
    settings = load_settings()
    webhook = settings["webhook"]

    import requests
    import json

    data = {
        "username": "Uzumaki™",
        "avatar_url": LOGO,
        "content": " ",
        "embeds": [
            {
                "title": "Tracking Number",
                "url": tracklink,
                "color": 3128760,
                "footer": {"text": "Powered by Uzumaki Tools", "icon_url": LOGO},
                "thumbnail": {"url": url_image},
                "fields": [
                    {"name": "Status", "value": lineItemStatus, "inline": False},
                    {"name": "Price", "value": price + "€", "inline": True},
                    {"name": "Name", "value": name, "inline": True},
                    {"name": "Size", "value": size, "inline": True},
                    {"name": "Address", "value": address, "inline": True},
                    {"name": "City", "value": city, "inline": True},
                    {"name": "Country", "value": country, "inline": True},
                    {"name": "Zip", "value": zip, "inline": True},
                    {
                        "name": "Order Number",
                        "value": tracking_number,
                        "inline": True,
                    },
                ],
            }
        ],
    }
    result = requests.post(
        webhook, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
