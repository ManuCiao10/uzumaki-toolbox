from handler.utils import print_task, CYAN, RED, GREEN, PURPLE
from handler.webhook import redirect_webhook_brt
import os
import time
import requests
from bs4 import BeautifulSoup




def brt(company, tracking_number, OrderZip, name, phone, address, city, state, zip, email):

    #if tracking_number first 2 digit is 05
    # if tracking_number[:2] != "05":
    #     brt_tarcking_redirect(company, tracking_number, OrderZip, name, phone, address, city, state, zip, email)

    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

    params = {
    'docmit': tracking_number,
    'ksu': '1664282',
    'lang': 'en',
}

    try :
        session = requests.Session()
        # http = "185.91.206.181:6871:hgj3x3cas2:0ef2uixpcu"
        # ip = http.split(":")[0]
        # port = http.split(":")[1]
        # username = http.split(":")[2]
        # password = http.split(":")[3]

        # proxies = {
        #     "http": "http://%s:%s@%s:%s" % (username, password, ip, port),
        #     "https": "http://%s:%s@%s:%s" % (username, password, ip, port),
        # }

        # session.proxies = proxies

        response = session.get('https://vas.brt.it/vas/sped_ricdocmit_load.hsm', params=params, headers=headers)
        
        if "Shipment not found." in response.text:
            print_task("[brt %s] %s" % (tracking_number, "Shipment not found"), RED)
            time.sleep(2)
            os._exit(1)

        url = "https://vas.brt.it/vas/sped_ricdocmit_load.hsm?docmit=%s&ksu=1664282&lang=en" % tracking_number
        
        if "dettaglio della spedizione" in response.text.lower():
            spedizione = ""
            print_task("[brt %s] %s" % (tracking_number, "Redirecting package"), GREEN)

            if "N. spedizione" in response.text:
                soup = BeautifulSoup(response.text, 'html.parser')

                for table in soup.find_all('table', class_="table_dati_spedizione"):
                    for td in table.find_all('td'):
                        if td.text[:3] == "166":
                            spedizione = td.text
                            break

                if spedizione == "":
                    print_task("[brt %s] %s" % (tracking_number, "Redirect not available"), RED)
                    time.sleep(2)
                    os._exit(1)

                headers = {
                    'authority': 'www.mybrt.it',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                    'cache-control': 'no-cache',
                    'pragma': 'no-cache',
                    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"macOS"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'cross-site',
                    'sec-fetch-user': '?1',
                    'sec-gpc': '1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                }

                params = {
                    'lang': 'it',
                    'parcelNumber': '23' + spedizione,
                }
                
                try:
                    response = session.get('https://www.mybrt.it/it/mybrt/my-parcels/search', params=params, headers=headers)
                    
                    if "Protezione dei dati":
                        print_task("[brt %s] %s" % (tracking_number, "Filling the form"), PURPLE)

                    soup = BeautifulSoup(response.text, 'html.parser')
                    csrf = soup.find('meta', attrs={'name': '_csrf'})['content']

                    headers = {
                        'authority': 'www.mybrt.it',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                        'cache-control': 'no-cache',
                        'origin': 'https://www.mybrt.it',
                        'pragma': 'no-cache',
                        'referer': 'https://www.mybrt.it/it/mybrt/my-parcels/search?lang=it&parcelNumber=' + '23' + spedizione,
                        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"macOS"',
                        'sec-fetch-dest': 'document',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'same-origin',
                        'sec-fetch-user': '?1',
                        'sec-gpc': '1',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                    }

                    data = {
                        '_csrf': csrf,
                        'verificationCode': OrderZip,
                        'recaptchaResponse': '',
                        'number': '23' + spedizione,
                        'shipmentType': 'PARCEL_DETAILS',
                        'sourceUrl': '',
                        'validate': 'Conferma',
                    }

                    response = session.post('https://www.mybrt.it/it/mybrt/my-parcels/search/protection', headers=headers, data=data)

                    if "Il CAP inserito non corrisponde alla spedizione" in response.text:
                        print_task("[brt %s] %s" % (tracking_number, "Wrong ZipCode"), RED)
                        time.sleep(2)
                        return
                    
                    if "della richiesta si è verificato un problema tecnico." in response.text:
                        print_task("[brt %s] %s" % (tracking_number, "problema tecnico."), RED)
                        time.sleep(2)
                        return
                    
                    if "CAPTCHA mancante o non valido, si prega di riprovare." in response.text:
                        print_task("[brt %s] %s" % (tracking_number, "CAPTCHA hit."), RED)
                        time.sleep(2)
                        return
                    
                    brt_number = response.url.split("parcelNumber=")[1]
                    brt_tracking_response = response.url

                    headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Origin': 'https://vas.brt.it',
                        'Pragma': 'no-cache',
                        'Referer': 'https://vas.brt.it/vas/sped_det_show.htm',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-User': '?1',
                        'Sec-GPC': '1',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"macOS"',
                    }

                    data = {
                        'refererBolla': 'sped_det_show.htm',
                        'referer': 'sped_numspe_par.htm',
                        'reqid': '',
                        'pagina': '',
                        'ksu': '',
                        'annoSpedizione': '2023',
                        'nSpediz': spedizione,
                        'brtCode': brt_number,
                        'BRTCODE': brt_number,
                    }
                    session2 = requests.Session() 
                    response = session2.post('https://vas.brt.it/vas/istruzioni_consegna_form.htm', headers=headers, data=data)

                    if "Referente consegna" in response.text:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        dateValue = soup.find("input", {"name": "dataConsegna"})['value']
                        #<input name="desLoc" type="hidden" value="MERCATO S SEVERINO" />
                        locationValue = soup.find("input", {"name": "desLoc"})['value']
                        #<input name="desProv" type="hidden" value="SA" />
                        provValue = soup.find("input", {"name": "desProv"})['value']

                        #<input name="email" type="hidden" id="inputEmail" value="carlottasessa@hotmail.it" />
                        emailValue = soup.find("input", {"name": "email"})['value']
                        
                        time.sleep(2)

                        bigGipServer = response.cookies.get_dict()['BIGipServerAS777-Pool']

                        TS01ef7a66 = response.cookies.get_dict()['TS01ef7a66']

                        cookies = {
                            'BIGipServerAS777-Pool': bigGipServer,
                            'iduser': '',
                            'lstaut': '0000000000100',
                            'usrname': '',
                            'ksu': '',
                            'lang': 'en',
                            'TS01ef7a66': TS01ef7a66,
                        }

                        headers = {
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                            'Cache-Control': 'no-cache',
                            'Connection': 'keep-alive',
                            'Origin': 'https://vas.brt.it',
                            'Pragma': 'no-cache',
                            'Referer': 'https://vas.brt.it/vas/istruzioni_consegna_form.htm',
                            'Sec-Fetch-Dest': 'document',
                            'Sec-Fetch-Mode': 'navigate',
                            'Sec-Fetch-Site': 'same-origin',
                            'Sec-Fetch-User': '?1',
                            'Sec-GPC': '1',
                            'Upgrade-Insecure-Requests': '1',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"macOS"',
                        }
                        client_timestamp = int(time.time() * 1000)
                        new_state = state.upper()

                        data = {
                            'newReferenteConsegna': name,
                            'newTelefonoFisso': phone,
                            'newEmail': email,
                            'newCellulare': '',
                            'tipoIstruzione': '3',
                            'newDataConsegna': dateValue,
                            'newOraConsegna': '',
                            'newNominativo1Consegna': name,
                            'newNominativo2Consegna': '',
                            'newIndirizzoConsegna': address,
                            'newCapConsegna': zip,
                            'newLocalitaConsegna': city,
                            'newProvinciaConsegna': new_state,
                            'newDataConsegnaNewInd': '',
                            'newOraConsegnaNewInd': '',
                            'altre': '',
                            'inputConferma': 'Confirm',
                            'annoSpedizione': '2023',
                            'nSpediz': spedizione,
                            'brtCode': brt_number,
                            'clientTimeStamp': client_timestamp,
                            'referenteConsegna': '',
                            'telefonoFisso': '',
                            'email': emailValue,
                            'cellulare': '',
                            'destinat': '',
                            'destinat2': '',
                            'desIndir': '',
                            'desCap': '',
                            'desLoc': locationValue,
                            'desProv': provValue,
                            'dataConsegna': dateValue,
                            'oraConsegna': '',
                            'urlReferer': 'istruzioni_consegna_form.htm',
                            'refererBolla': 'sped_det_show.htm',
                            'referer': 'sped_numspe_par.htm',
                            'reqid': '',
                            'pagina': '',
                            'newPudoId': '',
                            'oldPudoId': '',
                            'pudoData': '',
                    }

                        response = session2.post('https://vas.brt.it/vas/istruzioni_consegna_conferma.htm', cookies=cookies, headers=headers, data=data)
                        
                        if "request submitted successfully" in response.text.lower():
                            print_task("[brt %s] %s" % (tracking_number, "Successfull redirect"), GREEN)
                            redirect_webhook_brt(company, brt_number, OrderZip, name, phone, address, city, state, zip, brt_tracking_response, email)
                            time.sleep(2)
                            return
                        if "ti confermiamo di aver preso in carico la tua richiesta del" in response.text.lower():
                            print_task("[brt %s] %s" % (tracking_number, "Successfull redirect"), GREEN)
                            redirect_webhook_brt(company, brt_number, OrderZip, name, phone, address, city, state, zip, brt_tracking_response, email)
                            time.sleep(2)
                            return
                        
                        else:
                            print_task("[brt %s] %s" % (tracking_number, "Failed redirect"), RED)
                            time.sleep(3)
                            return
                            
                    else:
                        print_task("[brt %s] %s" % (tracking_number, "No Redirect Found"), RED)
                        time.sleep(3)
                        return
                  
                except requests.exceptions.ConnectionError or requests.exceptions.ReadTimeout:
                    print_task("[brt %s] %s" % (tracking_number, "Connection Error"), RED)
                    time.sleep(2)
                    return
                
    except requests.exceptions.ConnectionError:
        print_task("[brt %s] %s" % (tracking_number, "Connection Error"), RED)
        

def ups(company, tracking_number, OrderZip, name, phone, address, city, state, zip, email):
    
    headers = {
    'authority': 'www.ups.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
}

    params = {
    'loc': 'it_IT',
    'tracknum': '1Z30R0336869572495',
    'requester': 'ST/trackdetails/trackdetails',
}
    session = requests.Session()
    response = session.get('https://www.ups.com/track', params=params, headers=headers)

    xxsrfoken = response.cookies.get_dict()['X-XSRF-TOKEN-ST']

    headers = {
    'authority': 'www.ups.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.ups.com',
    'pragma': 'no-cache',
    'referer': 'https://www.ups.com/track?loc=it_IT&tracknum=1Z30R0336869572495&requester=ST%2Ftracksummary%2Ftrackdetails',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Brave";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'x-xsrf-token': xxsrfoken,
}

    params = {
        'loc': 'it_IT',
    }

    json_data = {
        'Locale': 'it_IT',
        'TrackNumberType': 'TRACK_NUM_TYPE_INFO_NOTICE',
        'TrackingNumber': [
            'ayload''true',
        ],
    }

    response = session.post(
    'https://www.ups.com/track/api/Track/GetStatus',
    params=params,
    headers=headers,
    json=json_data,
)
    print(response.text)




def redirectHandler(company, tracking_number, OrderZip, name, phone, address, city, state, zip, email):
    if company == "brt":
        brt(company, tracking_number, OrderZip, name, phone, address, city, state, zip, email)
    elif company == "ups":
        ups(company, tracking_number, OrderZip, name, phone, address, city, state, zip, email)
    else:
        print_task("Company not supported", RED)
        time.sleep(3)
        os._exit(1)

def redirect():
    import csv
    import threading

    print_task("starting redirect.csv...", CYAN)

    try:
        with open("Uzumaki/redirect/redirect.csv", "r") as f:
            reader = csv.reader(f)

            try:
                next(reader)
            except StopIteration:
                print_task("file is empty", RED)
                time.sleep(2)
                os._exit(1)

            try:
                row = next(reader)
            except StopIteration:
                print_task("Please Fill Uzumaki/redirect/redirect.csv", RED)
                time.sleep(2)
                os._exit(1)

            f.seek(0)
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                company = row[0].lower().strip()
                tracking_number = row[1].lower().strip()
                OrderZip = row[2].lower().strip()
                name = row[3].lower().strip()
                phone = row[4].lower().strip()
                address = row[5].lower().strip()
                city = row[6].lower().strip()
                state = row[7].lower().strip()
                zip = row[8].lower().strip()
                email = row[9].lower().strip()

                threading.Thread(target=redirectHandler, args=(
                    company, tracking_number, OrderZip, name, phone, address, city, state, zip, email)).start()
                
    except FileNotFoundError:
        print_task("Uzumaki/redirect/redirect.csv not found", RED)
        time.sleep(2)
        os._exit(1)
