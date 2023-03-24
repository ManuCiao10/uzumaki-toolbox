from pypresence import Presence
from handler.utils import VERSION
import time


def reachPresence(username):
    client_id = "1048021287584403627"

    try:
        RPC = Presence(client_id)
        RPC.connect()
    except:
        print("Discord not found")

    start_time = time.time()

    try:
        RPC.update(
            details=f"{username} - v{VERSION}",
            large_image="logo",
            large_text="Uzumaki",
            start=start_time,
        )
    except:
        print("Discord not found")
