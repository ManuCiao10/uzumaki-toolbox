from handler.utils import *
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

import requests


class Size:
    def __init__(self, stock: int, size: str):
        self.stock: int = stock
        self.size: str = size


class Restock:
    def __init__(self, sku):
        self.sku = sku

        self.session = self.login()
        return self.getProducts()

    def login(self):
        print_task(f"[restock {self.sku}] getting session", PURPLE)

        restocks_headers = {
            "Host": "restocks.net",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        }

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

        self.session.headers.update(restocks_headers)

        response = self.session.get("https://restocks.net/it/login")

        soup = BeautifulSoup(response.text, "html.parser")

        csrf_token = soup.find("meta", {"name": "csrf-token"})["content"]

        data = {
            "_token": csrf_token,
            "email": "EMAIL",
            "password": "PASSWORD",
        }

        response = self.session.post("https://restocks.net/it/login", data=data)

        response = self.session.get("https://restocks.net/it/account/profile")

        soup = BeautifulSoup(response.text, "html.parser")

        try:
            _ = soup.find("div", {"class": "col-lg-3 col-md-4"}).findAll("span")[1].text
            print_task(f"[restock {self.sku}] got session", WHITE)
        except:
            print_task(f"[restock {self.sku}] error getting session", RED)
            time.sleep(3)
            return

        return self.session

    def getStock(self, id, id_size):
        try:
            response = self.session.get(
                f"https://restocks.net/en/product/get-lowest-price/{id}/{id_size}",
            )
            if response.status_code != 200:
                print_task(f"[restock {self.sku}] error {response.status_code}", RED)
                time.sleep(3)
                return

            return str(response.text)

        except Exception as e:
            print_task(f"[restock {self.sku}] error {e}", RED)
            time.sleep(3)
            return

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

        sizes: list[Size] = []

        for size in data:
            self.id_size = size["id"]
            size_number = size["name"]
            stock = self.getStock(id, self.id_size)

            sizes.append(
                Size(
                    stock=stock,
                    size=size_number,
                )
            )

        self.webhook(
            sizes,
        )

    def webhook(self, productSizes: list[Size]):
        settings = load_settings()

        webhook = DiscordWebhook(
            url=settings["webhook"],
            rate_limit_retry=True,
            username="Uzumaki™",
            avatar_url=LOGO,
        )

        embed = DiscordEmbed(
            title=self.name,
            description=f"> **Restock SKU: {self.sku}**",
            color=12298642,
            url=self.url,
        )

        embed.set_thumbnail(url=self.image)

        value_size = []
        value_stock = []

        for size in productSizes:
            value_size.append(f"{size.size}\n")
            value_stock.append(f"{size.stock} €\n")

        embed.add_embed_field(name="Size", value="```" + "".join(value_size) + "```")
        embed.add_embed_field(name="Payout", value="```" + "".join(value_stock) + "```")

        embed.set_footer(text="Powered by Uzumaki Tools", icon_url=LOGO)

        webhook.add_embed(embed)

        response = webhook.execute()
        if "<Response [405]>" in str(response):
            print_task(f"[restock {self.sku}] error sending webhook", RED)
            time.sleep(2)
        else:
            print_task(f"[restock {self.sku}] webhook sent", GREEN)
            time.sleep(2)
