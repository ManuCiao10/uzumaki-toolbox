from handler.utils import *
import time
import os
import csv
import threading
from io import BytesIO
from zipfile import ZipFile
import urllib.request


def geocodeRunVersion(zipcode):
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
                                    ["address", "number", "city", "region", "zip_zode"]
                                )
                            writer = csv.writer(f)
                            writer.writerow(
                                [street, number, city.lower(), region.lower(), zipcode]
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


def geocode():
    print_task("starting geocoding...", CYAN)

    try:
        with open("Uzumaki/geocode/geocoding.csv", "r") as f:
            reader = csv.reader(f)

            try:
                next(reader)
            except StopIteration:
                print_task("file is empty", RED)
                time.sleep(2)
                os._exit(1)

            try:
                row = next(reader)
            except StopIteration:
                print_task("please fill Uzumaki/geocode/geocoding.csv", RED)
                input("Press Enter to exit...")
                os._exit(1)

            f.seek(0)
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                zip_zode = row[0].lower().strip()

                threading.Thread(target=geocodeRunVersion, args=(zip_zode,)).start()

    except FileNotFoundError:
        print_task("Uzumaki/geocode/geocoding.csv not found", RED)
        time.sleep(2)
        os._exit(1)
