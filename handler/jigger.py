import os
from handler.utils import *
import csv
import threading
import names
import random
import numpy as np

country_prefix = {
    "Afghanistan": "+93",
    "Albania": "+355",
    "Algeria": "+213",
    "Andorra": "+376",
    "Angola": "+244",
    "Antigua and Barbuda": "+1-268",
    "Argentina": "+54",
    "Armenia": "+374",
    "Australia": "+61",
    "Austria": "+43",
    "Azerbaijan": "+994",
    "Bahamas": "+1-242",
    "Bahrain": "+973",
    "Bangladesh": "+880",
    "Barbados": "+1-246",
    "Belarus": "+375",
    "Belgium": "+32",
    "Belize": "+501",
    "Benin": "+229",
    "Bhutan": "+975",
    "Bolivia": "+591",
    "Bosnia and Herzegovina": "+387",
    "Botswana": "+267",
    "Brazil": "+55",
    "Brunei": "+673",
    "Bulgaria": "+359",
    "Burkina Faso": "+226",
    "Burundi": "+257",
    "Cambodia": "+855",
    "Cameroon": "+237",
    "Canada": "+1",
    "Cape Verde": "+238",
    "Central African Republic": "+236",
    "Chad": "+235",
    "Chile": "+56",
    "China": "+86",
    "Colombia": "+57",
    "Comoros": "+269",
    "Congo, Democratic Republic of the": "+243",
    "Congo, Republic of the": "+242",
    "Costa Rica": "+506",
    "Cote d'Ivoire": "+225",
    "Croatia": "+385",
    "Cuba": "+53",
    "Cyprus": "+357",
    "Czech Republic": "+420",
    "Denmark": "+45",
    "Djibouti": "+253",
    "Dominica": "+1-767",
    "Dominican Republic": "+1-809, +1-829, +1-849",
    "East Timor (Timor-Leste)": "+670",
    "Ecuador": "+593",
    "Egypt": "+20",
    "El Salvador": "+503",
    "Equatorial Guinea": "+240",
    "Eritrea": "+291",
    "Estonia": "+372",
    "Ethiopia": "+251",
    "Fiji": "+679",
    "Finland": "+358",
    "France": "+33",
    "Gabon": "+241",
    "Gambia": "+220",
    "Georgia": "+995",
    "Germany": "+49",
    "Ghana": "+233",
    "Greece": "+30",
    "Grenada": "+1-473",
    "Guatemala": "+502",
    "Guinea": "+224",
    "Guinea-Bissau": "+245",
    "Guyana": "+592",
    "Haiti": "+509",
    "Honduras": "+504",
    "Hungary": "+36",
    "Iceland": "+354",
    "India": "+91",
    "Indonesia": "+62",
    "Iran": "+98",
    "Iraq": "+964",
    "Ireland": "+353",
    "Israel": "+972",
    "Italy": "+39",
    "Jamaica": "+1-876",
    "Japan": "+81",
    "Jordan": "+962",
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


def jigStart(First_Name, Second_name, Mobile_Number, Address, HouseNumebr, Country):
    print_task("Jigging the data...", PURPLE)
    array_name = []
    array_surname = []
    array_mobile = []

    if First_Name != "random":
        last_car = First_Name[-1]
        mod1 = First_Name + last_car
        array_name.append(mod1)

        mod2 = First_Name[:-1]
        array_name.append(mod2)

        mod3 = First_Name[1:]
        array_name.append(mod3)

        middle_car = get_middle_char(First_Name)
        mod4 = First_Name.replace(middle_car, middle_car + middle_car)
        array_name.append(mod4)

        first_car = First_Name[0]
        mod5 = first_car + First_Name
        array_name.append(mod5)

        mod6 = First_Name + "x"
        array_name.append(mod6)

        mod7 = Second_name
        array_name.append(mod7)

        mod8 = Second_name + last_car
        array_name.append(mod8)

        mod9 = Second_name[:-1]
        array_name.append(mod9)

        mod10 = Second_name[1:]
        array_name.append(mod10)

        mod11 = Second_name.replace(middle_car, middle_car + middle_car)
        array_name.append(mod11)

        mod12 = first_car + Second_name
        array_name.append(mod12)

        mod13 = Second_name + "x"
        array_name.append(mod13)

        mod14 = "x" + First_Name
        array_name.append(mod14)

        mod15 = "x" + Second_name
        array_name.append(mod15)

    else:
        First_Name = names.get_first_name()
        array_name.append(First_Name)

    if Second_name != "random":
        last_car = Second_name[-1]
        mod1_ = Second_name + last_car
        array_surname.append(mod1_)

        mod2_ = Second_name[:-1]
        array_surname.append(mod2_)

        mod3_ = Second_name[1:]
        array_surname.append(mod3_)

        middle_car_ = get_middle_char(Second_name)
        mod4_ = Second_name.replace(middle_car_, middle_car_ + middle_car_)
        array_surname.append(mod4_)

        first_car_ = Second_name[0]
        mod5_ = first_car_ + Second_name
        array_surname.append(mod5_)

        mod6_ = Second_name + "x"
        array_surname.append(mod6_)

        mod7_ = First_Name
        array_surname.append(mod7_)

        mod8_ = First_Name + last_car
        array_surname.append(mod8_)

        mod9_ = First_Name[:-1]
        array_surname.append(mod9_)

        mod10_ = First_Name[1:]
        array_surname.append(mod10_)

        mod11_ = First_Name.replace(middle_car_, middle_car_ + middle_car_)
        array_surname.append(mod11_)

        mod12_ = first_car_ + First_Name
        array_surname.append(mod12_)

        mod13_ = First_Name + "x"
        array_surname.append(mod13_)

        mod14_ = "x" + First_Name
        array_surname.append(mod14_)

        mod15_ = "x" + Second_name
        array_surname.append(mod15_)

    else:
        Second_name = names.get_last_name()
        array_surname.append(Second_name)

    prefix = country_prefix[Country]

    for i in array_name:
        array_mobile.append(generate_phone_number(prefix))

    array_ = []
    addy = Address.split(" ")
    counter = 0

    for i in addy:
        counter += 1

        last_car = i[-1]
        mod1 = i + last_car
        array_.append(mod1)

        mod2 = i[:-1]
        array_.append(mod2)

        mod3 = i[1:]
        array_.append(mod3)

        middle_car = get_middle_char(i)
        mod4 = i.replace(middle_car, middle_car + middle_car)
        array_.append(mod4)

        first_car = i[0]
        mod5 = first_car + i
        array_.append(mod5)

        mod6 = i + "x"
        array_.append(mod6)

        mod7 = "Street " + i
        array_.append(mod7)

        mod8 = i + "xx"
        array_.append(mod8)

        mod9 = "xx" + i
        array_.append(mod9)

        mod10 = "x" + i
        array_.append(mod10)

        mod11 = i + "x"
        array_.append(mod11)

        mod12 = "x" + i + "x"
        array_.append(mod12)

        mod13 = "x" + i + "xx"
        array_.append(mod13)

        mod14 = "x " + i
        array_.append(mod14)

        mod15 = i + " x"
        array_.append(mod15)

    split_arrays = np.array_split(array_, counter)
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


def jigger():
    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

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
    except KeyError:
        print_task("invalid option", RED)
        time.sleep(3)
        os._exit(1)

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
            First_Name = row[0].lower().strip()
            Second_name = row[1].lower().strip()
            Mobile_Number = row[2].lower().strip()
            Address = row[3].lower().strip()
            HouseNumebr = row[4].lower().strip()
            Country = row[5].capitalize().strip()

            threading.Thread(
                target=jigStart,
                args=(
                    First_Name,
                    Second_name,
                    Mobile_Number,
                    Address,
                    HouseNumebr,
                    Country,
                ),
            ).start()
