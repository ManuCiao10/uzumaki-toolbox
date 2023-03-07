from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from handler.utils import *
from twilio.twiml.voice_response import VoiceResponse


def ups(username):
    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

    print(
            f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n"
        )
    
    account_sid = "***REMOVED***"
    ups_number = "+390230303039"
    manuel = "+393662299421"

    auth_token  = "351727e4a71c83b2c28cfcf42690566c"
    print_task("getting session", PURPLE)
    
    try:    
        client = Client(account_sid, auth_token)
        call = client.calls.create(
            from_="+15673392063",
            to=ups_number,
            url="https://handler.twilio.com/twiml/EHfbef825852f2e3c2a682522ca467cf64",
            record=True,
        )
        
    except TwilioRestException as err:
        print_task("error getting session", RED)
        input("Press Enter to exit...")
        return

    print_task("call registered", GREEN)
    print_task("call id: " + call.sid, GREEN)




