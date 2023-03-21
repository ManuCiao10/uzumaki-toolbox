from handler.utils import *
import os
import requests
import platform
import sys
import time

api_key = "***REMOVED***"


def update():
    print_task("checking for updates...", PURPLE)
    supported = ["Windows", "Darwin"]

    if platform.system() not in supported:
        print_task("Platform not supported", RED)
        exit_program()

    cookies = {
        "authorization": "YiDX0QjGN17Ex2ApMVbyl",
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
        print_task("Failed to get response for update", RED)
        time.sleep(3)
        return

    try:
        data = response.json()
    except Exception as e:
        print_task("error checking software version:" + str(e), RED)
        exit_program()

    version = os.path.basename(sys.argv[0])

    try:
        if platform.system() == "Darwin":
            version = version.split("_")[1][:-1]
        elif platform.system() == "Windows":
            version = version.split("_")[1][:-4]
    except Exception as e:
        print_task("error checking software version:" + str(e), RED)
        time.sleep(3)
        return

    hyper_version = data.get("data")

    for i in hyper_version:
        if platform.system() == "Darwin":
            if i.get("type") == "application/octet-stream":
                hyper_version = i.get("filename")
                hyper_version = hyper_version.split("_")[1][:-1]
                break
        elif platform.system() == "Windows":
            if i.get("type") == "exe":
                hyper_version = i.get("filename")
                hyper_version = hyper_version.split("_")[1][:-4]
                break

    if version != hyper_version:
        print_task("New update available!", GREEN)

        id = getID(data)

        response = requests.get(
            "https://uzumakitools.hyper.co/ajax/files/" + id,
            cookies=cookies,
            headers=headers,
        )

        if platform.system() == "Windows":
            with open("Uzumaki_" + hyper_version + ".exe", "wb") as f:
                f.write(response.content)
        elif platform.system() == "Darwin":
            with open("Uzumaki_" + hyper_version, "wb") as f:
                f.write(response.content)
            #rename file
            os.rename("Uzumaki_" + hyper_version, "Uzumaki_" + hyper_version + ".")
            #assign execute permissions
            os.chmod("Uzumaki_" + hyper_version + ".", 0o777)

        print_task("Successfully downloaded update, check" + os.getcwd(), GREEN)
        exit_program()
    else:
        print_task("uzumaki is up to date", YELLOW)


def getID(data):
    for i in data.get("data"):
        if platform.system() == "Windows":
            if i.get("type") == "exe":
                return i.get("id")
        elif platform.system() == "Darwin":
            if i.get("type") == "application/octet-stream":
                return i.get("id")


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
        exit_program()

    license_data = get_license(key)

    if license_data:
        if license_data.get("metadata") != {}:
            print_task("License is already in use on another machine!", RED)
            exit_program()
    else:
        print_task("Invalid license key!", RED)
        exit_program()

    username = license_data.get("integrations").get("discord").get("username")

    if not webhook or webhook == "WEBHOOK HERE":
        print_task("please set webhook...", RED)
        exit_program()

    return username
