from handler.utils import *
from handler.webhook import send_webhook
import time


def ups(tracking_number):
    import requests

    session = requests.Session()

    headers = {
        "authority": "www.ups.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    }

    params = {
        "loc": "en_IT",
        "tracknum": tracking_number,
        "requester": "ST/trackdetails",
    }

    try:
        response = session.get(
            "https://www.ups.com/track", params=params, headers=headers
        )

        if response.status_code != 200:
            print_task("[ups %s] failed to get session..." % tracking_number, RED)
            time.sleep(3)
            return

        print_task("[ups %s] successful got session..." % tracking_number, YELLOW)

        token_ = response.cookies["X-XSRF-TOKEN-ST"]

        refer = (
            "https://www.ups.com/track?loc=en_IT&tracknum="
            + tracking_number
            + "&requester=ST%2Ftrackdetails%2Ftrackdetails%2Ftrackdetails%2Ftrackdetails"
        )

        headers = {
            "authority": "www.ups.com",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "https://www.ups.com",
            "pragma": "no-cache",
            "referer": refer,
            "sec-ch-ua": '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "x-xsrf-token": token_,
        }

        params = {
            "loc": "en_IT",
        }

        json_data = {
            "Locale": "en_IT",
            "TrackingNumber": [
                tracking_number,
            ],
            "Requester": "st/trackdetails/trackdetails/trackdetails",
            "returnToValue": "",
        }

        response = session.post(
            "https://www.ups.com/track/api/Track/GetStatus",
            params=params,
            headers=headers,
            json=json_data,
        )

        if response.json()["statusCode"] != "200":
            print_task(f"[ups {tracking_number}] error: {response.status_code}", RED)
            time.sleep(3)
            return

        try:
            track_details = response.json()["trackDetails"][0]

            package_status = track_details.get("packageStatus")
            deliveredDate = track_details.get("deliveredDate")
            shipmentProgressActivities = track_details.get("shipmentProgressActivities")

            time_stamp = shipmentProgressActivities[0].get("time")
            location = shipmentProgressActivities[0].get("location")
        except:
            print_task(f"[ups {tracking_number}] error: invalid response format", RED)
            time.sleep(3)
            return

        data = {
            "tracking_number": tracking_number,
            "package_status": package_status,
            "delivered_date": deliveredDate,
            "time_stamp": time_stamp,
            "location": location,
        }

        print_task(f"[ups {tracking_number}] successful got data...", PURPLE)

        send_webhook(data)

    except Exception as e:
        print_task(f"[ups {tracking_number}] error: {e}", RED)
        time.sleep(3)
        return
