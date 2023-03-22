from handler.utils import *
import os
from internal.security import processRunning
import requests
from requests_html import HTMLSession
import re


def proxy(username):
    proxy_list = []
    proxy_count = 0
    bad_proxy_count = 0
    good_proxy_count = 0
    checked_count = 0

    processRunning()
    setTitleMode("proxy - scraper")

    os.system("cls" if os.name == "nt" else "clear")

    print(f"{RED}{BANNER}{RESET}")
    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    url_base = (
        "https://raw.githubusercontent.com/hendrikbgr/Proxy-Scraper/main/urls.txt"
    )

    try:
        resp = requests.get(url_base, allow_redirects=True)
    except:
        print_task("error getting proxies", RED)
        exit_program()

    # count response.text lines
    urls = resp.text.splitlines()

    for url in urls:
        index = urls.index(url)
        print_task(f"crawling proxies [{index}]", PURPLE)

        session = HTMLSession()

        try:
            r = session.get(url)
            links = r.html.absolute_links
            links = str(links)
            links = links.replace("{", "")
            links = links.replace("}", "")
            links = links.split(",")
            for link in links:
                # print('Link Scraped: ', link)
                print_task
                print()

            # Get Proxies
            page = r.html.find("html", first=True)
            proxies_found = re.findall("\d+\.\d+\.\d+\.\d+\:\d+", page.html)
            print("Proxies found: ", proxies_found)

            proxy_list = proxy_list + proxies_found
            for proxy in proxy_list:
                proxy_count += 1

            session.close()

            for link in links:
                index_link = urls.index(link)
                print_task(f"crawling proxies [{index_link}]", PURPLE)
                # print('Crawling Proxies from: ', link)

                try:
                    r = session.get(link)
                    page = r.html.find("html", first=True)
                    proxies_found = re.findall("\d+\.\d+\.\d+\.\d+\:\d+", page.html)
                    print("Proxies found: ", proxies_found)
                    proxy_list = proxy_list + proxies_found
                    for proxy in proxy_list:
                        proxy_count += 1
                        print("Proxy found: ", proxy)
                    session.close()
                except:
                    pass
        except:
            pass
