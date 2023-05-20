from handler.utils import *
from handler.webhook import send_webhook_sda


def sda(tracking_number):
    setTitleMode("tracker - sda")
    import requests
    import json

    print_task("[sda %s] getting session..." % tracking_number, PURPLE)

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
        "locale": "it",
        "tracing.letteraVettura": tracking_number,
    }
    session = requests.Session()
    invalid_tracking = "Dettagli spedizione"
    # try:
    response = session.get(
        "https://www.sda.it/wps/portal/Servizi_online/dettaglio-spedizione",
        params=params,
        headers=headers,
    )

    if invalid_tracking not in response.text:
        print_task(
            "[sda %s] error: %s"
            % (tracking_number, "invalid or unavailable tracking number..."),
            RED,
        )
        return

    if response.status_code == 200:
        print_task("[sda %s] successful got session..." % tracking_number, YELLOW)

        DigestTracker = response.cookies.get_dict()["DigestTracker"]
        sessionID = response.cookies.get_dict()["JSESSIONID"]

        cookies = {
            "DigestTracker": DigestTracker,
            "JSESSIONID": sessionID,
            "WASReqURL": "https:///wps/wcm/myconnect/sda/7c456830-d753-49e2-bd79-70c1176244ec/logo-crononline.png?MOD=AJPERES&CACHEID=ROOTWORKSPACE.Z18_6O5IG2G0OG6540QCGUATFF0000-7c456830-d753-49e2-bd79-70c1176244ec-n2-.at0",
        }

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://www.sda.it",
            "Pragma": "no-cache",
            "Referer": "https://www.sda.it/wps/portal/Servizi_online/dettaglio-spedizione?locale=it&tracing.letteraVettura=288044I077562",
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

        data = {
            "modalita": "01",
            "codiceRicercato": tracking_number,
            "campiRicercaVuoti": "false",
        }

        response = session.post(
            "https://www.sda.it/wps/portal/Servizi_online/dettaglio-spedizione/!ut/p/z1/jY_BCoJAEIafxRdopl1192pbgpJYB9PmIlvIYmway9bzJ9UpSJrLz8A3388AQQM06EdvtO_HQdtpP1LcFtlaLnOFZcm5wr2SKJjcIKYC6heAPyZBoH_uZwCa19dAXxVptZoMuzjn24xjGX2AGUcOZOx4er_LXKEKA-SdPveDWdjO-87pwxR3p6FhUmIYZihEFDO4XasGL5E1SRA8AT5YYHM!/p0/IZ7_MID81JC0OO33C0QC80728E0G81=CZ6_MID81JC0OO33C0QC80728E00F7=NJQCPricercaSpedizione.json=/",
            cookies=cookies,
            headers=headers,
            data=data,
        )
        try:
            json_data = json.loads(response.text)
        except:
            print_task(
                "[sda %s] error: %s" % (tracking_number, "error while parsing data..."),
                RED,
            )
            return

        print_task("[sda %s] successful got data..." % tracking_number, GREEN)

        try:
            something = json_data.get("lettereVettura")[0].get("dettaglioSpedizioni")[0]
        except:
            print_task(
                "[sda %s] error: %s" % (tracking_number, "error while parsing data..."),
                RED,
            )
            return

        date = something.get("dataOra")
        city = something.get("citta")
        status = something.get("statoLavorazione")

        send_webhook_sda(tracking_number, date, city, status)
