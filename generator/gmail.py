import requests
import random
import base64


class ByPassGoogleBotGuard(object):
    size = 2268

    def generate_random_num(self, range_val):
        rand_num = ""
        for i in range(range_val):
            gen_rand_num = random.randint(1, 9)
            rand_num += str(gen_rand_num)
        return int(rand_num)

    def generate_bg_list_array(self):
        bg_list = []
        gen_l = 2
        i = 0
        while i <= self.size:
            bg_list.append(self.generate_random_num(gen_l))
            if gen_l == 2:
                gen_l = 3
            elif gen_l == 3:
                gen_l = 2
            i += 1
        return bg_list

    def generate_bg_request_data(self):
        bg_list = self.generate_bg_list_array()
        bg_uni = "".join(map(chr, bg_list))
        bg_b64 = base64.b64encode(bg_uni.encode())
        bg_request_data = "!{}".format(
            bg_b64.decode().replace("+", "-").replace("/", "_").replace("=", "")
        )
        return bg_request_data


def gmail(username):
    # processRunning()
    # setTitleMode("GENERATOR YAHOO")
    data = ByPassGoogleBotGuard().generate_bg_request_data()
    print(data)

    headers = {
        "authority": "accounts.google.com",
        "accept": "*/*",
        "accept-language": "en-GB,en;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "google-accounts-xsrf": "1",
        "origin": "https://accounts.google.com",
        "pragma": "no-cache",
        "referer": "https://accounts.google.com/signup/v2/webcreateaccount?biz=false&cc=IT&flowEntry=SignUp&flowName=GlifWebSignIn&",
        "sec-ch-ua": '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"macOS"',
        "sec-ch-ua-platform-version": '"12.3.0"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "x-same-domain": "1",
    }

    params = {
        "hl": "it",
        "_reqid": "262019",
        "rt": "j",
    }

    data = f"flowEntry=SignUp&flowName=GlifWebSignIn&continue=https%3A%2F%2Faccounts.google.com%2FManageAccount%3Fnc%3D1&f.req=%5B%22AEThLlwyu1F1-LK8NgnKa6FO-3cIjkeBUi8kmEKOisbYaFAE2Vgy6h76uxTKxBl87iFNijtN5Z7-D7u16PE627w-6azVhYEL7S-35sH2tBdpVWraOLW2FNwymWw8Ht-Sdnc0IL99tWbNR6RjkwZtugLI3CPXoy_itOmh-rhO_2DnJAxP_04y6MmFNDy9E_GmqczzoRa352vN2xOxnhJRqkSVwA_GA6B04A%22%2C%22emanuele%22%2C%22diocane%22%2C%22emanuele%22%2C%22diocane%22%2C%22emanuelecanedporn%22%2C%22caccolafritta3%22%2C%22emanuelecanedporn%22%2C1%2C1%2C%5Bnull%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5D%5D%5D&bgRequest={data}&azt=AFoagUW0LrJz2x8mSBGh-dW7wFPfx043bg%3A1684249974736&cookiesDisabled=false&deviceinfo=%5Bnull%2Cnull%2Cnull%2C%5B%5D%2Cnull%2C%22IT%22%2Cnull%2Cnull%2Cnull%2C%22GlifWebSignIn%22%2Cnull%2C%5Bnull%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5D%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C2%2Cnull%2C0%2C1%2C%22%22%2Cnull%2Cnull%2C1%2C0%5D&gmscoreversion=undefined&"

    response = requests.post(
        "https://accounts.google.com/_/signup/accountdetails",
        params=params,
        headers=headers,
        data=data,
    )
    print(response.text)

    with open("response_gmail.html", "w") as f:
        f.write(response.text)
