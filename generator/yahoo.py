import requests
import time
import tls_client


class Yahoo:
    def __init__(self):
        # read data input name, surname etc..
        # read the apikey for get the phone number
        self.session = tls_client.Session(client_identifier="chrome_105")

        self.headers = {
            "authority": "login.yahoo.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://login.yahoo.com",
            "pragma": "no-cache",
            "referer": "https://login.yahoo.com/account/create",
            "sec-ch-ua": '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        }

        return self.login()

    def login(self):
        print("getting session...")

        try:
            resp = self.session.get(
                "https://login.yahoo.com/account/create",
                headers=self.headers,
            )
            print(resp.cookies.get_dict())
            if resp.status_code != 200:
                # retry if failed
                print("error getting session...")
                time.sleep(3)
                return self.login()

            print("Successfull got session...")
        except Exception:
            print("error doing request...")
            time.sleep(3)
            return self.login()

        return self.payload()

    def payload(self):
        print("getting payload...")

        params = {
            "intl": "it",
            "specId": "yidregsimplified",
            "context": "reg",
            "done": "https://www.yahoo.com",
        }

        data = "browser-fp-data=%7B%22language%22%3A%22en-GB%22%2C%22colorDepth%22%3A24%2C%22deviceMemory%22%3A1%2C%22pixelRatio%22%3A2%2C%22hardwareConcurrency%22%3A7%2C%22timezoneOffset%22%3A-120%2C%22timezone%22%3A%22Europe%2FRome%22%2C%22sessionStorage%22%3A1%2C%22localStorage%22%3A1%2C%22indexedDb%22%3A1%2C%22openDatabase%22%3A1%2C%22cpuClass%22%3A%22unknown%22%2C%22platform%22%3A%22MacIntel%22%2C%22doNotTrack%22%3A%22unknown%22%2C%22plugins%22%3A%7B%22count%22%3A4%2C%22hash%22%3A%222d8b4607a01680e3ff172e1ccd83a02a%22%7D%2C%22canvas%22%3A%22canvas+winding%3Ayes%7Ecanvas%22%2C%22webgl%22%3A1%2C%22webglVendorAndRenderer%22%3A%22Google+Inc.+%28Google%29%7EANGLE+%28Google%2C+Vulkan+1.3.0+%28SwiftShader+Device+%28Subzero%29+%280x0000C0DE%29%29%2C+SwiftShader+driver%29%22%2C%22adBlock%22%3A0%2C%22hasLiedLanguages%22%3A0%2C%22hasLiedResolution%22%3A0%2C%22hasLiedOs%22%3A0%2C%22hasLiedBrowser%22%3A0%2C%22touchSupport%22%3A%7B%22points%22%3A0%2C%22event%22%3A0%2C%22start%22%3A0%7D%2C%22fonts%22%3A%7B%22count%22%3A27%2C%22hash%22%3A%22d52a1516cfb5f1c2d8a427c14bc3645f%22%7D%2C%22audio%22%3A%22123.30898461164907%22%2C%22resolution%22%3A%7B%22w%22%3A%221440%22%2C%22h%22%3A%22900%22%7D%2C%22availableResolution%22%3A%7B%22w%22%3A%22816%22%2C%22h%22%3A%221440%22%7D%2C%22ts%22%3A%7B%22serve%22%3A1680035449265%2C%22render%22%3A1680035449771%7D%7D&specId=yidregsimplified&cacheStored=&crumb=&acrumb=X3z3MBBy&sessionIndex=&done=https%3A%2F%2Fwww.yahoo.com&googleIdToken=&authCode=&attrSetIndex=0&specData=yQyNodLzoFrXxOprM5V%2B5XWVF7hHpXv4TqbwMLLgYmgVyFOBjBQW2d7BXhbMph%2BSZ2tGeYKxBhCAHCPmUnehIGBRKLPHxIx6LypO3FM%2B8IkzwLp3EElwAiipM0iqAOTL9utPPbGVwmjnEXmnhxONl9VnbF0aMTDPxrXgSMOcPXpxwt79yLSsQL4qPTxmwDZFfc73GSI6UNlf%2BDdWoUjAqRDSd6Of3ucuSfJ1WDVQG%2FMGbFDdD55b9I10h8Pq4EQn13Pso%2FDD%2FTh%2BaL8NnZ34S8Ylui2xqR%2F7VGGg574zGlVyxoqoNMgVBClAahomD7I100tsZguNndou5AvbKe8wGj%2BNwkOoRg2jC%2B9AROgRzJojbX4hlInzeHB1CTvs7iKRoLUsla6MLQSdpOQDUlkHFwGiG4bVQJlN8vlDjvlT0Dlbq%2BtvSokWDumi3geejXBaH4LonnrqKVKfF2zaLVeWxJbDrFySlb3JO1zTDpe7axzLz2wff%2BiIVjpR41m1kCkyONoVJoUp5QTgnRYIKKa35n84Kptl%2FCf8cgzQtLrjLk0vk8VWk6yoj1rXdn1xGmyQhy%2F%2F9AlZKuCSo%2BBayCbY0nykQLX8K63YBdDfJ%2FlQvLxHCqjrtzooi%2BZSCRICeJSgWZU27Ydwy5zJ3waD%2Fy48eZ8OT85r23DAlEDBbgIM6AX5zWdezYIu%2F%2FcQzTvWQa8FbzVXxGfzxPwV3jRVzzhP6e0FxDgdhAnKsyYW6jwZIo%2Br9iweuz4jTdt%2BKS7S7ZOt%2Bv0bLXUfmqKYUdwu6zQonRuw03A4kuADnYe%2BAApCNp6WuceE%2BdHp3SORG9P0jJIxEHwWFA4i71Do8xd1ps%2FMppwN53My1zdh2JGBKyoB3qlSn0wGtOzCYJNi4XFR9DMjbOKBYW2M2bptxmi%2BxUpm8BMIdQZx1qLVRWo%2B%2Bc9L7jLn%2BL8WsMvfTlKiQbM6ACyEJHnIpSRjUryHlFxGwFY6ozDIjXxTFnORsHQo5ZwE%2BNK9o%2BL9vnTnCxTUTXyKMRRgXqdRAf3%2BXl1OXg8Q5UchWYqQH%2Bbj0QMOonQkhVbRleQc2zgP5ut9gDc%2FlNVNTshyE1v%2FUTxWNIRZXQeXLMBbVMai4ozZh0xCWrQn236lVD%2BH5uvaO141UKYc0roQrS7smf4lRDJW4Md4SYN7dlXlAGJ%2B4Tz4MyS339B0l3WpYPJFwaXySgfGyTz8Abz1VCeoUzXb7kZv0B8%2B7PaGWZQs5dJj3UonFqvhWxaTL7c4C6FCthaVkCExjS6ZCWHsDvQy6Kj1uSzLXtpagtgGOknQ7j9mYwr42a2dmu%2B9SZQSsuufrGFQeo7RjRLqtEM8idAC7AU6JkNbCA3sU8571GyNhUncFxCMXtV%2FElOH%2FSqpB1dEoFp5P%2Fk9aMzoaAiZ4ON0ImRpgVBmByfVnsttAgH3mIwkcMUB6AHFStRb5dhKwKkVDLU%2FfE%2B4cZK4OYnYnRJIfkA8YrLG8eFq%2BIV9fgNSpr75Sg6X1siquRudrWThoLZwIabRqnuyeQMVYkQUTXxq9BP7QuaBfIsNAnZ06vKwdW9KTso49gFuB%2Bdq97PMkrywBeLlXtlCQ8KtGW%2Fj3w1koGw51dxtKAck%2BvuT06Mjo84Dy3K9eqdrHcHtAvQdXxK6gIFJGkoLQX15jQ0D7Rz5I46toNEiuvkLB7z%2FQARJLGbSn9U0CWxWLC5GhwyUbw87njcKeh1YM%2Fm6JU3juva8%2BpuEGg1mecWnuaTm8ThJBI5ovUMSeNAUr9m6vW81Z70pXJn%2F%2F6GmhUHTZO%2BWV6qAqBI4duMKULTqZe1leTVyHuhnKeltldkHO3uJWOOAAJb8dlWfOG5g3%2FVZdE2PpgKBYSmeBWc9Wp%2F6ElkIXMi0isHjwtgmKYDWC6iDLOpTeod5KRB2PpXMQmelYlP1QtQ05acw%2BhKXBBptQ5QrEA7mdCxHpPfxpDm8CDM7tjWGcmDdtdhIMN7lmNpJmrYZpbTogK%2BIHvq7UeuWnBQemYcLyeQykG4GUXylGcN%2B5hkL7pqRlW0Q%2F7olnr2idrfSrZ0TWbXYb8UqtTWA1OF5ykaGc5PBvCj0ykyShiZ2rmQJHSwoq7D%2FFLu4jMOHXoUlcWaf4Vh3f%2F6srDCVUzGrX163g6FiRYg3rt8DrLMMb4QcM9lh5FAMCSNWZDPjTO6Vi08YSM7gkTGeUQ8qaPdKbDCgtheP7JwRkfM71dXVB09dtdH76JZmX1KrvgSmZNT%2BUBynNX3AEHbT7hwZ2m46LMZnY59V24I3VP8nOPfVGNYOVwyVbXbjZu2yOCPWaVO07zftfS7mQbZYPhs3lMf0e9jy6z8M8r2xgFLEI3O1k%2Bt6axA%2F%2BjnSjZ4QPv10QARYdKf1WXr9g6IymRgv5tOzMgVHqA%2BkQlcklgXmGVYZpVBhYk9JBqRDPGWK3ychpbQAL%2FiUnHxQsxPcWjKVznTUxp%2FiWaEmHDVMIsMlbpUPltctpcZgU%2FBNPJgtwA1SmQ3cPkN4qzPIt%2BNFRbte8Y4Ij13q2rsiK5fmbY4AMyve7048G%2FxPHub7tfdacr2r%2Bbnkw1XnUisNvYe3wqSw9mDwYvDGiJ%2BVyFkvi1l7tv%2FvdYkka0ftRR86sPhOBeixdhqBhvf3WivJBBZN7zAbJsaUq0WmCgyqVRCFTQZyNgRDisJOIx4EshNt0RVTgvClE6%2FeIi%2BALw18PP9BuC219CZWXc7by1qVaxM%2FUQm0UBw9HZpaIm%2Bah9vg7MgTVSRiV%2Bu2iiE39HPnLNCsmD7xFUH%2F5Nw07IR59srOmIuxZWyc2HtWyhD7l0wVB3EepCxrRP%2FzlWqNXUBY5v%2Fn2Y%2Fjz5ru%2BlIyv8m4tP45lAhVgm24bYZrE4vwd1dLbOT%2FliUG%2BfNwmWQ6kPnxw84hI2Jt0%2FzRm5Lrg0aW8olzelibW0XCgAhlmsXuinEre620XwvmYrVuiRWGyD5Qscz40aD%2FeB7YbKbs0ETsY23SH8usaSDxIA%2BTXJTxwpWGWTiDZ9QN4WXfjXMM0beEUiSwr%2Fe4fzSsmLK5k8YvEBCrJapt71Oc7%2B7E91xRyOd3w8X%2FTO2Uqet65v790QfIAlZBvRs73PTgoAk3c9Zs7Ic6mH3wwIs9gl3y4QmHLVou8Rap1LxN9DBzcvo0TXCYjCFZM2kYfOyjiBLB98yZlfHp3F7BbjELi5Jnfef5%2BMFxa6iwJ7zEPVRhrkxvnisdFT2W0GwZyY0jzVnTuB4JpIksIab0cdGnMQSRf3%2F9UE%2FSaHnbFTwp1LN7%2F3oV9AwZy7vvJLGFKAM43%2B8Hcppc%2Bw0UyjNyZ%2FqvmYoOsleoUHLmSaTVtPnH1RehFnNvb87rBphErKI3%2F9h%2BXvh0zjfETmT2HJnBqt36AhF4xHIbV%2FeID6%2FsKAd31bp9aHtdd5PsDmerK7sSgsWUosMlGiPPLs2q35hGQ5HEIZ6pmPdM7oOkVFDNS%2F7FFLKR3PHWTJQRitUc5ZwGjfFhdv7QKfZnYdPdWq%2BJ7Ij136soi%2F9pr%2BA4Gtw19rRjGx2zRgrCx6GHTHuYBJlz0DlMomkO1uEwpP1VHH2fvsZOenpiGyj532i7gdsZUcSBf%2B7%2F%2B0YC6%2BmJkkhm15Lv0KS03D9zgZNJlAln5ipuEQTYDNEXidnwAshHHhksw%2FCXTzqkCusEhOu3EwmcRPPEeFvjigsDW2u97TkD1Uu1dzxEo1RlYXYKDDnDOmzjYsUJt0iBg%2FZXVgMAjNO9ozD6kGfgnlg6V6PX8cFDBBz%2BcB%2B%2FeK81AbsRchfFOsSeNPihZV%2BrQ5Egs1dxCzpUZKV6Cp0QTMt4bO%2FXIigPBDudo5RHBTpfrE9bL5YVmTmfPDvhdOKvzljbNCmo6ymrCV0t7ldFH9%2Bi2Id6oj1dwxq93GtYNwrLvB0TqDqC4R%2Fg30uO4nmj0gNg0JG4gIENfUgMgzTR0RedbHz70tjMVP6gVQrAJNMRbnI687xbBWw58eb3efTT4K6EkeF4YI63z9gKN7lLpLpb9Cq9vgIiYP4SjR54CYwMBQeImnHymESbheyEi%2FsOiH6aBvOjrcbjKPcz%2FRwp9M%2FtaM94ugLJAl8TztfiRhd8hQR%2Fr3IgJfjbcgPCvhJnTmja9getYp6UMMCKAUDe%2BH%2FFv46KROympx3kMaNGgKcW2t7rjoEzT7q8Dvqc2%2Bjsuwmuj3qJlJO0lZAp5q5M%2FLyoxMHEPT4BFLkQE3ImNwMm4a93VeCc9GkoqYC1hQW42SC2FxTj68fhDKBksrolKPZeB%2F7Gd%2B5cAU3NFL4pKOOCR2CUb%2FhknF6oniTswKjoCgUfmJvV4DFpMZVBMTlCy%2BxA3HtUDYw7X9uiavLkSmMDrYlv7gOt39b%2Bq58VTjALqIpiaSrV2RuW8Pk%2FByK1uTkuW2JociJzChAcIj%2B23xvopHRJJ9Xk0ZKmfvsS%2Fvm6KXBpZBr1tZFJVwJE%2Fk8vSgy4pGnXNBknjQ6hzuiG5mrHEcDbxnHhlM4vR%2FrQLTYQ8%2BaHcR0Q%2BnzlpS7iXGMQMBLJy73EDLAEEizkG48R1ykRs0EaF2fAt4lw7bFs0UNfcB62eThKiBzDhr0xlTDGbjWQi9ZI%2F614bwpw79B8j0t6%2FLda29uz%2Fagx7JRfnUIRPOst9001gnakxiJfzHCTBMLt4sxLxyaMU4pks9r40xEHJcfJ8auEuFUjw4%2BnGswiyw3pagBfSG%2BO8sDpTp6ANxnEQfaTuCUelkeBzb3z%2Bisze0CNuASL3K%2BoDZ2u8WaoawIS8RN%2Fz0P%2Fc2ZwHGYbyyw1tUOSVIvhcUtnhFkSDdp%2BFx%2BsYG0img%2FmWft428%2B6PdLys%2FaTBxRZbVRb9R3r1CwSnkUhsbwe%2FrBimdL%2F8KivZXuFS5IIiSgiBRB0ZNCuOEXB6UPp2ljORswa%2FycStCuzH1cMqOoKo4IA2bp5AFWWJ7RTWQiyKmkaet%2FarlWPosgJA9Tl1yfqHJlwejCjGfzCebASNi%2Bqzk7pSrRSKG1PUY8q4DNphLQLnFwml5gdFBqJg%2BivgF6afaABIBCUcZdc4C19GPlCJY0FWYkUCFpClEoyS0C7CJXQ2O%2Bvwa8Jex22Uj8wjGk9zAyrQHcYeCC6aROU1iKUPfGadYf7ZJgv6jUKzloZxT%2F8f6Py%2FafHNAiBKqLCqzWtxEnaJiV7xmsVx3o9YvCCwV0EFJGKSKaQp6w56QIXJ1GIi%2FAzSHzsEwZz1GCmG6c0yC3P3%2BvUcpyaCJgFWivW2nqmJntR2fv2gg7mXVzq0MGSvRkwwAEnnZBxl10XrUsTR2LDCQuC6ET0QckCZj6ZroZgd4F76041O7EF5CBpC1hMer3HFeje5UHOr%2FQSI%2BnI8YWW4imIolUV32GCuBFwBcTTyhPaXUni6xLbQF3z3XiU3XKvKzxA%2BqwzfJK1KrToc1ISfyn4%2FCLmHv3SGMrAbSzFk3IomyjkPSYuIOegEbeZchGYgSGyBQcF5wr1CelGdRQDDTG1iVhcNzHcfkNXilThqaKcdZ2rxTpoQPNN67RHTDQGWrTWBmFZZWrr5WepQ%2FvO%2F6py5hmQvnnTS8F9Ia9d4B2ej3N97QDPR7xz0tMNvyeYN4j0zzByeKc%2BPM%2Fbx4M006gMQYmwtEJaNUdSVuzo6BdCz5qg1YLaXSQnP3WJOl50HwM8FTCIDZRT%2FfxgBBT5VcD8uTKo%2BLkGY8HdrkJWVBsgz%2F5o1gTfoICm8f0670ssMTjFowgTQcAxZm83H9uUZ6wg%2FZIM1skn9EyINrSaOfOJzpi7IzJMNvTIoqp93h4jwy8xWuEu0zQ5%2B03IL%2FrwndkDdia%2Fp8R5izPtFvLkmi5%2Beb1XgDZfGcxThwvK3PTPeMYqvbWAy%2B6st8MgxnhQPk0bCgPimJ1SYaJAQjOkMwpndSEvp4fpsEoj5xVJe92CunxUnI8%3D%7CN7xKW0lMyBwEaro6IrSeSw%3D%3D%7CR7OvhZYWpWdyn8NNeilHhw%3D%3D&multiDomain=&tos0=oath_freereg%7Cit%7Cit-IT&firstName=emanuele&lastName=ardinghi&userid-domain=yahoo&userId=dcfgvhb&yidDomainDefault=yahoo.com&yidDomain=yahoo.com&password=jJ%23NK%2Bee%26sMDE5C&birthYear=2000&signup="
        try:
            response = self.session.post(
                "https://login.yahoo.com/account/create",
                params=params,
                data=data,
            )
            if response.status_code != 200:
                print("error getting payload" + str(response.status_code))
                time.sleep(2)
                return self.payload()

            if "It looks like something went" in response.text:
                print("error getting session " + str(response.status_code))
                time.sleep(2)
                return self.payload()

            print("Successfull got session")
            # print(response.text)

        except Exception:
            print("error doing request")
            time.sleep(2)
            return self.payload()
