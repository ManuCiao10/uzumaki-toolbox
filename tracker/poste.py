import requests
from handler.utils import *
from handler.webhook import poste_webhook
import time
from datetime import datetime

def poste(tracking_number, zip_code):
    print_task(f"[poste {tracking_number}] getting order...", YELLOW)

    headers = {
        "authority": "jouw.postnl.nl",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://jouw.postnl.nl/track-and-trace/3SJJMY000372141-NL-6952HS?language=en",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }

    params = {
        "language": "en",
    }

    try:
        response = requests.get(
            f"https://jouw.postnl.nl/track-and-trace/api/trackAndTrace/{tracking_number}-NL-{zip_code}",
            params=params,
            headers=headers,
        )
        resp = response.json()
        print_task(f"[poste {tracking_number}] got order", PURPLE)
    except requests.exceptions.ConnectionError:
        print_task(f"[poste {tracking_number}] connection error", RED)
        time.sleep(3)
        return

    except requests.exceptions.Timeout:
        print_task(f"[poste {tracking_number}] connection timeout", RED)
        time.sleep(3)
        return

    except Exception as e:
        print_task(f"[poste {tracking_number}] {e}", RED)
        time.sleep(3)
        return
    
    try:
        colli = resp["colli"][f"{tracking_number}"]
        effectiveDate = colli["effectiveDate"]
        effectiveDate = effectiveDate.split("T")[0]
        sender = colli["sender"]["names"]["personName"]
        if sender == "":
            sender = colli["sender"]["names"]["companyName"]
        deliveryAddress = colli["deliveryAddress"]["names"]["personName"]
        if deliveryAddress == "":
            deliveryAddress = colli["deliveryAddress"]["names"]["companyName"]
        street = colli["deliveryAddress"]["address"]["street"]
        houseNumber = colli["deliveryAddress"]["address"]["houseNumber"]
        postalCode = colli["deliveryAddress"]["address"]["postalCode"]
        town = colli["deliveryAddress"]["address"]["town"]
        country = colli["deliveryAddress"]["address"]["country"]
        status = colli["statusPhase"]["message"]
        
        poste_webhook(
            tracking_number,
            zip_code,
            effectiveDate,
            sender,
            deliveryAddress,
            street,
            houseNumber,
            postalCode,
            town,
            country,
            status,
        )
    except Exception as e:
        print_task(f"[poste {tracking_number}] json {e}", RED)
        time.sleep(3)
        return
