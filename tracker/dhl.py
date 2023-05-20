from handler.utils import *
from handler.webhook import dhl_webhook
import requests


def dhl(tracking_number):
    setTitleMode("tracker - dhl")
    print_task(f"[dhl {tracking_number}] getting order...", YELLOW)

    url = "https://api-eu.dhl.com/track/shipments"

    querystring = {"trackingNumber": tracking_number}

    headers = {"DHL-API-Key": "DHL_API_Key"}

    response = requests.request("GET", url, headers=headers, params=querystring)

    try:
        resp = response.json()
        if resp["title"] == "No result found":
            print_task(
                f"[dhl {tracking_number}] no result found for the given tracking number",
                RED,
            )
            time.sleep(3)
            return
    except KeyError:
        pass

    try:
        service = resp["shipments"][0]["service"]
        if service == "express":
            origin = resp["shipments"][0]["origin"]["address"]["addressLocality"]
            destination = resp["shipments"][0]["destination"]["address"][
                "addressLocality"
            ]
            weight = "N/A"
            unit = ""

        else:
            origin = resp["shipments"][0]["origin"]["address"]["countryCode"]
            destination = resp["shipments"][0]["destination"]["address"]["countryCode"]
            weight = resp["shipments"][0]["details"]["weight"]["value"]
            unit = resp["shipments"][0]["details"]["weight"]["unitText"]

        status = resp["shipments"][0]["status"]["statusCode"]
        text = resp["shipments"][0]["status"]["status"]
        location = resp["shipments"][0]["events"][0]["location"]["address"][
            "addressLocality"
        ]

        print_task(f"[dhl {tracking_number}] got order", PURPLE)
        dhl_webhook(
            tracking_number,
            service,
            origin,
            destination,
            status,
            text,
            weight,
            unit,
            location,
        )

    except Exception as e:
        print_task(f"[dhl {tracking_number}] error: {e}", RED)
        time.sleep(3)
        return
