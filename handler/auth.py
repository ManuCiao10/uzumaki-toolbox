from handler.utils import print_task, RED, load_settings
import time
import os
import requests

api_key = "***REMOVED***"


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

    if key == "KEY HERE" or key == "":
        print_task("please set key...", RED)
        time.sleep(3)
        os._exit(1)

    license_data = get_license(key)

    if license_data:
        if license_data.get("metadata") != {}:
            print_task("License is already in use on another machine!", RED)
            time.sleep(3)
            os._exit(1)
    else:
        print_task("Invalid license key!", RED)
        time.sleep(3)
        os._exit(1)

    username = license_data.get("integrations").get("discord").get("username")

    if webhook == "WEBHOOK HERE" or webhook == "":
        print_task("please set webhook...", RED)
        time.sleep(3)
        os._exit(1)


    return username
