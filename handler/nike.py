from handler.utils import *
import requests


def nike(tracking_number, email):
    if len(email) == 0:
        print_task("[nike %s] email is required" % tracking_number, RED)
        time.sleep(3)
        os._exit(1)

    headers = {
        "authority": "www.nike.com",
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
    session = requests.Session()
    try:
        response = session.get("https://www.nike.com/orders/details/", headers=headers)

        if response.status_code == 200:
            print_task("[nike %s] successful got session..." % tracking_number, PURPLE)

    except requests.exceptions.ConnectionError:
        print_task(
            "[nike %s] error: %s" % (tracking_number, "error connecting to nike..."),
            RED,
        )
        time.sleep(3)
        os._exit(1)

    headers = {
        "authority": "api.nike.com",
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "nike-api-caller-id": "com.nike:sse.orders",
        "origin": "https://www.nike.com",
        "pragma": "no-cache",
        "referer": "https://www.nike.com/",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "x-nike-visitid": "1",
        "x-nike-visitorid": "49655fc2-c618-4b1a-8700-99adea557fb4",
    }

    params = {
        "locale": "en_us",
        "country": "US",
        "language": "en",
        "email": email,
        "timezone": "Europe/Rome",
    }

    try:
        response = session.get(
            "https://api.nike.com/orders/summary/v1/" + tracking_number,
            params=params,
            headers=headers,
        )

        try:
            data = response.json()
            print(data)
            error = data.get("errors")[0].get("message")

            if error == "Order Not Found":
                print_task(
                    "[nike %s] error: %s"
                    % (tracking_number, "Order Not Found..."),
                    RED,
                )
                time.sleep(3)
                os._exit(1)

            print_task("[nike %s] successful got order..." % tracking_number, GREEN)
            
            price = data.get("transaction")
            status = data.get("group")[0].get("heading")
            print(price, status)
            # item_name = data.get("lineItems")[0].get("product").get("name")


        except ValueError:
            print_task(
                "[nike %s] error: %s"
                % (tracking_number, "invalid or unavailable order..."),
                RED,
            )
            time.sleep(3)
            os._exit(1)

    except requests.exceptions.ConnectionError:
        print_task("connection error", RED)
        time.sleep(3)
        os._exit(1)
