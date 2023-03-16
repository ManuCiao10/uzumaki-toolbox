from handler.utils import *

import requests


class Restock:
    def __init__(self, sku):
        self.sku = sku
        self.session = requests.Session()

        self.session.headers = {
            "authority": "restocks.net",
            "accept": "*/*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://restocks.net/en/account/sell",
            "sec-ch-ua": '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
        return self.getProducts()

    def getProducts(self):
        print_task(f"[restock {self.sku}] getting products", PURPLE)

        params = {
            "q": self.sku,
            "page": "1",
        }

        try:
            response = self.session.get(
                "https://restocks.net/en/shop/search",
                params=params,
            )
            data = response.json()
            
            print_task(f"[restock {self.sku}] got products", WHITE)

        except Exception as e:
            print_task(f"[restock {self.sku}] error {e}", RED)
            time.sleep(3)
            return

        if response.status_code != 200:
            print_task(f"[restock {self.sku}] error {response.status_code}", RED)
            time.sleep(3)
            return

        for id in data["data"]:
            self.name = id["name"]
            self.url = id["slug"]
            self.image = id["image"]
            self.getSizes(id["id"])

    def getSizes(self, id):
        print_task(f"[restock {self.sku}] getting sizes", PURPLE)

        try:
            response = self.session.get(
                f"https://restocks.net/en/product/get-sizes/{id}"
            )
            data = response.json()
            print_task(f"[restock {self.sku}] got sizes", WHITE)

        except Exception as e:
            print_task(f"[restock {self.sku}] error {e}", RED)
            time.sleep(3)
            return

        if response.status_code != 200:
            print_task(f"[restock {self.sku}] error {response.status_code}", RED)
            time.sleep(3)
            return

        for size in data:
            self.id_size = size["id"]
            self.size_number = size["name"]
            self.getStock(id, self.id_size)

    def getStock(self, id, id_size):
        print_task(f"[restock {self.sku}] getting stock", PURPLE)

        try:
            response = self.session.get(
                f"https://restocks.net/en/product/get-lower-price/{id}/{id_size}"
            )
            data = response.json()
            print_task(f"[restock {self.sku}] got stock", WHITE)

        except Exception as e:
            print_task(f"[restock {self.sku}] error {e}", RED)
            time.sleep(3)
            return

        if response.status_code != 200:
            print_task(f"[restock {self.sku}] error {response.status_code}", RED)
            time.sleep(3)
            return

        # if data["stock"] > 0:
        #     self.stock = data["stock"]
        #     self.getPrice(id, id_size)
