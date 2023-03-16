from handler.utils import *
import requests
from handler.webhook import correos_webhook


def correos(tracking_number):
    setTitleMode(f"tracker - correos")

    print_task("[correos %s] getting session..." % tracking_number, PURPLE)

    params = {
        "text": tracking_number,
        "language": "ES",
        "searchType": "envio",
    }

    try:
        response = requests.get(
            "https://api1.correos.es/digital-services/searchengines/api/v1/",
            params=params,
        )
    except requests.exceptions.HTTPError as err:
        print_task(f"[correos {tracking_number}] {err}", RED)
        time.sleep(3)
        return

    except Exception as err:
        print_task(f"[correos {tracking_number}] {err}", RED)
        time.sleep(3)
        return

    try:
        data = response.json()
        type = data["type"]
        quatity = data["expedition"]["numPackages"]

        events = data["shipment"][0]["events"]

        # loop through events in reverse order
        for event in events:
            eventDate = event["eventDate"]
            eventTime = event["eventTime"]
            summaryText = event["summaryText"]
            extendedText = event["extendedText"]

        date_delivery_sum = data["shipment"][0]["date_delivery_sum"]

        correos_webhook(
            tracking_number,
            type,
            quatity,
            date_delivery_sum,
            summaryText,
            extendedText,
            eventDate,
            eventTime,
        )

    except Exception as err:
        print_task(f"[correos {tracking_number}] {err}", RED)
        time.sleep(3)
        return
