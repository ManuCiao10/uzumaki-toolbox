from handler.utils import *
from handler.redirect import redirect
from handler.geocode import geocode
from handler.auth import auth, update
from handler.jigger import jigger
from handler.scraperOrder import scraperOrder
from handler.presence import reachPresence
from handler.restock import restockPayout
from handler.unsubscriber import unsubscriber
from handler.gls import glsRedirect
from handler.dhlRedirect import dhlRedirect

from tracker.tracker import tracker
from internal.security import processRunning
from internal.pickup import pickup

from proxy.proxy import proxy
from payout.payout import payout
from monitor.wethenew import wethenew
from multiprocessing import freeze_support
from generator.outlook import Inizialize
from generator.yahoo import yahoo

import colorama

OPTIONS = {
    "01": redirect,
    "02": tracker,
    "03": geocode,
    "04": jigger,
    "05": scraperOrder,
    "06": restockPayout,
    "07": unsubscriber,
    "08": glsRedirect,
    "09": pickup,
    "10": payout,
    "11": wethenew,
    "12": proxy,
    "13": dhlRedirect,
    "14": Inizialize,
    "15": yahoo,
    # "16": gmail,
    "00": bye,
}


class LoginWebDE:
    def __init___(self, email, password):
        self.session = self.__get_session___()
        self.email = email
        self.password = password

        return self.__login___()

    def __get_session___(self):
        import requests

        print("getting session...")

        session = requests.Session()
        session.headers = {
            "authority": "web.de",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        }

        _ = session.get("https://web.de/")

        return session

    def __login___(self):
        print("starting log in...")

        self.session.headers = {
            "Host": "login.web.de",
            "cache-control": "max-age=0",
            "sec-ch-ua": '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "upgrade-insecure-requests": "1",
            "origin": "https://web.de",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "sec-gpc": "1",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "referer": "https://web.de/",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        }

        data = {
            "successURL": "https://bap.navigator.web.de/login",
            "statistics": "kR8BWaubR5/vA1KhqEY3LOBuNIy/0UiyKfW8gXUbkE9ajaE5dqAorbuXCwUU2zxykOEv9JD/9AWh+zAJ//a2WMHWIInMjKb8hXoy+K0iQyeWYypnCpnWoUOpQvJbItZGvle7mgDbprFKgW+XoPP4IpcUuEqAWHDTB1pM3aH/wNA=",
            "service": "freemail",
            "server": "https://freemail.web.de",
            "loginErrorURL": "https://bap.navigator.web.de/loginerror",
            "loginFailedURL": "https://web.de/logoutlounge/?status=login-failed",
            "ibaInfo": "os=5;browser=11;deviceclass=b;abd=false;weather_temp=12;weather_condition=3",
            "uinguserid": "",
            "tpidHash": "",
            "salt": "",
            "username": self.email,
            "password": self.password,
        }

        response = self.session.post("https://login.web.de/login", data=data)

        if (
            "aptchaPanel:captchaImagePanel:captchaInput:topWrapper:inputWrapper:input"
            in response.text
        ):
            print("captcha hitted")
            time.sleep(5)

        print(response.text)

def nike():
    import requests

    headers = {
    'authority': 'api.nike.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    # 'cookie': 'AnalysisUserId=184.25.126.93.597881677108267502; geoloc=cc=IT,rc=,tp=vhigh,tz=GMT+1,la=45.47,lo=9.20; AMCVS_F0935E09512D2C270A490D4D%40AdobeOrg=1; anonymousId=E3D31238740BB8C170DF65ED7DFDAF4D; optimizelyEndUserId=oeu1679927799517r0.7307478073949414; RES_TRACKINGID=85974982059872997; ResonanceSegment=1; ni_s=1; s_ecid=MCMID%7C87900974342592021727641172016718436529; AMCV_F0935E09512D2C270A490D4D%40AdobeOrg=1994364360%7CMCMID%7C87900974342592021727641172016718436529%7CMCAID%7CNONE%7CMCOPTOUT-1680783753s%7CNONE%7CvVersion%7C3.4.0; audience_segmentation_performed=true; AKA_A2=A; bm_mi=9B8AB3CE432D0225F1888F0FD7386558~YAAQvjRoaJILaBmHAQAAc46SVhPiXs4FPeQRg/E/CUsSN7yfRjdm6DMVqt46OjuJn/tQvEO6XAMm6qcacAw+67CcodQWtkvrFo6f0rjrFwuArMFaqqXY4YflBdpbI8r8o31v7z+JyBSqiGVto6/UQbL2y8evyEP7xIjHki/dxaWy6rjNzGUv8zOvJaubZzeo5Neyh7LWAQfLMhx2yDVbwLP7WkR9lDuPShvOhhZxXxC4KQhiK42g6/6oHZZ+pdYALhTRSyv8RSZ3VEOfXRPwmG//XZjuOpEMq6y+wAJs1vM5ImaCV9gj7aIU/R8IntfSs45rRcpseGA=~1; ak_bmsc=466B45C3CD78674D288CF028097C9DB5~000000000000000000000000000000~YAAQYn4ZuMNPzFKHAQAA3Y+SVhN6t8Wq2eAvCCr/h9Tl+tIaf6Mz/i2n0JLEoMKCS/VRvEIYGmLge0HcCKmH/udpA3fXrlmHgZDnUuZwI7JHT6gfbnn/uUSFfRZcDHEHhzNU08SkkuF4+SLDzshpBxRO7RjDSHyVg+0n0Fr70DP9R4fdl4xa41i764Zl8JHRjfrcEbT/FbaAgaQY0SvLvXlQHOJy3js8Fq3tZgI1pfO/4yT9+WFF1RCbucbWHPrXM/YhVcnQiwavSbo6vDBVCk/0/BGGCmC3ohi4P+qxWPCuXo5IhzQzjMPswpfh+SvvAF4oZDIGCVb1FZk6TgmLLxM0eW9RZXpS7T8G0MiVs/3MI+9B+RhtBikjZGN1LXMKj3g0GKvmMt696B/zvGnNC9XTkVmZZKe6b/Bcla30uqPyF5fU1oSi643CWM561vekB0FCWp4eGGQVMdvMgiF0PyJLY3BgZmoF1nUoDkIOxd43RLNIMtww3OY3WhZf3G7C/XUJh8BzAUUEYDU=; guidS=9fdb9b46-4047-46fd-e3b7-10ea0f6ac57f; guidU=f06c29dd-4819-4a29-8cbc-6b0dcf40d689; NIKE_COMMERCE_COUNTRY=US; NIKE_COMMERCE_LANG_LOCALE=en_US; nike_locale=us/en_us; CONSUMERCHOICE=us/en_us; CONSUMERCHOICE_SESSION=t; ppd=store%20locator|nikecom>store%20locator>store>Brescia%20Nike%20Factory%20Store; ak_bmsc_nke-2.3-ssn=0J0ApVmKUoNov7IbdPpZbj5ZD7N9YNxhdkJkPEwdpcWKRSGAdajrJovNedspAhp72vJafKkuZbmNBBAojMj0tQ0hxx9f1QG77QhvnJAfg377l8W3WSq28Epkn3ytZ83SByUEImKVYnGqtrJhge136hajj; ak_bmsc_nke-2.3=0J0ApVmKUoNov7IbdPpZbj5ZD7N9YNxhdkJkPEwdpcWKRSGAdajrJovNedspAhp72vJafKkuZbmNBBAojMj0tQ0hxx9f1QG77QhvnJAfg377l8W3WSq28Epkn3ytZ83SByUEImKVYnGqtrJhge136hajj; bm_sv=DEEDDBF9C6FDABE8AF4E55879EE290C4~YAAQRn4ZuJdM1xWHAQAAlEy2VhMoi5KmcPYVnGk80S2fyYNpRcrJltjy/xWoIUuFsBL8iJwjsGBSsfoOqvmNBXy6DVIuPpmbLFKWrZkjV612kdZg+ZsERN+sDaJtMHB7hTQRNYkEjpTs8QYFAtALvZzw0KiStoE16VfMeLuSA7pgW2PGkB/zUV9VCLeR5Romo2nRzTvSZznA1aObWU/vbytRaIl/cxJFqMPWNer84BnbTLuMxaCl8Ur/OogLNbw=~1; _abck=095E76D93E925F0CC4E7B1C8E1F5306B~-1~YAAQRn4ZuF6C1xWHAQAACnm4VglW+HkGNQZU/jqJ67HCMb16vMaBDBCciaHONXWEKfmmRCKiNKgbnrJgY5/W7rNhhCNqCl+5pbtc/1v05x7yjmKURtLcrmDEqy/RjM0FnW6NHDGA7SKbxIbcges8HBYiyExTDcB/UjWuLF2xZwflirIvLueWV+FAfFcAE+eyy2J9l6aWV0Prt8zFcpGY4B4qY/ZDV/DWOZ3ABDunrL+l2V221et5Fw9yvvaHgInidOKnY7m6hLJ+PhmxQbbojoXwRTu6hWKteAzDlgO3oWwh7hevJc0VYEq2v4W2thh2m5u/ZoKIahMbMGA1q+1bHxkuOgm4eq4rWA6mZi7otZxsjY15viZT3XqKVjc6N7Eyx5qaG+TtiXcWp7NAS3Z8H1p2KWDcz4KiqG0nSOfO8CAw1VFSVqIJKo85/ZEoY9a8hcuBJzz9NjRxnAhKg26sV3+e1f5hO1A/GIm0HTHt4WTl183eMsm1H0g/370DMGraCq8A4yP293MKIaiLhIYKD5BvnGmaEw==~-1~-1~-1; bm_sz=E1B3B2CBA454404FEE460FEA358BC985~YAAQRn4ZuF+C1xWHAQAACnm4VhMfG9vFOXUIg3i1H//I2pgnYsryHIKrbimYi4RfwLkPHamPs5nszsbT7wrfCXZonttbg9Vgo921r5pKCQb39592jVW0Zz90879NIw82rwXZEGoz9C/z05AWHNBPlVaxefg7CnKsPAHUmE1ZGog9E/KKSSREGihIK3dn95shl7z8uTrrO0HktJ7LurDpcp4u07lvLkzKjk5H5pVDKoK91gkENTg9mewXhPeqOcB/wP/pvaR6cQyYI3pFXUd0c06u7h8+6bC4UauhDKF5L2vo4vEhinnvOJlqvK8PYI8uIX0CM3yw8TkpDYsL+mCtPt/8kvKtLJXYzMyEhGGZWSAtXSFKfaGg5/XNdwu/xBimkV/u5DkxjIoFYpOv1N2Bek9SxQkDvlzrgRsGwk7cTwIqvf3NWQWSz40UQxB00xtSKQHgxYflPutu7HUOzQbIDyjXTresNzKMP1wlqYAUmg4/7mCwtC9IRxEFPECcptLmfNsjWKa7Vval3Jwa8BFE8A==~3228483~4534342',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

    params = {
    'language': 'en-IT',
    'search': '(((brand==NIKE and facilityType==NIKE_OWNED_STORE or facilityType==FRANCHISEE_PARTNER_STORE or facilityType==MONO_BRAND_NON_FRANCHISEE_PARTNER_STORE and (region==ITALY)) and (businessConcept!=EMPLOYEE_STORE and businessConcept!=BRAND_POP_UP)) and (coordinates=geoProximity={"maxDistance": 5000, "measurementUnits": "mi","latitude": 41.87, "longitude": 12.56}))',
}

    response = requests.get('https://api.nike.com/store/store_locations/v1', params=params, headers=headers)

    print(response.text)

    #save to file
    with open('nike.json', 'w') as f:
        json.dump(response.json(), f)

    #get the store id
    store = response.json()['objects']


    for i in store:
        print(i['id'])
    time.sleep(50)

def main():
    colorama.init(wrap=True)

    nike()
    # update()
    # checking()
    # processRunning()
    # username = auth()
    # reachPresence(username)
    # setTitle()
    username = "dev"

    while True:
        option = banner(username)
        try:
            OPTIONS[option](username)
            break
        except KeyError:
            print_task("invalid option", RED)
            time.sleep(0.5)


if __name__ == "__main__":
    freeze_support()
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        print_task("Key Interrupt", YELLOW)
        exit_program()


# fix Monitor Wethenew
# imporve monitor design
# macOS Version to get more client
# gmail - yahoo - icloud generator email
# ticket master Monitor
# nike instore monitor
