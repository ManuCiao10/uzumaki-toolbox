from handler.utils import *
import requests



def dhlRedirect():
    url = "https://del.dhl.com/IT/9PzlE-pnRb"

    session = requests.Session()

    session.headers = {
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
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

    response = session.get(url)
    if "AWB=" not in response.url:
        print("error")
        return

    if response.status_code != 200:
        print("error")
        return
    
    import re
    regex = re.compile(r'javax.faces.ViewState" id="j_id1:javax.faces.ViewState:1" value="(.*)" autocomplete="off"')
    viewstate = regex.findall(response.text)[0]
    print(viewstate)

    data = {
    'redirectForm': 'redirectForm',
    'javax.faces.ViewState': viewstate,
    'redirectForm:redirectBtn': 'redirectForm:redirectBtn',
    'DELOPS': '',
    'QAR': '',
    'USRID': '',
    'src': '',
}

    response = session.post('https://del.dhl.com/prg/jsp/redirect_page.xhtml', data=data)
    print(response.url)
    print(response.status_code)
    print(response.text)

    time.sleep(2000)
    