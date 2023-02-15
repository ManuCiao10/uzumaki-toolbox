from handler.utils import print_task, RED, load_settings
import time
import os


def auth():
    # checking key and settings webhook
    settings = load_settings()
    webhook = settings["webhook"]
    # key = settings["key"]

    # if key == "KEY HERE":
    #     print_task("key not set", RED)
    #     print_task("please set key", RED)
    #     exit()

    if webhook == "WEBHOOK HERE" or webhook == "":
        print_task("please set webhook...", RED)
        time.sleep(1)
        os._exit(1)
