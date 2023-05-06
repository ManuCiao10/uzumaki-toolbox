from handler.utils import *
import requests


def ups(username):
    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    print("starting ups redirect...\n")

    session = requests.Session()

    tracknum = "1Z175Y406893005280"

    referer = f"https://www.ups.com/track?loc=en_IT&tracknum={tracknum}&requester=ST/trackdetails"

    headers = {
        "authority": "www.ups.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "referer": referer,
        "sec-ch-ua": '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    }

    params = {
        "clientId": "TRK",
        "loc": "en_IT",
        "trackingNumber": tracknum,
        "infoNoticeNum": "",
        "returnToURL": f"/track?loc=en_IT&tracknum={tracknum}&src=&requester=",
    }

    response = session.get(
        "https://www.ups.com/deliverychange",
        params=params,
        headers=headers,
    )

    referer = f"https://www.ups.com/deliverychange/?clientId=TRK&loc=en_IT&trackingNumber={tracknum}&infoNoticeNum=&returnToURL=%2Ftrack%3Floc%3Den_IT%26tracknum%3D{tracknum}%26src%3D%26requester%3D"
    headers = {
        "authority": "www.ups.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/json",
        "origin": "https://www.ups.com",
        "referer": referer,
        "sec-ch-ua": '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    }

    json_data = {
        "trackingNumber": tracknum,
        "infoNoticeNumber": "",
        "loc": "en_IT",
        "isADBD": False,
        "isAC": False,
        "userID": "ManuCiao10",
        "param1": "",
        "inqType": None,
        "clientUrl": "",
        "isShipper": False,
        "dcrReturn": "0",
    }

    response = session.post(
        "https://www.ups.com/deliverychange/api/Entry/GetEntryInformation",
        headers=headers,
        json=json_data,
    )

    print(response.text)
