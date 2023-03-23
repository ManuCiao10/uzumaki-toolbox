from handler.utils import *
import os
import requests
import platform
from io import BytesIO
from zipfile import ZipFile
import time
from urllib.request import urlopen

HYPER_API_KEY = "***REMOVED***"
GITHUB_API_KEY = "***REMOVED***"

def getGithubVersion():
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + GITHUB_API_KEY,
        "X-GitHub-Api-Version": "2022-11-28",
    }

    try:
        response = requests.get(
            "https://api.github.com/repos/ManuCiao10/uzumaki-update/releases/latest",
            headers=headers,
        )
        data = response.json()
        version = data.get("tag_name")
        version = version.replace("v", "")
        url_download = data.get("assets")[0].get("browser_download_url")
    except requests.exceptions.RequestException as e:
        print_task("Error: " + str(e), RED)
        time.sleep(2)
        return
    except Exception as e:
        print_task("Error: " + str(e), RED)
        time.sleep(2)
        return

    return version, url_download


def update():
    print_task("checking for updates...", PURPLE)
    
    github_version, url_download = getGithubVersion()
    if not github_version:
        print_task("Error getting version", RED)
        time.sleep(2)
        return
    
    if not url_download:
        print_task("Error getting download url", RED)
        time.sleep(2)
        return

    if VERSION != github_version:
        print_task(f"new update available v{github_version}", YELLOW)
        try:
            resp = urlopen(url_download)
        except requests.exceptions.RequestException as e:
            print_task("Error RequestException: " + str(e), RED)
            time.sleep(2)
            return

        except Exception as e:
            print_task("Error Exception: " + str(e), RED)
            time.sleep(2)
            return

        try:
            with open(f"Uzumaki_{github_version}.exe", "wb") as f:
                f.write(resp.read())
        except Exception as e:
            print_task("Error: " + str(e), RED)
            time.sleep(2)
            return
        
        #delete old version
        for file in os.listdir():
            if file.startswith("Uzumaki") and file.endswith(".exe") and file != f"Uzumaki_{github_version}.exe":
                print_task("removing old version", WHITE)
                os.remove(file)

        print_task("Successfully downloaded update, check" + os.getcwd(), GREEN)
        exit_program()
    else:
        print_task("uzumaki is up to date", YELLOW)


def get_license(license_key):
    headers = {
        "Authorization": f"Bearer {HYPER_API_KEY}",
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
