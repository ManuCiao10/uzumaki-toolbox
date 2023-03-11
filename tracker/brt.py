from handler.utils import print_task, YELLOW, RED, GREEN
from handler.webhook import send_webhook_brt


def brt(tracking_number):
    import requests

    session = requests.Session()

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://services.brt.it/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    try:
        response = session.get(
            "https://vas.brt.it/vas/sped_numspe_par.htm", headers=headers
        )

        if response.status_code == 200:
            print_task("[brt %s] successful got session..." % tracking_number, YELLOW)

            it = "Dettaglio della spedizione"
            en = "Shipment details"
            fr = "Détail de l'envoi"

            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Origin": "https://vas.brt.it",
                "Pragma": "no-cache",
                "Referer": "https://vas.brt.it/vas/sped_numspe_par.htm",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Sec-GPC": "1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
            }
            BIGipServerAS777_Pool = response.cookies.get_dict()["BIGipServerAS777-Pool"]
            TS01ef7a66 = response.cookies.get_dict()["TS01ef7a66"]

            cookies = {
                "BIGipServerAS777-Pool": BIGipServerAS777_Pool,
                "iduser": "",
                "lstaut": "0000000000100",
                "usrname": "",
                "ksu": "",
                "lang": "en",
                "TS01ef7a66": TS01ef7a66,
            }

            data = {
                "brtCode": tracking_number,
                "RicercaBrtCode": "Ricerca",
                "referer": "sped_numspe_par.htm",
                "nSpediz": "458032091937",
            }
            response = session.post(
                "https://vas.brt.it/vas/sped_det_show.htm",
                cookies=cookies,
                headers=headers,
                data=data,
            )

            if it in response.text or en in response.text or fr in response.text:
                class_data = "table_stato_dati"
                from bs4 import BeautifulSoup

                soup = BeautifulSoup(response.text, "html.parser")
                table = soup.find("table", {"class": class_data})
                # get <tr> with class="table_stato_dati"
                rows = table.find_all("tr")
                rows = rows[1:]

                cols = rows[0].find_all("td")
                cols = [ele.text.strip() for ele in cols]

                print_task("[brt %s] successful got data..." % tracking_number, GREEN)

                send_webhook_brt(
                    "brt", tracking_number, cols[0], cols[1], cols[2], cols[3]
                )

                with open("Uzumaki/tracker/brt_result.csv", "a") as f:
                    import csv

                    writer = csv.writer(f)
                    writer.writerow(
                        [tracking_number, cols[0], cols[1], cols[2], cols[3]]
                    )

            else:
                print_task(
                    "[brt %s] error: %s"
                    % (tracking_number, "invalid tracking number..."),
                    RED,
                )
                return

        else:
            print_task(
                "[brt %s] error: %s" % (tracking_number, response.status_code), RED
            )
            return
    except Exception as e:
        print_task("[brt %s] error: %s" % (tracking_number, e), RED)
