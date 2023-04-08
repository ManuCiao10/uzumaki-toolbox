import requests


def getStoreData():
    print("Starting scraping data store...")

    headers = {
        "authority": "api.nike.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Brave";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    }

    params = {
        "language": "en-IT",
        "search": '(((brand==NIKE and facilityType==NIKE_OWNED_STORE or facilityType==FRANCHISEE_PARTNER_STORE or facilityType==MONO_BRAND_NON_FRANCHISEE_PARTNER_STORE and (region==ITALY)) and (businessConcept!=EMPLOYEE_STORE and businessConcept!=BRAND_POP_UP)) and (coordinates=geoProximity={"maxDistance": 500, "measurementUnits": "mi","latitude": 41.87, "longitude": 12.56}))',
    }

    params_romania = {
        "language": "de-DE",
        "search": '(((brand==NIKE and facilityType==NIKE_OWNED_STORE or facilityType==FRANCHISEE_PARTNER_STORE or facilityType==MONO_BRAND_NON_FRANCHISEE_PARTNER_STORE and (region!=GREATER_CHINA)) and (businessConcept!=EMPLOYEE_STORE and businessConcept!=BRAND_POP_UP)) and (coordinates=geoProximity={"maxDistance": 500, "measurementUnits": "mi","latitude": 45.94, "longitude": 24.96}))',
    }

    response = requests.get(
        "https://api.nike.com/store/store_locations/v1", params=params, headers=headers
    )

    response_romania = requests.get(
        "https://api.nike.com/store/store_locations/v1",
        params=params_romania,
        headers=headers,
    )

    for data in response_romania.json()["objects"]:
        id = data.get("id")  # get the id
        name = data.get("name")  # get the name
        address = data.get("address").get("address1")  # get the address
        address2 = data.get("address").get("address2")  # get the address2
        address3 = data.get("address").get("address3")  # get the address3
        city = data.get("address").get("city")  # get the city
        state = data.get("address").get("state")  # get the state
        postalCode = data.get("address").get("postalCode")  # get the postalCode
        country = data.get("address").get("country")  # get the country

        with open("romania.csv", "a") as f:
            # write headers if file is empty
            if f.tell() == 0:
                f.write(
                    "id,name,address,address2,address3,city,state,postalCode,country"
                    + "\n"
                )
            # write data
            if country == "ROU":
                f.write(
                    f"{id},{name},{address},{address2},{address3},{city},{state},{postalCode},{country}\n"
                )

    for data in response.json()["objects"]:

        id = data.get("id")  # get the id
        name = data.get("name")  # get the name
        address = data.get("address").get("address1")  # get the address
        address2 = data.get("address").get("address2")  # get the address2
        address3 = data.get("address").get("address3")  # get the address3
        city = data.get("address").get("city")  # get the city
        state = data.get("address").get("state")  # get the state
        postalCode = data.get("address").get("postalCode")  # get the postalCode
        country = data.get("address").get("country")  # get the country

        with open("nikestore.csv", "a") as f:
            # write headers if file is empty
            if f.tell() == 0:
                f.write(
                    "id,name,address,address2,address3,city,state,postalCode,country"
                    + "\n"
                )
            # write data
            if country == "ITA":
                f.write(
                    f"{id},{name},{address},{address2},{address3},{city},{state},{postalCode},{country}\n"
                )

    print("Finished scraping data store...")
