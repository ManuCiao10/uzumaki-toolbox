from handler.utils import *
import time
import os
import requests
from bs4 import BeautifulSoup
import csv
import threading

def geocodeRun(zip_zode):
    
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    }

    query_page = 1
    while query_page <= 100:

        params = {
            'k': zip_zode,
            's': query_page,
        }

        session = requests.Session()
        resp = session.get('https://zip-codes.nonsolocap.it/cap', params=params, headers=headers)
        
        if resp.status_code == 200:
            if "did not match any documents." in resp.text:
                print_task("[geocode %s] %s" % (zip_zode, "did not match any documents."), RED)
                os._exit(1)

            if query_page == 1:
                print_task("[geocode %s] successful got session..." % zip_zode, PURPLE)
            
            soup = BeautifulSoup(resp.text, 'html.parser')

            for td in soup.find_all('td', class_="d-none d-sm-table-cell ha"):
                address = td.text     

                for td in soup.find_all('td', class_="d-none d-sm-table-cell"):
                    try:
                        int(td.text)
                    except ValueError:
                        city = td.text

                for td in soup.find_all('td', class_="d-none d-lg-table-cell text-nowrap"):
                    region = td.text

                print_task("[geocode %s] %s, %s, %s" % (zip_zode, address, city, region), GREEN)

                with open("Uzumaki/geocode/result.csv", "a") as f:
                    if os.stat("Uzumaki/geocode/result.csv").st_size == 0:
                        writer = csv.writer(f)
                        writer.writerow(["zip_zode", "address", "city", "region"])
                    writer = csv.writer(f)
                    writer.writerow([zip_zode, address, city, region])

            query_page += 10

        else:
            print_task("[geocode %s] error %s" % (zip_zode, resp.status_code), RED)
            time.sleep(1)


def geocode():
    print_task("starting geocoding...", CYAN)

    try :
        with open("Uzumaki/geocode/geocoding.csv", "r") as f:
            reader = csv.reader(f)

            try:
                next(reader)
            except StopIteration:
                print_task("file is empty", RED)
                time.sleep(1)
                os._exit(1)

            try:
                row = next(reader)
            except StopIteration:
                print_task("please fill Uzumaki/geocode/geocoding.csv", RED)
                time.sleep(1)
                os._exit(1)

            f.seek(0)
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                zip_zode = row[0].lower().strip()

                threading.Thread(target=geocodeRun , args=(zip_zode,)).start()

    except FileNotFoundError:
        print_task("Uzumaki/geocode/geocoding.csv not found", RED)
        time.sleep(1)
        os._exit(1)