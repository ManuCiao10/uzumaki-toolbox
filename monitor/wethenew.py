import socket
import tls_client
from handler.utils import *
from twocaptcha import TwoCaptcha
from internal.security import processRunning
from handler.webhook import webhook_wethenew


def wethenew(username):
    processRunning()
    setTitleMode("Wethenew QuickTask")

    try:
        os.chdir("Uzumaki/wethenew")
    except:
        print_task("error finding directory", RED)
        input("Press Enter to exit...")
        os._exit(1)

    os.system("cls" if os.name == "nt" else "clear")

    print(f"{RED}{BANNER}{RESET}")

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    try:
        with open("login.json", "r") as f:
            credentials = json.load(f)

        if not validate_wethenew(credentials):
            print_task("please fill wethenew/login.json", RED)
            input("Press Enter to exit...")
            os._exit(1)

    except:
        print_task("error getting credentials", RED)
        input("Press Enter to exit...")
        os._exit(1)

    HOST = "127.0.0.1"  # Listen on localhost
    PORT = 8080  # Use port 8080

    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a local address
    try:
        s.bind((HOST, PORT))
    except socket.error as e:
        print_task(f"{str(e)}", RED)
        input("Press Enter to exit...")
        os._exit(1)

    # Listen for incoming connections
    s.listen()

    checkoutToken, uuid_payment, uuid_address = payload(
        credentials["email"], credentials["password"]
    )

    print_task("Wethenew QuickTask is waiting...", WHITE)

    # Wait for a connection
    conn, _ = s.accept()

    # Print a message when a connection is received
    print_task(f"Reiceved Wethenew QuickTask...", PURPLE)

    # post the response in the page quicktask started
    response = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
    response += b"<html><body><h1>QuickTask Started</h1></body></html>"
    conn.sendall(response)

    # Receive data from the connection
    data = conn.recv(1024)

    # http://localhost:8080/url=https://sell.wethenew.com/instant-sales/6290
    url = data.decode().split("\n")[0].split()[1].split("=")[1]

    checkout(url, checkoutToken, uuid_payment, uuid_address)

    # Close the connection
    conn.close()


def payload(email: str, password: str) -> tuple:
    print_task(f"starting Wethenew QuickTask", PURPLE)

    session = tls_client.Session(client_identifier="chrome_105")

    solver = TwoCaptcha("2715cf93c9fb0ef644a452ba7a6990f1")
    sitekey = "6LeJBSAdAAAAACyoWxmCY7q5G-_6GnKBdpF4raee"
    url_key = "https://sell.wethenew.com/login"

    try:
        recaptchaToken = solver.recaptcha(sitekey=sitekey, url=url_key)
        recaptchaToken = recaptchaToken["code"]
    except Exception as e:
        print_task(f"error captha: {str(e)}", RED)
        input("Press Enter to exit...")
        os._exit(1)

    session.headers = {
        "authority": "sell.wethenew.com",
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://sell.wethenew.com/login",
        "sec-ch-ua": '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    }

    try:
        response = session.get("https://sell.wethenew.com/api/auth/csrf")
        csrf_token = response.json()["csrfToken"]
    except Exception as e:
        print_task(f"error cloudflare: {str(e)}", RED)
        input("Press Enter to exit...")
        os._exit(1)

    params = ""

    payload_data = {
        "redirect": "false",
        "email": email,
        "password": password,
        "recaptchaToken": recaptchaToken,
        "pushToken": "undefined",
        "os": "undefined",
        "osVersion": "undefined",
        "csrfToken": csrf_token,
        "callbackUrl": "https://sell.wethenew.com/login",
        "json": "true",
    }

    try:
        response = session.post(
            "https://sell.wethenew.com/api/auth/callback/credentials",
            params=params,
            data=payload_data,
        )

    except Exception as e:
        print_task(f"error credentials: {str(e)}", RED)
        input("Press Enter to exit...")
        os._exit(1)

    try:
        response = session.get("https://sell.wethenew.com/api/auth/session")
        token_bearer = response.json()["user"]["accessToken"]

    except Exception as e:
        print_task(f"error auth|session: {str(e)}", RED)
        input("Press Enter to exit...")
        os._exit(1)

    session.headers = {
        "authority": "api-sell.wethenew.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "authorization": "Bearer " + token_bearer,
        "cache-control": "no-cache",
        "feature-policy": "microphone 'none'; geolocation 'none'; camera 'none'; payment 'none'; battery 'none'; gyroscope 'none'; accelerometer 'none';",
        "origin": "https://sell.wethenew.com",
        "pragma": "no-cache",
        "referer": "https://sell.wethenew.com/",
        "sec-ch-ua": '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "x-xss-protection": "1;mode=block",
    }

    try:
        response = session.get("https://api-sell.wethenew.com/payment_infos")
        data = response.json()
    except Exception as e:
        print_task(f"error payment_infos: {str(e)}", RED)
        input("Press Enter to exit...")
        os._exit(1)

    try:
        uuid_payment = data[0]["uuid"]
    except Exception as e:
        print_task(f"check your payment info: {str(e)}", RED)
        input("Press Enter to exit...")
        os._exit(1)

    try:
        response = session.get("https://api-sell.wethenew.com/addresses")
        data = response.json()
    except Exception as e:
        print_task(f"error addresses: {str(e)}", RED)
        input("Press Enter to exit...")
        os._exit(1)

    try:
        uuid_bank = data[0]["uuid"]
    except Exception as e:
        print_task(f"check your addresses info: {str(e)}", RED)
        input("Press Enter to exit...")
        os._exit(1)

    return token_bearer, uuid_payment, uuid_bank


def checkout(url, checkoutToken, uuid_payment, uuid_address):
    session = tls_client.Session(client_identifier="chrome_105")

    session.headers = {
        "authority": "api-sell.wethenew.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "authorization": "Bearer " + checkoutToken,
        "cache-control": "no-cache",
        "feature-policy": "microphone 'none'; geolocation 'none'; camera 'none'; payment 'none'; battery 'none'; gyroscope 'none'; accelerometer 'none';",
        "origin": "https://sell.wethenew.com",
        "pragma": "no-cache",
        "referer": "https://sell.wethenew.com/",
        "sec-ch-ua": '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "x-xss-protection": "1;mode=block",
    }

    try:
        response = session.get(
            f"https://api-sell.wethenew.com/sell-nows/{url.split('/')[-1]}"
        )
        resp = response.json()
    except Exception as e:
        print_task(f"error getting shoes data: {str(e)}", RED)
        input("Press Enter to exit...")
        os._exit(1)

    id = resp["id"]
    variant_id = resp["variantId"]
    image = resp["image"]
    name = resp["name"]
    size = resp["size"]
    price = resp["price"]

    json_data = {
        "sellNowId": id,
        "variantId": variant_id,
        "paymentInfosUuid": uuid_payment,
        "isTermsAndConditionsAccepted": True,
        "addressUuid": uuid_address,
    }

    try:
        response = session.post(
            "https://api-sell.wethenew.com/sell-nows", json=json_data
        )
        if "Problem ocurred while processing seller info" in response.text:
            print_task("Problem ocurred while processing seller info", RED)
            input("Press Enter to exit...")
            os._exit(1)

    except Exception as e:
        print_task(f"error posting shoes data: {str(e)}", RED)
        input("Press Enter to exit...")
        os._exit(1)

    webhook_wethenew(url, image, name, size, price)
