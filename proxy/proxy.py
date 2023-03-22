from handler.utils import *
import os
from internal.security import processRunning
import requests
from requests_html import HTMLSession
import re
import threading
import urllib.request
import socket
import urllib.error

socket.setdefaulttimeout(180)


def is_bad_proxy(pip):
    try:
        proxy_handler = urllib.request.ProxyHandler({"http": pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [("User-agent", "Mozilla/5.0")]
        urllib.request.install_opener(opener)
        sock = urllib.request.urlopen(
            "http://www.google.com"
        )  # change the url address here

    except urllib.error.HTTPError as e:
        # print_task("error code: %s" % (e.code), RED)
        return e.code
    except Exception as detail:
        # print_task("error: %s" % (detail), RED)
        return 1
    return 0


def checker_proxies(proxies):
    path = "Uzumaki/proxy"

    if is_bad_proxy(proxies):
        print_task("not working proxy %s" % (proxies), RED)
    else:
        print_task("working Proxy %s" % (proxies), GREEN)
        with open(path + "/proxies.txt", "a") as f:
            f.write(proxies + "\n")


def crwaling_proxies(url, urls):
    proxy_list = []
    proxy_count = 0

    index = urls.index(url)
    print_task(f"[{index}] crawling proxies", PURPLE)

    session = HTMLSession()

    try:
        r = session.get(url)
        links = r.html.absolute_links
        links = str(links)
        links = links.replace("{", "")
        links = links.replace("}", "")
        links = links.split(",")

        # Get Proxies
        page = r.html.find("html", first=True)
        proxies_found = re.findall("\d+\.\d+\.\d+\.\d+\:\d+", page.html)

        proxy_list = proxy_list + proxies_found
        for proxy in proxy_list:
            proxy_count += 1

        session.close()

        for link in links:
            index_link = urls.index(link)
            print_task(f"[{index_link}] crawling sublink proxies", PURPLE)

            try:
                r = session.get(link)
                page = r.html.find("html", first=True)
                proxies_found = re.findall("\d+\.\d+\.\d+\.\d+\:\d+", page.html)

                proxy_list = proxy_list + proxies_found
                for proxy in proxy_list:
                    proxy_count += 1

                session.close()
            except:
                pass
    except:
        pass

    proxy_list = list(dict.fromkeys(proxy_list))
    for proxy in proxy_list:
        threading.Thread(
            target=checker_proxies,
            args=(proxy,),
        ).start()


def proxy(username):
    processRunning()
    setTitleMode("Proxy Scraper")

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
        threading.Thread(
            target=crwaling_proxies,
            args=(
                url,
                urls,
            ),
        ).start()

    # print_task("proxy scraper finished", GREEN)

    # print_task("check Uzumaki/proxy/proxies.txt", WHITE)
