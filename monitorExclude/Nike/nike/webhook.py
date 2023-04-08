import requests
from datetime import datetime

LOGO_UZUMAKI = "https://media.discordapp.net/attachments/819084339992068110/1083492784146743416/Screenshot_2023-03-09_at_21.53.23.png"


def webhook(
    PID: str,
    stock_list: list,
    modificationDate: str,
    name: str,
    image: str,
    price: str,
    address_list: list,
    name_store: str,
    slug: str,
):

    array_address = []
    array_sizes = []
    embee = []

    title_url = f"https://www.nike.com/it/t/{slug}/{PID}"
    # webhook_test = "WEBHOOK_HERE"
    webhook_uzumaki = "https://discord.com/api/webhooks/1094250094733312104/F1jCulUqsx4CbIrcWkyJTa4VG9L9nO6XdcWDmde_lFVM-pA6UJIhUOdnVHc4yJDfQdRs"
    flag = ":flag_it:"
    name_store = f"{name_store} {flag}"

    date_time = datetime.strptime(modificationDate[:-1], "%Y-%m-%dT%H:%M:%S.%f")
    time_str = date_time.strftime("%I:%M:%S %p")

    for i in address_list:
        if i != "":
            i = str(i)
            i = i.strip()
            if len(i) < 6:
                array_address.append(i + " ")
            else:
                array_address.append(i + "\n")

    array_address = "".join(array_address)

    embee.append({"name": "Store", "value": name_store, "inline": False})
    embee.append(
        {"name": "Address", "value": "```" + array_address + "```", "inline": False}
    )
    # len_stock_list = len(stock_list)
    # number_colunm = len_stock_list

    # stcok_list = ['35.5 [OOS]', '36.5 [OOS]', '38 [OOS]', '36 [LOW]', '37.5 [LOW]']
    for i in stock_list:
        array_sizes.append(i + "\n")

    array_sizes = "".join(array_sizes)

    embee.append({"name": "Sizes", "value": array_sizes, "inline": False})

    embee.append({"name": "SKU", "value": PID, "inline": False})
    embee.append({"name": "Price", "value": str(price) + "€", "inline": False})

    data = {
        "username": "Nike Instore IT",
        "avatar_url": LOGO_UZUMAKI,
        "embeds": [
            {
                "title": name,
                "url": title_url,
                "color": 12298642,
                "thumbnail": {"url": image},
                "fields": embee,
                "footer": {
                    "text": "Nike Instore Uzumaki | " + time_str,
                    "icon_url": LOGO_UZUMAKI,
                },
            }
        ],
    }

    response = requests.post(webhook_uzumaki, json=data)
    try:
        response.raise_for_status()
        print("[{}] - {} success".format(PID, response.status_code))
    except requests.exceptions.HTTPError as err:
        print(err)
    except:
        print("An unexpected error occurred")
