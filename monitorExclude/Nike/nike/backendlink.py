import time
from nike.nikeTypes import Thread
from nike.helper import getStoreData
from nike.webhook import webhook
import requests
import threading

headers = {
    "authority": "api.nike.com",
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


def getShoesStock(PID: str, id_store: str):
    firstRun = True

    while True:
        try:
            response = requests.get(
                f"https://api.nike.com/deliver/available_gtins/v3?filter=styleColor({PID})&filter=storeId({id_store})&filter=method(INSTORE)",
                headers=headers,
            )
            if firstRun:
                print(
                    "[{}] {} - {} Adding store to the list. (first run)".format(
                        PID, id_store, response.status_code
                    )
                )
                firstRun = False
                try:
                    data = response.json()["objects"]
                    print(data)
                    # data = ["gtin", "level"] # for testing purposes
                except:
                    data = {}

        except Exception as e:
            print(str(e))
            time.sleep(60)
            continue

        # if the response is 200, then the store has the shoes in stock
        if response.status_code == 200:
            data2 = response.json()["objects"]
            print(data2)

            if data != data2:
                print(
                    "[{}] {} - {} Stock changed!".format(
                        PID, id_store, response.status_code
                    )
                )
                data = data2
                getLevelStock(PID, id_store, data)
                # getLevelStock(PID, id_store, data2) # for testing purposes

            else:
                print(
                    "[{}] {} - {} Stock not changed.".format(
                        PID, id_store, response.status_code
                    )
                )
                print(
                    "[{}] {} - {} sleeping for 300 seconds...".format(
                        PID, id_store, response.status_code
                    )
                )
                time.sleep(300)
                continue
        elif response.status_code == 403:
            print(
                "[{}] {} - {} Rate limit exceeded.".format(
                    PID, id_store, response.status_code
                )
            )
            print(
                "[{}] {} - {} sleeping for 300 seconds...".format(
                    PID, id_store, response.status_code
                )
            )
            time.sleep(300)
            continue
        else:
            print(
                "[{}] {} - {} the store doesn't have the shoes in stock.".format(
                    PID, id_store, response.status_code
                )
            )
            print(
                "[{}] {} - {} sleeping for 300 seconds...".format(
                    PID, id_store, response.status_code
                )
            )
            time.sleep(300)
            continue


def getLevelStock(PID: str, id_store: str, dataResponse: list):
    with open("nikestore.csv", "r") as f:
        for line in f:
            if line.startswith("id"):
                continue
            if id_store in line:
                store_detail = line.split(",")
                break

    response = requests.get(
        f"https://api.nike.com/product_feed/threads/v2?filter=language(it)&filter=marketplace(IT)&filter=channelId(d9a5bc42-4b9c-4976-858a-f159cf99c647)&filter=productInfo.merchProduct.styleColor({PID})",
        headers=headers,
    )

    data = response.json()["objects"][0]

    stock_list = list()
    address_list = list()
    dict = {}

    address_list.append(store_detail[2])
    address_list.append(store_detail[3])
    address_list.append(store_detail[4])

    name_store = store_detail[1]

    try:
        for i in dataResponse:
            gtin = i.get("gtin")
            level = i.get("level")
            modificationDate = i.get("modificationDate")

            dict.update({gtin: level})

            for e in data["productInfo"][0]["skus"]:
                if gtin == e["gtin"]:
                    size = e["countrySpecifications"][0]["localizedSize"]
                    stock_list.append(size + " [" + dict[gtin] + "]")

                    break
    except:
        print("error")

    price = data["productInfo"][0]["merchPrice"]["currentPrice"]
    name = data["productInfo"][0]["productContent"]["title"]
    slug = data["productInfo"][0]["productContent"]["slug"]
    image = data["publishedContent"]["nodes"][0]["nodes"][0]["properties"][
        "squarishURL"
    ]

    webhook(
        PID,
        stock_list,
        modificationDate,
        name,
        image,
        price,
        address_list,
        name_store,
        slug,
    )


def BackendLinkFlow(PID: str, parentThread: Thread):
    print("[{}] Starting thread.".format(PID))
    # getStoreData()

    # loop over the id_store present in the csv file
    with open("nikestore.csv", "r") as f:
        for line in f:
            if line.startswith("id"):
                continue
            id_store = line.split(",")[0]

            # use threading to speed up the process
            t = threading.Thread(target=getShoesStock, args=(PID, id_store))
            t.start()

    # with open("romania.csv", "r") as f:
    #     for line in f:
    #         if line.startswith("id"):
    #             continue
    #         id_store = line.split(",")[0]

    #         # use threading to speed up the process
    #         t = threading.Thread(target=getShoesStock, args=(PID, id_store))
    #         t.start()


# fix nike link
