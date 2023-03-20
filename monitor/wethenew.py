# response in the page quicktask started
# do the login
# sell the shoes

import socket
import tls_client
from handler.utils import *
import jwt
from internal.security import processRunning


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

    print_task("Wethenew QuickTask is waiting...", WHITE)

    # Wait for a connection
    conn, _ = s.accept()

    # Print a message when a connection is received
    print_task(f"starting Wethenew QuickTask...", PURPLE)

    # post the response in the page quicktask started
    response = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
    response += b"<html><body><h1>QuickTask Started</h1></body></html>"
    conn.sendall(response)

    # Receive data from the connection
    data = conn.recv(1024)

    # http://localhost:8080/url=https://sell.wethenew.com/instant-sales/6290
    url = data.decode().split("\n")[0].split()[1].split("=")[1]

    # call the wethenew function
    login(credentials["email"], credentials["password"], url)

    # Close the connection
    conn.close()


def get_bearer_token() -> str:
    timestamp = int(time.time())

    # timestamp_exp = timestamp + 2592000
    secret_key = ""

    # Set the payload data
    payload = {
        "email": "emanuele.ardinghi@gmail.com",
        "firstname": "emanuele",
        "lastname": "ardinghi",
        "iat": 1679260653,
        "exp": 1684444653,
    }

    return jwt.encode(payload, secret_key, algorithm="HS256")


def login(email: str, password: str, url: str):
    session = tls_client.Session(client_identifier="chrome_105")

    Bearer_token = get_bearer_token()
    print(Bearer_token)
    # print(Bearer_token)
    session.headers = {
        "authority": "api-sell.wethenew.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "authorization": "Bearer " + Bearer_token,
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

    response = session.get("https://api-sell.wethenew.com/payment_infos")
    print(response.json())
