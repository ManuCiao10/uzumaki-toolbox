from requests import post
from time import sleep

import json
import time
from handler.utils import load_settings, print_task, RED, WHITE
from random import choice


class Funcaptcha:
    try:
        settings = load_settings()
        key = settings["captcha_key"]
        print(key)

    except Exception as e:
        print_task("Error loading settings" + str(e), RED)
        time.sleep(2)
        exit()

    def getKey(proxy) -> str:
        proxy_selected = choice(proxy)
        payload = json.dumps(
            {
                "clientKey": Funcaptcha.key,
                "task": {
                    "type": "FunCaptchaTask",
                    "websitePublicKey": "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA",
                    "websiteURL": "https://signup.live.com/API/CreateAccount?lcid=1033&wa=wsignin1.0&rpsnv=13&ct=1667394016&rver=7.0.6737.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26signup%3d1%26RpsCsrfState%3d7f6d4048-5351-f65f-8b93-409ba7e7e4e4&id=292841&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=90015&lic=1&uaid=93bc3e1fb03c42568561df0711c6d450",
                    "funcaptchaApiJSSubdomain": "https://client-api.arkoselabs.com",
                    "proxy": proxy_selected,
                },
            }
        )
        req = post("https://api.capsolver.com/createTask", data=payload)
        status = ""
        while status == "" or status == "processing":
            sleep(0.3)
            task = post(
                "https://api.capsolver.com/getTaskResult",
                json={"clientKey": Funcaptcha.key, "taskId": req.json()["taskId"]},
            )
            status = task.json()["status"]
            if task.json()["status"] == "ready":
                return task.json()["solution"]["token"]
