import os
from handler.utils import *
import csv
import threading
import random
import time
import names
import numpy as np

road_dictionary = {
    "Italy": "Via",
    "France": "Rue",
    "Spain": "Calle",
    "Germany": "Straße",
    "United Kingdom": "Road",
    "United States": "Street",
    "Canada": "Street",
    "Australia": "Street",
}


def get_middle_char(input_str):
    length = len(input_str)
    if length % 2 == 0:
        return input_str[length // 2 - 1 : length // 2 + 1]
    else:
        return input_str[length // 2]


def generate_phone_number(prefix):
    # Remove the '+' sign from the prefix
    prefix = prefix.replace("+", "")

    # Determine the number of digits in the prefix
    num_prefix_digits = len(prefix)

    # Generate a random number with the remaining digits
    remaining_digits = 10 - num_prefix_digits
    subscriber_number = "".join(
        [str(random.randint(0, 9)) for _ in range(remaining_digits)]
    )

    # Combine the prefix and subscriber number and return the phone number
    return f"{prefix}{subscriber_number}"


def generate_modifications(name, prefix=""):
    modifications = []
    last_car = name[-1]
    middle_car = get_middle_char(name)

    # Add modified versions of the name
    modifications.append(name + last_car)
    modifications.append(name[:-1])
    modifications.append(name[1:])
    modifications.append(name.replace(middle_car, middle_car + middle_car))
    modifications.append(prefix + name)
    modifications.append(name + "x")
    modifications.append("x" + name)

    return modifications


def jig_start(
    First_Name,
    Second_name,
    Mobile_Number,
    Address,
    HouseNumebr,
    Country,
):
    print_task("Jigging the data...", PURPLE)
    array_name = []
    array_surname = []
    array_mobile = []

    try:
        road = road_dictionary[Country]
    except KeyError:
        road = "Street"

    if First_Name != "random":
        array_name.extend(generate_modifications(First_Name))
        array_name.extend(generate_modifications(Second_name, prefix=First_Name[0]))
    else:
        First_Name = names.get_first_name()
        array_name.append(First_Name)

    if Second_name != "random":
        array_surname.extend(generate_modifications(Second_name))
        array_surname.extend(generate_modifications(First_Name, prefix=Second_name[0]))
    else:
        Second_name = names.get_last_name()
        array_surname.append(Second_name)

    prefix = country_prefix[Country]

    for i in array_name:
        array_mobile.append(generate_phone_number(prefix))

    addy = Address.split()

    array_ = (
        [i + i[-1] for i in addy]
        + [i[:-1] for i in addy]
        + [i[1:] for i in addy]
        + [i.replace(get_middle_char(i), get_middle_char(i) * 2) for i in addy]
        + [i[0] + i for i in addy]
        + [i + "x" for i in addy]
        + [road + i for i in addy]
        + [i + "xx" for i in addy]
        + ["xx" + i for i in addy]
        + ["x" + i for i in addy]
        + [i + "x" for i in addy]
        + ["x" + i + "x" for i in addy]
        + ["x" + i + "xx" for i in addy]
        + ["x " + i for i in addy]
        + [i + " x" for i in addy]
    )

    num_addresses = len(addy)
    split_arrays = np.array_split(array_, num_addresses)
    result_array = [" ".join(row) for row in np.transpose(split_arrays)]

    with open("Uzumaki/jigger/result.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                "First Name",
                "Second Name",
                "Mobile Number",
                "Address",
                "House Number",
                "Country",
            ]
        )

    # csv
    for i in range(len(array_name)):
        with open("Uzumaki/jigger/result.csv", "a", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(
                [
                    array_name[i],
                    array_surname[i],
                    array_mobile[i],
                    result_array[i],
                    HouseNumebr,
                    Country,
                ]
            )
            print_task("writing info in result.csv", GREEN)

    input("press enter to exit...")


def jigger(username):

    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print(RED + BANNER + RESET)

        print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

        os.chdir("Uzumaki/jigger")
        files = os.listdir()
        os.chdir("../..")

        files = [file for file in files if file != ".DS_Store"]
        files = [file for file in files if file != "result.csv"]

        files_dict = {}

        for index, file in enumerate(files):
            print_file(str(index) + ". " + file)

            files_dict[str(index)] = file

        print("\n")
        option = input(TAB + "> choose: ")

        try:
            file = files_dict[option]
            break
        except KeyError:
            print_task("invalid option", RED)
            time.sleep(2)

    with open("Uzumaki/jigger/" + file, "r") as f:
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
            print_task("Please Fill Uzumaki/jigger/" + file, RED)
            time.sleep(2)
            os._exit(1)

        f.seek(0)
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            First_Name, Second_name, Mobile_Number, Address, HouseNumebr, Country = [
                r.lower().strip() if i < 5 else r.capitalize().strip()
                for i, r in enumerate(row)
            ]

            try:
                threading.Thread(
                    target=jig_start,
                    args=(
                        First_Name,
                        Second_name,
                        Mobile_Number,
                        Address,
                        HouseNumebr,
                        Country,
                    ),
                ).start()

            except Exception as e:
                print_task(f"Error: {e}", RED)
                time.sleep(3)
                os._exit(1)
