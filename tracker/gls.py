from handler.utils import print_task, YELLOW, RED, PURPLE
from handler.webhook import gls_webhook
import requests
import time
from bs4 import BeautifulSoup


def gls(tracking_number):
    """Handles GLS tracking."""

    print_task(f"[gls {tracking_number}] getting order...", YELLOW)

    headers = {
        "Accept": "application/json",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": f"https://gls-group.com/IT/it/servizi-online/ricerca-spedizioni.html?match={tracking_number}&type=NAT",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    params = {
        "match": tracking_number,
        "type": "NAT",
        "caller": "witt002",
        "millis": "1678419911445",
    }

    try:
        response = requests.get(
            "https://gls-group.com/app/service/open/rest/IT/it/rstt001",
            params=params,
            headers=headers,
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as err:
        print_task(f"[gls {tracking_number}] {err}", RED)
        time.sleep(3)
        return

    try:
        shipper = data["tuStatus"][0]["addresses"][1]["value"]["name1"]
        receiver = data["tuStatus"][0]["addresses"][3]["value"]["name1"]
    except Exception:
        shipper = ""
        receiver = ""

    try:
        status = data["tuStatus"][0]["history"][0]["evtDscr"]
        location = data["tuStatus"][0]["history"][0]["address"]["city"]
        date = data["tuStatus"][0]["history"][0]["date"]
        time = data["tuStatus"][0]["history"][0]["time"]
    except Exception:
        status = ""
        location = ""
        date = ""
        time = ""

    gls_webhook(
        tracking_number,
        shipper,
        receiver,
        status,
        location,
        date,
        time,
    )
