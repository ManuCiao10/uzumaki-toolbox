import requests
import time
import json
from handler.utils import *

api_key = "***REMOVED***"

# Change of activation status

access_ready = 'ACCESS_READY'  # number readiness confirmed
access_ready_get = 'ACCESS_RETRY_GET'  # waiting for a new sms
access_activation = 'ACCESS_ACTIVATION'  # service successfully activated
access_cancel = 'ACCESS_CANCEL'  # activation canceled

# Get activation status:

status_wait = 'STATUS_WAIT_CODE'  # waiting for sms
status_wait_retry = "STATUS_WAIT_RETRY"  # waiting for code clarification
status_wait_resend = 'STATUS_WAIT_RESEND'  # waiting for re-sending SMS *
status_cancel = 'STATUS_CANCEL'  # activation canceled
status_ok = "STATUS_OK"  # code received

# Mistakes: (ERROR)

error_sql = 'ERROR_SQL'  # SQL-server error
no_activation = 'NO_ACTIVATION'  # activation id does not exist
bad_service = 'BAD_SERVICE'  # incorrect service name
bad_status = 'BAD_STATUS'  # incorrect status
bad_key = 'BAD_KEY'  # Invalid API key
bad_action = 'BAD_ACTION'  # incorrect action

status_ready = '1'
status_complete = '6'
status_ban = '8'


country = "0"
service = "mb"
operator = "any"
forward = '0'
ref = '2647315'

def getCode(id : str) -> str:
    print_task("Getting code...", WHITE)

    # Activation status
    time.sleep(2)
    ch_activation_status = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=setStatus&status=' + status_ready + '&id=' + id + '&forward=' + forward)
    
    time.sleep(20)
    if ch_activation_status.text in access_ready:
        print("number readiness confirmed\n")

        # SMS status
        time.sleep(3)
        get_sms = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=getStatus&id=' + id)
        code = get_sms.text

        while status_wait in code or status_ok in code or status_cancel in code or status_wait_resend in code or status_wait_retry in code:
            if code in status_wait:
                print("wait sometime for SMS")
                time.sleep(20)
                get_sms = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=getStatus&id=' + id)
                code = get_sms.text
                print("SMS status: ", code)
            elif status_ok in code:
                tex, m_code = code.split(':')
                print("Your SMS code: ", m_code)

                time.sleep(2)
                
                _ = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key='+api_key+'&action=setStatus&status='+status_complete+'&id='+id+'&forward='+forward)
                print("PVA complete")
                break
            else:
                ch_activation_status = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=setStatus&status=' + status_ban + '&id=' + id + '&forward=' + forward)
                print("Cancel the activation")
                print("sorry this number has some issues")
                exit()

    else:
        ch_activation_status = requests.get('https://sms-activate.ru/stubs/handler_api.php?api_key=' + api_key + '&action=setStatus&status=' + status_ban + '&id=' + id + '&forward=' + forward)
        print("Cancel the activation")
        print("sorry this number has some issues")
        time.sleep(20)
        exit()

    return m_code

def getPhone() -> str:
    print_task("Getting phone number...", WHITE)

    balance = requests.get(
        "https://sms-activate.ru/stubs/handler_api.php?api_key="
        + api_key
        + "&action=getBalance"
    )

    info = balance.text
    _, b2 = info.split(":")

    print_task(f"Balance: {b2}$", WHITE)

    # number of available phones
    find_numbers = requests.get(
        "https://sms-activate.ru/stubs/handler_api.php?api_key="
        + api_key
        + "&action=getNumbersStatus&country="
        + country
        + "&operator="
        + operator
    )

    try:
        num_numbers = json.loads(find_numbers.text)
    except json.decoder.JSONDecodeError:
        print_task("error loading json", RED)
        exit_program()
    except:
        print_task("unexpected error loading response", RED)
        exit_program()

    if num_numbers["go_0"] == "0":
        print_task("no number available", RED)
        exit_program()

    order_number = requests.get(
        "https://sms-activate.ru/stubs/handler_api.php?api_key="
        + api_key
        + "&action=getNumber&service="
        + service
        + "&forward="
        + forward
        + "&operator="
        + operator
        + "&ref="
        + ref
        + "&country="
        + country
    )

    info = order_number.text
    try:
        a, id, phone_number = info.split(":")
    except ValueError:
        print_task(f"error getting phone number {info}", RED)
        exit_program()
    
    print_task(f"Id: {id}", WHITE)
    print_task(f"Phone number: {phone_number}", WHITE)

    return id, phone_number



    
