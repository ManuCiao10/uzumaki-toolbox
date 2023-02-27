from handler.utils import *
import os
import requests
import platform

api_key = "***REMOVED***"


def update():
    cookies = {
        "authorization": "edjOnQx1qVIcRZnhwrqxK",
    }

    headers = {
        "authority": "uzumakitools.hyper.co",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "hyper-account": "I_lF5bu5kFr1JAp-Wyu3W",
        "hyper-env": "portal",
        "pragma": "no-cache",
        "referer": "https://uzumakitools.hyper.co/dashboard",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }

    params = ""

    response = requests.get(
        "https://uzumakitools.hyper.co/ajax/products/w4AR4dZsZ4njJ6Y815DRK/files",
        params=params,
        cookies=cookies,
        headers=headers,
    )

    if response.status_code != 200:
        print_task("Failed to check for updates!", RED)
        input("Press Enter to exit...")
        return

    try:
        data = response.json()
        print(data)
        #get latest version
        latest_version = data["data"][0]["filename"].split("_")[1][:-1]
        if latest_version != VERSION:
            print_task("New version available!", GREEN)
            

    except:
        print_task("Failed to check for updates!", RED)
        input("Press Enter to exit...")
        return


def get_license(license_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    req = requests.get(
        f"https://api.hyper.co/v6/licenses/{license_key}", headers=headers
    )
    if req.status_code == 200:
        return req.json()

    return None


def auth():
    settings = load_settings()
    webhook = settings["webhook"]
    key = settings["key"]

    if not key or key == "KEY HERE":
        print_task("please set key...", RED)
        input("Press Enter to exit...")
        os._exit(1)

    license_data = get_license(key)

    if license_data:
        if license_data.get("metadata") != {}:
            print_task("License is already in use on another machine!", RED)
            input("Press Enter to exit...")
            os._exit(1)
    else:
        print_task("Invalid license key!", RED)
        input("Press Enter to exit...")
        os._exit(1)

    username = license_data.get("integrations").get("discord").get("username")

    if not webhook or webhook == "WEBHOOK HERE":
        print_task("please set webhook...", RED)
        input("Press Enter to exit...")
        os._exit(1)

    return username
