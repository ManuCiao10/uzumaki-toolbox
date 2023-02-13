PURPLE = "\033[95m"
CYAN = "\033[96m"
DARKCYAN = "\033[36m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
TAB = "\t"
WHITE = "\033[97m"
LOGO = "https://media.discordapp.net/attachments/1074041462460784701/1074456541480095845/logo.jpg?width=1410&height=846"

BANNER = """
      .---.        .-----------
     /     \  __  /    ------
    / /     \(  )/    -----
   //////   ' \/ '   ---            ┏───────────────────────────────┓
  //// / // :    : ---              │     WELCOME TO EAGLE TOOLS    │
 // /   /  /'    '--                │      https://eaglebot.eu      │
//           /..\                   │           v.0.0.23            │
       ====UU====UU====             └───────────────────────────────┘
            ./||\.
             ''''
"""


def load_settings():
    import json
    with open("eagleTools/settings.json", "r") as f:
        settings = json.load(f)
        f.close()

    return settings


def checking():
    settings = load_settings()
    webhook = settings["webhook"]
    # key = settings["key"]

    # if key == "KEY HERE":
    #     print_task("key not set", RED)
    #     print_task("please set key", RED)
    #     exit()

    print(PURPLE + "checking folders...")

    if webhook == "WEBHOOK HERE" or webhook == "":
        print_task("please set webhook...", RED)
        exit()

    # check if folder exists
    import os
    if not os.path.exists("eagleTools"):
        print(GREEN + "creating folder eagleTools...")
        os.makedirs("eagleTools")
        os.makedirs("eagleTools/tracker")
        os.makedirs("eagleTools/modules")
        os.makedirs("eagleTools/redirect")

        with open("eagleTools/settings.json", "w") as f:
            f.write(
                '{\n  "webhook": "WEBHOOK HERE",\n  "key": "KEY HERE"\n}')
            f.close()

        with open("eagleTools/tracker/tracker.csv", "w") as f:
            f.write(
                "company,tracking_number")
            f.close()

        with open("eagleTools/tracker/ups.csv", "w") as f:
            f.write(
                "tracking_number,packageStatus,simplifiedText,streetAddress1,city,country,zipCode,attentionName")
            f.close()

        with open("eagleTools/redirect/redirect.csv", "w") as f:
            f.write(
                "company,tracking_number,name,phone,address,city,state,zip,country")
            f.close()


def banner():
    print(RED + BANNER + RESET)

    print(WHITE + "Author: " +
          RED + "@MANUCIAO|YΞ\n" + RESET)

    print(TAB + "\x1b[1;37;41m" +
          " Select an option or type exit for exiting " + "\x1b[0m" + "\n")

    print(TAB + RED + " 01 " + WHITE + "Redirect" +
          TAB + "Redirect packages ups brt")

    print(TAB + RED + " 02 " + WHITE + "Csv" + TAB +
          TAB + "Csv filler Jig")

    print(TAB + RED + " 03 " + WHITE + "Tracker" +
          TAB + "Order Tracker ups dhl")

    print(TAB + RED + " 04 " + WHITE + "Scraper" +
          TAB + "Resell payout scraper goat stockx restock")

    print(TAB + RED + " 05 " + WHITE + "Modules" +
          TAB + "Modules Nike Adidas")

    print(TAB + RED + " 00 " + WHITE + "Exit" +
          TAB + "Exit from Eagle Tools")

    print("\n")

    option = input(TAB + RED + ">" + WHITE + " choose: " + RESET)
    return option


def time():
    import datetime
    now = datetime.datetime.now()
    return "[" + now.strftime("%H:%M:%S") + "] "


def eagle():
    return "[EagleTool 0.0.23] "


def print_task(msg, color):
    print(color + eagle() + time() + msg.upper() + RESET)


def send_webhook(company, tracking_number, status, simplifiedText, streetAddress1, city, country, zipCode, attentionName):
    # https://www.mathsisfun.com/hexadecimal-decimal-colors.html

    settings = load_settings()
    webhook = settings["webhook"]

    import requests
    import json
    url: str = ""

    if company == "ups":
        url = "https://www.ups.com/track?loc=en_IT&tracknum=" + \
            tracking_number + "&requester=ST/trackdetails"
    elif company == "dhl":
        url = "https://www.dhl.com/en/express/tracking.html?AWB=" + \
            tracking_number + "&brand=DHL"

    data = {
        "content": " ",
        "embeds": [
            {
                "title": "Tracking Number",
                "url": url,
                "color": 3093078,
                "footer": {
                    "text": "Powered by Eagle Tools",
                    "icon_url": LOGO
                },
                "thumbnail": {
                    "url": LOGO
                },
                "fields": [
                    {
                        "name": "Company",
                        "value": company,
                        "inline": True
                    },
                    {
                        "name": "Tracking Number",
                        "value": tracking_number,
                        "inline": True
                    },
                    {
                        "name": "Status",
                        "value": status,
                        "inline": True
                    },
                    {
                        "name": "Text",
                        "value": simplifiedText,
                        "inline": True
                    },
                    {
                        "name": "Street Address",
                        "value": streetAddress1,
                        "inline": True
                    },
                    {
                        "name": "City",
                        "value": city,
                        "inline": True
                    },
                    {
                        "name": "Country",
                        "value": country,
                        "inline": True
                    },
                    {
                        "name": "Zip Code",
                        "value": zipCode,
                        "inline": True
                    },
                    {
                        "name": "Name",
                        "value": attentionName,
                        "inline": True
                    }
                ]
            }
        ]
    }
    result = requests.post(
        webhook, data=json.dumps(data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)


def ups(tracking_number):
    import requests
    session = requests.Session()

    headers = {
        'authority': 'www.ups.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    params = {
        'loc': 'en_IT',
        'tracknum': tracking_number,
        'requester': 'ST/trackdetails',
    }

    try:
        response = session.get('https://www.ups.com/track',
                               params=params, headers=headers)

        if response.status_code == 200:
            print_task("[ups %s] successful got session..." %
                       tracking_number, YELLOW)

        token_ = response.cookies['X-XSRF-TOKEN-ST']

        refer = 'https://www.ups.com/track?loc=en_IT&tracknum=' + tracking_number + \
            '&requester=ST%2Ftrackdetails%2Ftrackdetails%2Ftrackdetails%2Ftrackdetails'

        headers = {
            'authority': 'www.ups.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://www.ups.com',
            'pragma': 'no-cache',
            'referer': refer,
            'sec-ch-ua': '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'x-xsrf-token': token_,
        }

        params = {
            'loc': 'en_IT',
        }

        json_data = {
            'Locale': 'en_IT',
            'TrackingNumber': [
                tracking_number,
            ],
            'Requester': 'st/trackdetails/trackdetails/trackdetails',
            'returnToValue': '',
        }

        response = session.post(
            'https://www.ups.com/track/api/Track/GetStatus',
            params=params,
            headers=headers,
            json=json_data,
        )
        if response.json()["statusCode"] != "200":
            print_task("[ups %s] error: %s" % (tracking_number), RED)
            return

        try:
            packageStatus = response.json()["trackDetails"][0]["packageStatus"]
        except:
            packageStatus = "Not Found"
        try:
            simplifiedText = response.json(
            )["trackDetails"][0]["simplifiedText"]
        except:
            simplifiedText = "Not Found"
        try:
            streetAddress1 = response.json(
            )["trackDetails"][0]["upsAccessPoint"]["location"]["streetAddress1"]
        except:
            streetAddress1 = "Not Found"
        try:
            city = response.json()[
                "trackDetails"][0]["upsAccessPoint"]["location"]["city"]
        except:
            city = "Not Found"
        try:
            country = response.json(
            )["trackDetails"][0]["upsAccessPoint"]["location"]["country"]
        except:
            country = "Not Found"
        try:
            zipCode = response.json(
            )["trackDetails"][0]["upsAccessPoint"]["location"]["zipCode"]
        except:
            zipCode = "Not Found"
        try:
            attentionName = response.json(
            )["trackDetails"][0]["upsAccessPoint"]["location"]["attentionName"]
        except:
            attentionName = "Not Found"

        print_task("[ups %s] successful got data..." %
                   tracking_number, GREEN)

        with open("eagleTools/tracker/ups.csv", "a") as f:
            import csv
            writer = csv.writer(f)
            writer.writerow([tracking_number, packageStatus, simplifiedText,
                            streetAddress1, city, country, zipCode, attentionName])

        # send discord webhook
        send_webhook("ups", tracking_number, packageStatus, simplifiedText,
                     streetAddress1, city, country, zipCode, attentionName)

    except Exception as e:
        print_task("[ups %s] error: %s" % (tracking_number, e), RED)
        return


def companyHandler(company, tracking_number):
    if company == "ups":
        ups(tracking_number)
    # elif company == "brt":
    #     brt(tracking_number)
    else:
        print_task("invalid company", RED)


def tracker():
    import csv
    import threading
    print_task("starting tracker.csv...", PURPLE)
    with open("eagleTools/tracker/tracker.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            company = row[0].lower().strip()
            tracking_number = row[1].strip()

            threading.Thread(target=companyHandler, args=(
                company, tracking_number)).start()


def scraper():
    # print new terminal
    import os
    os.system('clear')
    print(RED + BANNER + RESET)

    print(WHITE + "Author: " +
          RED + "@MANUCIAO|YΞ\n" + RESET)
    print(TAB + "\x1b[1;37;41m" +
          " Scraper usage: " + "\x1b[0m" + "\n")
    print(TAB + RED + " 01 " + WHITE + "Goat" +
          TAB + "!goat < sku > or < key words >" + RESET)

    print(TAB + RED + " 02 " + WHITE + "Restock" +
          TAB + "!restock < sku > or < key words >" + RESET)

    print("\n")
    option = input(TAB + RED + ">" + WHITE +
                   " your option (ex. !goat DZ5485-410): " + RESET)
    print(option)


def handler_option(option):
    if option == "03":
        tracker()
    elif option == "04":
        scraper()
    elif option == "00":
        exit()
    else:
        print(RED + "Invalid option..." + RESET)
        exit()


if __name__ == "__main__":
    checking()

    option = banner()
    handler_option(option)
