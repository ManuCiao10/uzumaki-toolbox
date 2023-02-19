from handler.utils import *


def gls(
    company,
    tracking_number,
    tkn,
    city,
    address,
    number_house,
    province,
    zip_code,
    name,
    surname,
    instructions,
):
    import requests

    version = tracking_number[0:2]
    number = tracking_number[2:]

    print_task("[gls %s] getting session..." % tracking_number, PURPLE)

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    params = {
        "option": "com_gls",
        "view": "svincola",
        "mode": "flexdelivery",
        "firstspirit": "5",
        "loc": version,
        "num": number,
        "tkn": "clljjkda",
    }

    # try:
    session = requests.Session()

    response = session.get(
        "https://gls-italy.com/index.php", params=params, headers=headers
    )

    text = "Enter a new delivery address"

    if response.status_code == 200:
        print_task("[gls %s] successful got session..." % tracking_number, GREEN)

        if text in response.text:
            STunn = session.cookies.get_dict()["STunn"]

            joomsef_lang = session.cookies.get_dict()["joomsef_lang"]
            cookies = {
                "STunn": STunn,
                # '0c73b3f6168197b4a0547b472c2dfd1f': 'bbp8kmt56vaifl7d0vhj3i0udj',
                "joomsef_lang": joomsef_lang,
                "browserLanguage": "en",
            }

            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Origin": "https://gls-italy.com",
                "Pragma": "no-cache",
                "Referer": "https://gls-italy.com/index.php?option=com_gls&view=svincola&mode=flexdelivery&firstspirit=5&loc="
                + version
                + "&num="
                + number
                + "&tkn=clljjkda",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Sec-GPC": "1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
            }

            data = {
                "option": "com_gls",
                "view": "svincola",
                "mode": "flexdelivery_nuovoindirizzo_compila",
                "loc": version,
                "num": number,
                "tkn": "clljjkda",
                "svinm": "",
                "postback": "",
                "svincolo_pre_post": "OKPRE",
            }

            response = session.post(
                "https://gls-italy.com/index.php?option=com_gls&amp;lang=it",
                cookies=cookies,
                headers=headers,
                data=data,
            )

            if "Choose a new address:" in response.text:
                print_task("[gls %s] filling new address..." % tracking_number, YELLOW)
                cookies = {
                    "0c73b3f6168197b4a0547b472c2dfd1f": "bbp8kmt56vaifl7d0vhj3i0udj",
                    "joomsef_lang": joomsef_lang,
                    "browserLanguage": "en",
                    "STunn": STunn,
                    "privacy_download": "1",
                }

                headers = {
                    "Accept": "*/*",
                    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Origin": "https://gls-italy.com",
                    "Pragma": "no-cache",
                    "Referer": "https://gls-italy.com/index.php?option=com_gls&amp;lang=it",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-GPC": "1",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                    "X-Requested-With": "XMLHttpRequest",
                    "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"macOS"',
                }
                separate = address.split(" ")
                via = separate[0]
                road = separate[1]
                # 'option=com_users&task=registration.getIndirizzo&format=raw&indirizzo=Via+Orcagna&cap=50121&localita=Firenze&provincia=FI&sede_principale=-T1&comune=Firenze&zona=**&flex=si'
                data = (
                    "com_users&task=registration.getIndirizzo&format=raw&indirizzo="
                    + via
                    + "+"
                    + road
                    + "&cap="
                    + zip_code
                    + "&localita="
                    + city
                    + "&provincia="
                    + province
                    + "&sede_principale=-T1&comune="
                    + city
                    + "&zona=**&flex=si"
                )
                # data = 'option=com_users&task=registration.getIndirizzo&format=raw&indirizzo=Via+Orcagna&cap=50121&localita=Firenze&provincia=FI&sede_principale=-T1&comune=Firenze&zona=**&flex=si'

                response = session.post(
                    "https://gls-italy.com/index.php",
                    cookies=cookies,
                    headers=headers,
                    data=data,
                )

                print(response.text)

                cookies = {
                    "0c73b3f6168197b4a0547b472c2dfd1f": "bbp8kmt56vaifl7d0vhj3i0udj",
                    "joomsef_lang": "it",
                    "browserLanguage": "en",
                    "5b7108f43b147774a7dd742a6bcdf08a": "3f33uuu02skdd9gq2rdc2h7u02",
                    "STunn": "BWZWIfABOgqMKFx5nrn2WQ$$",
                }

                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Origin": "https://gls-italy.com",
                    "Pragma": "no-cache",
                    "Referer": "https://gls-italy.com/index.php?option=com_gls&amp;lang=it",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-User": "?1",
                    "Sec-GPC": "1",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                    "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"macOS"',
                }

                data = "option=com_gls&view=svincola&mode=flexdelivery_conferma&loc=V1&num=630144423&tkn=clljjkda&backcontrollo=si&destinatario_nome=emanuela&destinatario_cognome=urrito&destinatario=emanuela+urrito&localita=Firenze&numero_civico=66&indirizzo_senza_civico=Via+Orcagna&indirizzo=Via+Orcagna+66&cap=50121&provincia=FI&istruzioni=&zona=**&comune=Firenze&gls_usersede=-T1&tiposvin=Nuovo+indirizzo&svinm=&postback=&svincolo_pre_post=OKPRE"

                response = requests.post(
                    "https://gls-italy.com/index.php?option=com_gls&amp;lang=it",
                    cookies=cookies,
                    headers=headers,
                    data=data,
                )

                print(response.text)
                success = "The dispositions have been sent to the proper depot."
                print(response.status_code)

    else:
        print_task("[gls %s] error: %s" % (tracking_number, response.status_code), RED)
        return

    # except Exception as e:
    #     print_task("[gls %s] error: %s" % (tracking_number, e), RED)
