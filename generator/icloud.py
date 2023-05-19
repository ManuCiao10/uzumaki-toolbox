from handler.utils import *
from internal.security import processRunning
import requests


def icloud(username):
    processRunning()
    setTitleMode("Generator - Icloud")

    # while True:
    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    GeneratorIcloud()


def getSession(self):
    print("getting session")

    self.session = requests.Session()
    self.session.headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://appleid.apple.com/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }
    self.cookies = {
        "geo": "IT",
    }

    try:
        resp = self.session.get(
            "https://appleid.apple.com/account",
        )
        if resp.status_code != 200:
            # retry if failed
            print("error getting session")
            return getSession(self)

        print("Successfull got session")
    except Exception:
        print("error doing request")
        return getSession(self)

    return self.session


def getPayload(self):
    json_data = {
        "account": {
            "name": "pierino@gmail.com",
            "password": "IAododood",
            "person": {
                "name": {
                    "firstName": "peirim",
                    "lastName": "giacomo",
                },
                "birthday": "2000-11-02",
                "primaryAddress": {
                    "country": "ITA",
                },
            },
            "preferences": {
                "preferredLanguage": "en_GB",
                "marketingPreferences": {
                    "appleNews": False,
                    "appleUpdates": False,
                    "iTunesUpdates": False,
                },
            },
            "verificationInfo": {
                "id": "",
                "answer": "",
            },
        },
        "captcha": {
            "id": 1671865686,
            "token": "6d1a5277561a7646ed678ef4f719ff8ff3a88685d56d7f87baed0686bf983c3e03102d855d1f2b48c834f5725e4166abc64409d98c1ad2ef5355868fb7080aa858eb0d2bf3f7eebe76a4a5a6671de001bfe01e952534c9ce507405e9d399392a0202f7c06423edd7232d83714a87957821ac97ec0067f43f936eb7c05645c9306043a5706bc688b9dea64ceeeeab4e533eaa44f6514f45062a63890d77e0d9e6df2945f8251cf12420f7b778e301ea7a9ce51dbeb269ea5822114aacd5d31f72f3a9ef6d10b18c7b02bacd5b00af2f860afce4ebc711f147ada310c3018d153579f876b497338a8fb2b0557c8e147792350d48bc4b092189f256bc1eeabc1ca4df2ae71de816896245f2b1adedc5bb82a4649b9515fa63f4474e2992c8799029a4742e0543ff0f566141237e562827b7RRAR",
            "answer": "",
        },
        "phoneNumberVerification": {
            "phoneNumber": {
                "id": 1,
                "number": "3398765432",
                "countryCode": "IT",
                "countryDialCode": "39",
                "nonFTEU": False,
            },
            "mode": "sms",
        },
        "privacyPolicyChecked": False,
    }

    response = requests.post(
        "https://appleid.apple.com/account/validate", headers=headers, json=json_data
    )


class GeneratorIcloud:
    def __init__(self):
        # call the session
        getSession(self)
        getPayload(self)
