from handler.utils import *
import os
import psutil
from discord_webhook import DiscordWebhook
from discord_webhook import DiscordWebhook, DiscordEmbed


def processRunning():
    settings = load_settings()
    key = settings["key"]
    url_webhook = "WEBHOOK_HERE"

    if not key or key == "KEY HERE":
        print_task("please set key...", RED)
        input("Press Enter to exit...")
        os._exit(1)

    # add loopback-ip-address

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
                    webhook = DiscordWebhook(
                        url=url_webhook, username="Cracker Detected"
                    )

                    embed = DiscordEmbed(title="Cracker Detected", color="5865F2")
                    embed.set_thumbnail(url=LOGO)
                    embed.add_embed_field(name="Process", value=i, inline=False)
                    embed.add_embed_field(name="Key", value=key, inline=False)

                    webhook.add_embed(embed)
                    webhook.execute()
                    print_task("Cracker Detected...", RED)
                    input("Press Enter to exit...")
                    os._exit(1)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
