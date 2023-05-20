from handler.utils import *
import os
import requests
import time
from urllib.request import urlopen
import os


def authWhop() -> str:
    settings = load_settings()
    webhook = settings["webhook"]
    licenseKey = settings["key"]

    if not licenseKey or licenseKey == "KEY HERE":
        print_task("please set key... [from Whop dashboard]", RED)
        exit_program()

    if not webhook or webhook == "WEBHOOK HERE":
        print_task("please set webhook...", RED)
        exit_program()

    HWID = get_hwid()

    url = f"https://api.whop.com/api/v2/memberships/{licenseKey}/validate_license"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {WHOP_API_KEY}",
        "content-type": "application/json",
    }

    response = requests.post(
        url,
        headers=headers,
        json={"metadata": {"HWID": HWID}},
    )

    try:
        response = response.json()
    except requests.exceptions.JSONDecodeError:
        print_task("Backend login error.", RED)
        exit_program()

    error = response.get("error")
    if error and error.get("message"):
        error_msg = error["message"]
        print_task(error_msg, RED)
        exit_program()

    if response.get("banned"):
        print_task("License key is banned.", RED)
        exit_program()

    if response.get("is_scammer"):
        print_task("License key is marked as a scammer.", RED)
        exit_program()

    if response.get("valid") != True:
        print_task("License key is invalid.", RED)
        exit_program()

    discord_info = response.get("discord")
    if discord_info and "username" in discord_info:
        username = discord_info["username"]
        return username.split("#")[0]
    else:
        print_task("Discord info not found.", RED)
        exit_program()


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

    try:
        github_version, url_download = getGithubVersion()
    except TypeError:
        print_task("No version found", RED)
        time.sleep(2)
        return

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

        # delete old version
        for file in os.listdir():
            if (
                file.startswith("Uzumaki")
                and file.endswith(".exe")
                and file != f"Uzumaki_{github_version}.exe"
            ):
                # give the permission to delete the file
                try:
                    print_task("removing old version", WHITE)
                    os.chmod(file, 0o777)
                    os.remove(file)
                except OSError:
                    print_task("Error permission while deleting old version", RED)
                    pass

        print_task("Successfully downloaded update " + os.getcwd(), GREEN)
        exit_program()
