
        # print_task("Proxy: " + str(proxy), PURPLE)

    #     self.client.headers = {
    #         "authority": "login.yahoo.com",
    #         "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    #         "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    #         "cache-control": "no-cache",
    #         "content-type": "application/x-www-form-urlencoded",
    #         "origin": "https://login.yahoo.com",
    #         "pragma": "no-cache",
    #         "sec-ch-ua": '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    #         "sec-ch-ua-mobile": "?0",
    #         "sec-ch-ua-platform": '"macOS"',
    #         "sec-fetch-dest": "document",
    #         "sec-fetch-mode": "navigate",
    #         "sec-fetch-site": "same-origin",
    #         "sec-fetch-user": "?1",
    #         "sec-gpc": "1",
    #         "upgrade-insecure-requests": "1",
    #         "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    #     }

    #     return self.__login__()

    # def __login__(self):
    #     print("getting session...")

    #     try:
    #         resp = self.client.get(
    #             "https://login.yahoo.com/account/create",
    #         )

    #         if resp.status_code != 200:
    #             print("error getting session...")
    #             time.sleep(1)
    #             return self.__login__()

    #         self.data_token = re.search(
    #             r'<input type="hidden" value="(.*?)" name="specData">', resp.text
    #         ).group(1)

    #         self.acrumb = re.search(
    #             r'<input type="hidden" value="(.*?)" name="acrumb">', resp.text
    #         ).group(1)

    #         self.crumb = re.search(
    #             r'<input type="hidden" value="(.*?)" name="crumb">', resp.text
    #         ).group(1)

    #     except Exception as e:
    #         print("error doing request: " + str(e))
    #         return self.__login__()

    #     print("Successfull got session...")
    #     return self.__payload__()

    # def __payload__(self):
    #     print("getting payload...")

    #     self.password = f"{urandom(10).hex()}@!"
    #     token = urandom(3).hex()
    #     self.name = get_first_name()
    #     self.surname = get_last_name()
    #     self.email = f"{self.name}.{self.surname}{token}".lower()
    #     self.country = "IT"
    #     self.phone_number = "3662299421"

    #     self.params = {
    #         "intl": "it",
    #         "specId": "yidregsimplified",
    #         "context": "reg",
    #         "done": "https://www.yahoo.com",
    #     }

    #     self.browser_fp_data = "browser-fp-data=%7B%22language%22%3A%22en-GB%22%2C%22colorDepth%22%3A30%2C%22deviceMemory%22%3A4%2C%22pixelRatio%22%3A2%2C%22hardwareConcurrency%22%3A8%2C%22timezoneOffset%22%3A-120%2C%22timezone%22%3A%22Europe%2FRome%22%2C%22sessionStorage%22%3A1%2C%22localStorage%22%3A1%2C%22indexedDb%22%3A1%2C%22openDatabase%22%3A1%2C%22cpuClass%22%3A%22unknown%22%2C%22platform%22%3A%22MacIntel%22%2C%22doNotTrack%22%3A%22unknown%22%2C%22plugins%22%3A%7B%22count%22%3A4%2C%22hash%22%3A%220b9799dd33522fb458a9aa13bea17079%22%7D%2C%22canvas%22%3A%22canvas+winding%3Ayes%7Ecanvas%22%2C%22webgl%22%3A1%2C%22adBlock%22%3A0%2C%22hasLiedLanguages%22%3A0%2C%22hasLiedResolution%22%3A0%2C%22hasLiedOs%22%3A0%2C%22hasLiedBrowser%22%3A0%2C%22touchSupport%22%3A%7B%22points%22%3A0%2C%22event%22%3A0%2C%22start%22%3A0%7D%2C%22fonts%22%3A%7B%22count%22%3A27%2C%22hash%22%3A%22d52a1516cfb5f1c2d8a427c14bc3645f%22%7D%2C%22audio%22%3A%22122.8735701811529%22%2C%22resolution%22%3A%7B%22w%22%3A%221728%22%2C%22h%22%3A%221117%22%7D%2C%22availableResolution%22%3A%7B%22w%22%3A%221020%22%2C%22h%22%3A%221728%22%7D%2C%22ts%22%3A%7B%22serve%22%3A1680262528711%2C%22render%22%3A1680262529058%7D%7D"

    #     data = (
    #         self.browser_fp_data
    #         + "&specId=yidregsimplified&cacheStored=&crumb="
    #         + self.crumb
    #         + "&acrumb="
    #         + self.acrumb
    #         + "&sessionIndex=QQ--&done=https%3A%2F%2Fwww.yahoo.com&googleIdToken=&authCode=&attrSetIndex=1&specData="
    #         + self.data_token
    #         + "&multiDomain=def&tos0=oath_freereg%7Cit%7Cit-IT&firstName="
    #         + self.name
    #         + "&lastName="
    #         + self.surname
    #         + "&userid-domain=yahoo&userId="
    #         + self.email
    #         + "&yidDomainDefault=yahoo.com&yidDomain=yahoo.com"
    #         + "&password="
    #         + self.password
    #         + "&mm=1&dd=23&yyyy=2000"
    #         + "&shortCountryCode=IT&phone=3662299421&signup"
    #     )

    #     try:
    #         response = self.client.post(
    #             "https://login.yahoo.com/account/create",
    #             params=self.params,
    #             data=data,
    #         )

    #     except Exception as e:
    #         print("error doing request " + str(e))
    #         time.sleep(3)
    #         return self.__payload__()

    #     print("Successfull got payload")
    #     with open("response.html", "w") as f:
    #         f.write(response.text)

    #     return self.__send_code__(response.text)

    # def __send_code__(self, resp):
    #     print("sending code...")

    #     with open("response.html", "w") as f:
    #         f.write(resp)

    #     acrumb = re.search(
    #         r'<input type="hidden" value="(.*?)" name="acrumb">', resp
    #     ).group(1)

    #     crumb = re.search(
    #         r'<input type="hidden" value="(.*?)" name="crumb">', resp
    #     ).group(1)

    #     specData = re.search(
    #         r'<input type="hidden" value="(.*?)" name="specData">', resp
    #     ).group(1)

    #     data = (
    #         self.browser_fp_data
    #         + f"&specId=yidregsimplified&cacheStored=&crumb={crumb}&acrumb={acrumb}"
    #         + "&sessionIndex=QQ--&done=https%3A%2F%2Fwww.yahoo.com&googleIdToken=&authCode=&attrSetIndex=1&specData="
    #         + f"{specData}&multiDomain=def&shortCountryCode=IT&phone=3662299421&signup="
    #     )

    #     headers = {
    #         "authority": "login.yahoo.com",
    #         "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    #         "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    #         "cache-control": "max-age=0",
    #         "content-type": "application/x-www-form-urlencoded",
    #         "origin": "https://login.yahoo.com",
    #         "referer": "https://login.yahoo.com/account/create?specId=yidregsimplified&intl=it&context=reg&done=https%3A%2F%2Fwww.yahoo.com",
    #         "sec-ch-ua": '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    #         "sec-ch-ua-mobile": "?0",
    #         "sec-ch-ua-platform": '"macOS"',
    #         "sec-fetch-dest": "document",
    #         "sec-fetch-mode": "navigate",
    #         "sec-fetch-site": "same-origin",
    #         "sec-fetch-user": "?1",
    #         "sec-gpc": "1",
    #         "upgrade-insecure-requests": "1",
    #         "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    #     }
    #     response = self.client.post(
    #         "https://login.yahoo.com/account/create",
    #         params=self.params,
    #         data=data,
    #         headers=headers,
    #     )

    #     print("code sent")
    #     with open("payload.html", "w") as f:
    #         f.write(response.text)

    #     if "error?code=E500" in response.text:
    #         print("error sending code")
    #         time.sleep(3)
    #         return self.__payload__()
    #     print(response.status_code)
    #     print(response.url)