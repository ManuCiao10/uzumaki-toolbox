from handler.utils import *
import time
import os
import csv
import threading
from io import BytesIO
from zipfile import ZipFile
import urllib.request
from internal.security import processRunning


def geocodeRunItaly(zipcode):
    try:
        url = urllib.request.urlopen(
            "https://data.openaddresses.io/runs/1042889/it/countrywide.zip"
        )
    except:
        print_task("[geocode %s] error: %s" % (zipcode, "error getting data..."), RED)
        input("Press Enter to exit...")
        return

    try:
        with ZipFile(BytesIO(url.read())) as my_zip_file:
            print_task("[geocode %s] successful got session..." % zipcode, PURPLE)

            for contained_file in my_zip_file.namelist():
                for line in my_zip_file.open(contained_file).readlines():
                    if "," + zipcode + "," in str(line):
                        print_task("[geocode %s] %s" % (zipcode, line), GREEN)

                        number = str(line).split(",")[2]
                        street = str(line).split(",")[3]
                        city = str(line).split(",")[5]
                        region = str(line).split(",")[7]
                        with open("Uzumaki/geocode/result.csv", "a") as f:
                            if os.stat("Uzumaki/geocode/result.csv").st_size == 0:
                                writer = csv.writer(f)
                                writer.writerow(
                                    [
                                        "address",
                                        "number",
                                        "city",
                                        "region",
                                        "zip_zode",
                                        "country",
                                    ]
                                )
                            writer = csv.writer(f)
                            writer.writerow(
                                [
                                    street,
                                    number,
                                    city.lower(),
                                    region.lower(),
                                    zipcode,
                                    "italy",
                                ]
                            )

        print_task("[geocode %s] finished check results.csv file" % zipcode, CYAN)
        input("Press Enter to exit...")
        return

    except urllib.error.HTTPError:
        print_task("[geocode %s] http error" % zipcode, RED)
        input("Press Enter to exit...")
        return

    except:
        print_task("[geocode %s] unexpected error" % zipcode, RED)
        input("Press Enter to exit...")
        return


def geocode(username):
    processRunning()
    os.system("cls" if os.name == "nt" else "clear")

    print(f"{RED}{BANNER}{RESET}")

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    print_task("starting geocoding...", CYAN)

    try:
        with open("Uzumaki/geocode/geocode.csv", "r") as f:
            reader = csv.reader(f)

            try:
                next(reader)
            except StopIteration:
                print_task("file is empty", RED)
                time.sleep(3)
                os._exit(1)

            try:
                row = next(reader)
            except StopIteration:
                print_task("please fill Uzumaki/geocode/geocode.csv", RED)
                input("Press Enter to exit...")
                os._exit(1)

            f.seek(0)
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                country = row[0].lower().strip()
                zip_code = row[1].lower().strip()

                threading.Thread(
                    target=geocode_handler, args=(country, zip_code)
                ).start()

    except FileNotFoundError:
        print_task("Uzumaki/geocode/geocode.csv not found", RED)
        input("Press Enter to exit...")
        return


def geocodeRunSpain(zipcode):
    urls = [
        "https://data.openaddresses.io/runs/1049007/es/32628.zip",
        "https://data.openaddresses.io/runs/1045841/es/25831.zip",
        "https://data.openaddresses.io/runs/1045551/es/25830.zip",
        "https://data.openaddresses.io/runs/1045806/es/25829.zip",
    ]

    for website in urls:
        try:
            url = urllib.request.urlopen(website)
        except:
            print_task(
                "[geocode %s] error: %s" % (zipcode, "error getting data..."), RED
            )

        try:
            with ZipFile(BytesIO(url.read())) as my_zip_file:
                print_task("[geocode %s] successful got session..." % zipcode, PURPLE)

                for contained_file in my_zip_file.namelist():
                    for line in my_zip_file.open(contained_file).readlines():
                        if "," + zipcode + "," in str(line):
                            print_task("[geocode %s] %s" % (zipcode, line), GREEN)

                            number = str(line).split(",")[2]
                            street = str(line).split(",")[3]
                            city = str(line).split(",")[5]
                            region = str(line).split(",")[7]
                            with open("Uzumaki/geocode/result.csv", "a") as f:
                                if os.stat("Uzumaki/geocode/result.csv").st_size == 0:
                                    writer = csv.writer(f)
                                    writer.writerow(
                                        [
                                            "address",
                                            "number",
                                            "city",
                                            "region",
                                            "zip_zode",
                                            "country",
                                        ]
                                    )
                                writer = csv.writer(f)
                                writer.writerow(
                                    [
                                        street.lower(),
                                        number,
                                        city.lower(),
                                        region.lower(),
                                        zipcode,
                                        "spain",
                                    ]
                                )

        except urllib.error.HTTPError:
            print_task("[geocode %s] http error" % zipcode, RED)

        except:
            print_task("[geocode %s] unexpected error" % zipcode, RED)

    print_task("[geocode %s] finished check results.csv file" % zipcode, CYAN)
    input("Press Enter to exit...")
    return


def geocode_handler(country, zip_code):
    array_Italy = ["it", "ita", "italy", "italia"]
    array_Spain = ["es", "esp", "spain", "spagna"]

    if country.strip().lower() in array_Italy:
        geocodeRunItaly(zip_code)
    elif country.strip().lower() in array_Spain:
        geocodeRunSpain(zip_code)
    else:
        print_task("[geocode %s] error: %s" % (zip_code, "country not supported"), RED)
        input("Press Enter to exit...")
        return
