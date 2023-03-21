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
        time.sleep(3)
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
                        with open("Uzumaki/geocode/result.csv", "a", newline="") as f:
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
        time.sleep(3)
        return

    except urllib.error.HTTPError:
        print_task("[geocode %s] http error" % zipcode, RED)
        time.sleep(3)
        return

    except:
        print_task("[geocode %s] unexpected error" % zipcode, RED)
        time.sleep(3)
        return


def geocode(username):
    processRunning()
    setTitleMode("geocode")
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
                exit_program()

            try:
                row = next(reader)
            except StopIteration:
                print_task("please fill Uzumaki/geocode/geocode.csv", RED)
                exit_program()

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
        time.sleep(3)
        return


def geocodeRunUsa(zipcode):
    urls = [
        "https://data.openaddresses.io/openaddr-collected-us_northeast.zip",
        "https://data.openaddresses.io/openaddr-collected-us_midwest.zip",
        "https://data.openaddresses.io/openaddr-collected-us_south.zip",
        "https://data.openaddresses.io/openaddr-collected-us_west.zip",
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
                            print_task(f"[geocode {zipcode}] {line}", GREEN)

                            number = str(line).split(",")[2]
                            street = str(line).split(",")[3]
                            city = str(line).split(",")[5]
                            region = str(line).split(",")[7]
                            with open(
                                "Uzumaki/geocode/result.csv", "a", newline=""
                            ) as f:
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
                                        "usa",
                                    ]
                                )

            print_task("[geocode %s] finished check results.csv file" % zipcode, CYAN)
            time.sleep(3)
            return

        except urllib.error.HTTPError:
            print_task("[geocode %s] http error" % zipcode, RED)
            time.sleep(3)
            return

        except:
            print_task("[geocode %s] unexpected error" % zipcode, RED)
            time.sleep(3)
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
                            print_task(f"[geocode {zipcode}] {line}", GREEN)

                            number = str(line).split(",")[2]
                            street = str(line).split(",")[3]
                            city = str(line).split(",")[5]
                            region = str(line).split(",")[7]
                            with open(
                                "Uzumaki/geocode/result.csv", "a", newline=""
                            ) as f:
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
    time.sleep(3)
    return


def geocode_handler(country, zip_code):
    array_Italy = ["it", "ita", "italy", "italia"]
    array_Spain = ["es", "esp", "spain", "spagna"]
    array_Usa = ["us", "usa", "united states", "stati uniti"]

    if country.strip().lower() in array_Italy:
        geocodeRunItaly(zip_code)
    elif country.strip().lower() in array_Spain:
        geocodeRunSpain(zip_code)
    elif country.strip().lower() in array_Usa:
        geocodeRunUsa(zip_code)
    else:
        print_task("[geocode %s] error: %s" % (zip_code, "country not supported"), RED)
        time.sleep(3)
        return
