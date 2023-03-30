from execjs import compile
import requests


class Crypto:
    url = "https://raw.githubusercontent.com/ManuCiao10/uzumaki-update/main/enc.js"

    script = compile(requests.get(url).text)

    def encrypt(password: str, randomNum: str, Key: str) -> str:
        return Crypto.script.call("encrypt", password, randomNum, Key)
