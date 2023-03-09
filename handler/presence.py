from pypresence import Presence
import time


def reachPresence(username):
    client_id = "1048021287584403627"

    try:
        RPC = Presence(client_id)
        RPC.connect()
    except:
        print("Discord not found")
        # time.sleep(2)

    start_time = time.time()

    try:
        RPC.update(
            details=username + " - V.0.0.25",
            large_image="logo",
            large_text="Uzumaki",
            start=start_time,
        )
    except:
        print("Discord not found")
        # time.sleep(2)
