from handler.utils import *



def get_gls_mails(user, password):
    try:
        # setup imap
        imap_url = "imap.gmail.com"
        with imaplib.IMAP4_SSL(imap_url) as my_mail:
            my_mail.login(user, password)
            my_mail.select("Inbox")

            key = "FROM"
            value = wise_mail
            _, data = my_mail.search(None, key, value)

            mail_id_list = data[0].split()  # IDs of all emails that we want to fetch

            msgs = []  # empty list to capture all messages
            # Iterate through messages and extract data into the msgs list
            for num in mail_id_list:
                typ, data = my_mail.fetch(
                    num, "(RFC822)"
                )  # RFC822 returns whole message (BODY fetches just body)
                msgs.append(data)

        

        # return raw_mail_text

    except Exception as e:
        print_task(str(e), RED)
        input("Press Enter to exit...")
        os._exit(1)

def glsRedirect(username):
    os.chdir("Uzumaki/gls")
    os.system("cls" if os.name == "nt" else "clear")

    print(RED + BANNER + RESET)

    print(f"{Fore.WHITE}WELCOME BACK: {Fore.RED}{username.upper()}{Style.RESET_ALL}\n")

    #read file
    #scrape email
    #redirect where is possible

    print_task("starting gls redirect...", PURPLE)

    # Get credentials from file
    try:
        with open("gls.json", "r") as f:
            credentials = json.load(f)

        if not validate(credentials):
            print_task("please fill credentials.json", RED)
            input("Press Enter to exit...")
            os._exit(1)

    except:
        print_task("error getting credentials", RED)
        input("Press Enter to exit...")
        os._exit(1)

    userGmail = credentials["userGmail"]
    passwordGmail = credentials["passwordGmail"]

    try:
        print_task("getting gls mails...", CYAN)
        gls_mails = get_gls_mails(userGmail, passwordGmail)
        print_task(f"gls mails: {len(gls_mails)}", GREEN)

    except Exception as e:
        print_task(f"error getting gls mails: {str(e)}", RED)
        input("Press Enter to exit...")
        os._exit(1)