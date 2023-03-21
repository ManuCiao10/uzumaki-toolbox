from handler.utils import *
import os
import psutil
import socket
from discord_webhook import DiscordWebhook
from discord_webhook import DiscordWebhook, DiscordEmbed

import ipaddress


def is_loopback(ip):
    try:
        ip = ipaddress.ip_address(ip)
        if ip.is_loopback:
            return True
        else:
            return False
    except ValueError:
        return False


def webhook_cracked(i=None, key=None):
    url_webhook = "WEBHOOK_HERE"
    webhook = DiscordWebhook(url=url_webhook, username="Cracker Detected")

    embed = DiscordEmbed(title="Cracker Detected", color="5865F2")
    embed.add_embed_field(name="Process", value=i, inline=False)
    embed.add_embed_field(name="Key", value=key, inline=False)

    webhook.add_embed(embed)
    webhook.execute()
    print_task("Cracker Detected...", RED)
    exit_program()

def processRunning():
    settings = load_settings()
    key = settings["key"]

    if not key or key == "KEY HERE":
        print_task("please set key...", RED)
        exit_program()

    # get the current ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    if is_loopback(ip):
        webhook_cracked(i="Loopback", key=key)

    process_name = [
        "dnspy",
        "httpdebuggersvc",
        "fiddler",
        "charles",
        "wireshark",
        "dragonfly",
        "httpwatch",
        "burpsuite",
        "hxd",
        "http toolkit",
        "glasswire",
        "netlimiter",
    ]

    for proc in psutil.process_iter():
        try:
            for i in process_name:
                if i.lower() in proc.name().lower():
                    webhook_cracked(i=i, key=key)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
