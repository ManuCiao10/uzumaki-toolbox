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
DOWNLOAD_URL = (
    "https://github.com/ManuCiao10/uzumaki-update/releases/latest/download/Archive.zip"
)


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
        version = response.json().get("tag_name")
        version = version.replace("v", "")
    except requests.exceptions.RequestException as e:
        print_task("Error: " + str(e), RED)
        time.sleep(2)
        return
    except Exception as e:
        print_task("Error: " + str(e), RED)
        time.sleep(2)
        return

    return version


def update():
    print_task("checking for updates...", PURPLE)
    supported = ["Windows", "Darwin"]
    PLATFORM = platform.system()

    if PLATFORM not in supported:
        print_task("Platform not supported", RED)
        exit_program()

    github_version = getGithubVersion()
    if not github_version:
        print_task("Error getting version", RED)
        return

    if VERSION != github_version:
        print_task(f"new update available v{github_version}", YELLOW)

        try:
            resp = urlopen(DOWNLOAD_URL)
            myzip = ZipFile(BytesIO(resp.read()))
        except requests.exceptions.RequestException as e:
            print_task("Error RequestException: " + str(e), RED)
            time.sleep(2)
            return

        except Exception as e:
            print_task("Error Exception: " + str(e), RED)
            time.sleep(2)
            return

        try:
            for file in myzip.namelist():
                if PLATFORM == "Windows":
                    if file.endswith(".exe") and file.startswith("Uzumaki"):
                        new = file
                        with open(file, "wb") as f:
                            f.write(myzip.read(file))
                    for file in os.listdir():
                        if (
                            file.startswith("Uzumaki")
                            and file != new
                            and file.endswith(".exe")
                        ):
                            print_task("removing old version", YELLOW)
                            os.remove(file)
                elif PLATFORM == "Darwin":
                    if file.endswith(".") and file.startswith("Uzumaki"):
                        new = file
                        with open(file, "wb") as f:
                            f.write(myzip.read(file))
                    for file in os.listdir():
                        if (
                            file.startswith("Uzumaki")
                            and file != new
                            and file.endswith(".")
                        ):
                            print_task("removing old version", YELLOW)
                            os.remove(file)
        except Exception as e:
            print_task("Error myzip: " + str(e), RED)
            time.sleep(2)
            return

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
