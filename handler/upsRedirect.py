from pyVoIP.VoIP import VoIPPhone, InvalidStateError, CallState
import time
import wave
from handler.utils import *


def answer(call):
    try:
        f = wave.open("announcment.wav", "rb")
        frames = f.getnframes()
        data = f.readframes(frames)
        f.close()

        call.answer()
        call.write_audio(
            data
        )  # This writes the audio data to the transmit buffer, this must be bytes.

        stop = time.time() + (
            frames / 8000
        )  # frames/8000 is the length of the audio in seconds. 8000 is the hertz of PCMU.

        while time.time() <= stop and call.state == CallState.ANSWERED:
            time.sleep(0.1)
        call.hangup()
    except InvalidStateError:
        pass
    except:
        print_task("Failed to initiate the session", RED)
        call.hangup()


def ups(username):
    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    username = "5406532021"
    password = "Es9P8t2Z"
    myIP = ""
    domain = "sip.messagenet.it"
    port = 5061

    phone = VoIPPhone(
        server=domain,
        port=port,
        username=username,
        password=password,
        myIP=myIP,
        callCallback=answer,
    )

    phone.start()
    input("Press enter to exit...")
    phone.stop()
    return
