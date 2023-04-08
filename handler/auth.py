from handler.utils import *
import os
import requests
import time
from urllib.request import urlopen
import hashlib
import os
import getpass

HYPER_API_KEY = "***REMOVED***"
GITHUB_API_KEY = "***REMOVED***"
WHOP_API_KEY = "***REMOVED***"


def get_hwid():
    # sha256(Disk Serials (sep by comma) + Computer Name + Running User)

    disk_serials = ",".join(
        [
            os.environ.get("SystemSerialNumber", ""),
            os.environ.get("SystemUUID", ""),
            os.environ.get("DiskSerialNumber", ""),
        ]
    )
    computer_name = platform.node()
    running_user = getpass.getuser()
    hwid_input = disk_serials + computer_name + running_user
    hwid_bytes = hwid_input.encode("utf-8")
    hwid_hash = hashlib.sha256(hwid_bytes).hexdigest()

    return hwid_hash


# class Login(BaseModel):
#     licenseKey: str
#     HWID: str  #: sha256(Disk Serials (sep by comma) + Computer Name + Running User)
#     username: str  #: Discord Username


def authWhop() -> str:
    settings = load_settings()
    webhook = settings["webhook"]
    licenseKey = settings["key"]

    if not licenseKey or licenseKey == "KEY HERE":
        print_task("please set key...", RED)
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
        print(response)
    except requests.exceptions.JSONDecodeError:
        print_task("Backend login error.", RED)
        exit_program()

    if response.get("message"):
        if response["message"] == "Please reset your key to use on a new machine":
            print_task("HWID does not match current computer's HWID.", RED)
            exit_program()

        if response["message"] == "Not found":
            print_task("License key not found.", RED)
            exit_program()

        if response["message"] == "Please confirm your API token":
            print_task("Backend API Key Error", RED)
            exit_program()

        print_task("Unknown error...", RED)
        exit_program()

    if response.get("banned"):
        print_task("License key is banned.", RED)
        exit_program()

    if response.get("is_scammer"):
        print_task("License key is marked as a scammer.", RED)
        exit_program()

    if not response.get("valid"):
        print_task("License key is invalid.", RED)
        exit_program()

    if any(
        [response["key_status"] == "approved", response["key_status"] == "listed"]
    ) and any(
        [
            response["subscription_status"] == "completed",
            response["subscription_status"] == "active",
            response["subscription_status"] == "trialing",
        ]
    ):
        # return username
        return response["discord"]["discord_account_id"]

    print_task("License Unknown key is invalid.", RED)
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

    if not license_data:
        print_task("Invalid license key!", RED)
        exit_program()

    username = license_data.get("integrations").get("discord").get("username")

    if not webhook or webhook == "WEBHOOK HERE":
        print_task("please set webhook...", RED)
        exit_program()

    return username
