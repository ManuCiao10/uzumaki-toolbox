import os
from handler.utils import *
import csv
import threading
import random
import time
import names
from internal.security import processRunning


class Addyjigger:
    def __init__(
        self, first_name, second_name, mobile_number, address, house_number, country
    ):
        self.supported_countries = [
            "France",
            "Spain",
            "Italy",
            "Germany",
        ]

        self.street_name = {
            "France": ["rue", "r", "boulevard", "blvd", "avenue", "av", "chemin", "ch"],
            "Spain": ["calle", "cl", "avenida", "av", "carrer", "c", "passeig", "pg"],
            "Italy": ["via", "v", "piazza", "p", "corso", "c", "viale", "vl"],
            "Germany": ["straße", "str", "straße", "str", "platz", "pl", "allee", "al"],
        }

        self.first_name = first_name
        self.second_name = second_name
        self.mobile_number = mobile_number
        self.address = address
        self.house_number = house_number
        self.country = country

        if self.country not in self.supported_countries:
            print_task(
                f"{self.country} is not supported. Please choose from {self.supported_countries}",
                RED,
            )
            exit_program()

        return self.jig()

    def generate_phone_number(self, prefix):
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

    def random_name(self):
        return names.get_full_name().split(" ")[0]

    def random_surname(self):
        return names.get_full_name().split(" ")[1]

    def jig(self):
        print_task("Jigging the address...", PURPLE)

        streets = []
        phone_number = []
        name = []
        surname = []

        # remove the street name from the address
        try:
            address_tochange = self.address.split(" ")
            for i in address_tochange:
                if i in self.street_name[self.country]:
                    address_tochange.remove(i)
            street_name = " ".join(address_tochange)
        except:
            street_name = self.address

        for addy in self.street_name[self.country]:
            streets.append(addy + " " + street_name)
            phone_number.append(self.generate_phone_number(self.mobile_number))
            name.append(self.random_name())
            surname.append(self.random_name())

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

        for i in range(len(streets)):
            with open("Uzumaki/jigger/result.csv", "a", newline="") as file:
                writer = csv.writer(file)

                writer.writerow(
                    [
                        name[i],
                        surname[i],
                        phone_number[i],
                        streets[i],
                        self.house_number,
                        self.country,
                    ]
                )
                print_task("writing info in result.csv", GREEN)

        time.sleep(3)
        return


def jigger(username):
    processRunning()
    setTitleMode("jigger")

    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print(RED + BANNER + RESET)

        print(
            f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n"
        )

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
            time.sleep(1)

    with open("Uzumaki/jigger/" + file, "r") as f:
        reader = csv.reader(f)

        try:
            next(reader)
        except StopIteration:
            print_task("file is empty", RED)
            exit_program()

        try:
            row = next(reader)
        except StopIteration:
            print_task("Please Fill Uzumaki/jigger/" + file, RED)
            exit_program()

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
                    target=Addyjigger,
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
                exit_program()
