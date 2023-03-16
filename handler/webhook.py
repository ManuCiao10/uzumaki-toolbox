from handler.utils import *
import requests
import json
from discord_webhook import DiscordWebhook, DiscordEmbed

UPS_LOGO = "https://media.discordapp.net/attachments/819084339992068110/1078449797121445920/ups-social-share-logo-removebg-preview.png"
DHL_LOGO = "https://media.discordapp.net/attachments/819084339992068110/1083557169905020929/pngwing.com.png"
BRT_LOGO = "https://cdn.discordapp.com/attachments/819084339992068110/1078000541155721329/BRT_logo_cropped.png"
SDA_LOGO = "https://media.discordapp.net/attachments/819084339992068110/1083558464946716672/italy-courier-sda-dhl-express-poste-italiane-png-favpng-2nGkExNKQDVAFX0NTSkdbkYRZ-removebg-preview.png"
GLS_LOGO = "https://media.discordapp.net/attachments/819084339992068110/1083595173352702093/GLS_Logo_2021.svg.png"
POSTE_NL_LOGO = "https://cdn.discordapp.com/attachments/819084339992068110/1084179730112188446/1200px-PostNL_logo.png"
CORREOS_LOGO = "https://cdn.discordapp.com/attachments/819084339992068110/1085322661854466141/Correos-Symbol.png"


def correos_webhook(
    tracking_number,
    type,
    quatity,
    date_delivery_sum,
    summaryText,
    extendedText,
    eventDate,
    eventTime,
):
    settings = load_settings()
    webhook = DiscordWebhook(
        url=settings["webhook"],
        rate_limit_retry=True,
        username="Uzumaki™",
        avatar_url=LOGO,
    )

    embed = DiscordEmbed(
        title=tracking_number,
        description="> " + extendedText,
        color=12298642,
        url=f"https://www.correos.es/es/es/herramientas/localizador/envios/detalle?tracking-number={tracking_number}",
    )

    embed.set_thumbnail(url=CORREOS_LOGO)

    embed.add_embed_field(name="Type", value=type, inline=True)
    embed.add_embed_field(name="Quantity", value=quatity, inline=True)
    embed.add_embed_field(name="Summary", value=summaryText, inline=True)
    embed.add_embed_field(name="Event Date", value=eventDate, inline=True)
    embed.add_embed_field(name="Event Time", value=eventTime, inline=True)
    embed.add_embed_field(name="Date Delivery", value=date_delivery_sum, inline=True)

    embed.set_footer(text="Powered by Uzumaki Tools", icon_url=LOGO)

    webhook.add_embed(embed)

    response = webhook.execute()
    if "<Response [405]>" in str(response):
        print_task(f"[correos {tracking_number}] error Webhook Incorrect", RED)
    else:
        print_task(f"[correos {tracking_number}] successfully sent webhook", GREEN)


def poste_webhook(
    tracking_number,
    zip_code,
    effectiveDate,
    sender,
    deliveryAddress,
    street,
    houseNumber,
    postalCode,
    town,
    country,
    status,
):
    settings = load_settings()
    webhook = DiscordWebhook(
        url=settings["webhook"],
        rate_limit_retry=True,
        username="Uzumaki™",
        avatar_url=LOGO,
    )

    embed = DiscordEmbed(
        title=tracking_number,
        description="> " + status.upper(),
        color=12298642,
        url=f"https://jouw.postnl.nl/track-and-trace/{tracking_number}-NL-{zip_code}",
    )

    embed.set_thumbnail(url=POSTE_NL_LOGO)

    embed.add_embed_field(name="Shipper", value=sender, inline=False)
    embed.add_embed_field(name="Date", value=effectiveDate, inline=False)
    embed.add_embed_field(
        name="Receiver", value="||" + deliveryAddress + "||", inline=True
    )

    embed.add_embed_field(name="Street", value="||" + street + "||", inline=True)
    embed.add_embed_field(
        name="House Number", value="||" + houseNumber + "||", inline=True
    )
    embed.add_embed_field(
        name="Postal Code", value="||" + postalCode + "||", inline=True
    )
    embed.add_embed_field(name="Town", value="||" + town + "||", inline=True)
    embed.add_embed_field(name="Country", value="||" + country + "||", inline=True)

    embed.set_footer(text="Powered by Uzumaki Tools", icon_url=LOGO)

    webhook.add_embed(embed)

    response = webhook.execute()
    if "<Response [405]>" in str(response):
        print_task(f"[poste {tracking_number}] error Webhook Incorrect", RED)
    else:
        print_task(f"[poste {tracking_number}] successfully sent webhook", GREEN)


def gls_webhook(
    tracking_number,
    shipper,
    receiver,
    status,
    location,
    date,
    time,
):
    settings = load_settings()
    webhook = settings["webhook"]

    data = {
        "username": "Uzumaki™",
        "avatar_url": LOGO,
        "content": " ",
        "embeds": [
            {
                "title": tracking_number,
                "url": f"https://gls-group.com/IT/it/servizi-online/ricerca-spedizioni.html?match={tracking_number}&type=NAT",
                "color": 12298642,
                "description": "> " + status,
                "footer": {"text": "by Uzumaki Tools", "icon_url": LOGO},
                "thumbnail": {"url": GLS_LOGO},
                "fields": [
                    {"name": "Shipper", "value": shipper, "inline": True},
                    {"name": "Receiver", "value": receiver, "inline": True},
                    {"name": "Location", "value": location, "inline": False},
                    {"name": "Date", "value": date, "inline": True},
                    {"name": "Time", "value": time, "inline": True},
                ],
            }
        ],
    }

    try:
        requests.post(
            webhook,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        print_task(f"[gls {tracking_number}] sent webhook", GREEN)
    except Exception as e:
        print_task(f"[gls {tracking_number}] {e}", RED)
        time.sleep(3)
        return


def dhl_webhook(
    tracking_number, service, origin, destination, status, text, weight, unit, location
):
    settings = load_settings()
    webhook = settings["webhook"]
    box = str(weight) + " " + str(unit)

    data = {
        "username": "Uzumaki™",
        "avatar_url": LOGO,
        "content": " ",
        "embeds": [
            {
                "title": tracking_number,
                "url": "https://www.dhl.com/en/express/tracking.html?AWB="
                + tracking_number,
                "color": 12298642,
                "description": "> " + text,
                "footer": {"text": "by Uzumaki Tools", "icon_url": LOGO},
                "thumbnail": {"url": DHL_LOGO},
                "fields": [
                    {"name": "Status", "value": status, "inline": True},
                    {"name": "Service", "value": service, "inline": True},
                    {"name": "Origin", "value": origin, "inline": True},
                    {"name": "Destination", "value": destination, "inline": True},
                    {"name": "Weight", "value": box, "inline": True},
                    {"name": "Location", "value": location, "inline": True},
                ],
            }
        ],
    }

    result = requests.post(
        webhook, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )
    try:
        result.raise_for_status()
        print_task(f"[dhl {tracking_number}] sent webhook", GREEN)
    except requests.exceptions.HTTPError as err:
        print(err)


def redirect_webhook_brt(
    company, tracking_number, name, phone, address, city, state, zip, url, email
):
    settings = load_settings()
    webhook = settings["webhook"]

    data = {
        "username": "Uzumaki™",
        "avatar_url": LOGO,
        "content": " ",
        "embeds": [
            {
                "title": tracking_number,
                "url": url,
                "color": 12298642,
                "thumbnail": {"url": BRT_LOGO},
                "description": "> Successfully redirect your parcel!",
                "footer": {"text": "by Uzumaki Tools", "icon_url": LOGO},
                "fields": [
                    {"name": "Company", "value": company.upper(), "inline": True},
                    {
                        "name": "Tracking Number",
                        "value": tracking_number,
                        "inline": False,
                    },
                    {"name": "Name", "value": "||" + name + "||", "inline": True},
                    {"name": "Phone", "value": "||" + phone + "||", "inline": True},
                    {"name": "Address", "value": "||" + address + "||", "inline": True},
                    {"name": "City", "value": "||" + city + "||", "inline": True},
                    {"name": "State", "value": "||" + state + "||", "inline": True},
                    {"name": "Zip", "value": "||" + zip + "||", "inline": True},
                    {"name": "Email", "value": "||" + email + "||", "inline": False},
                ],
            }
        ],
    }

    result = requests.post(
        webhook, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )
    try:
        result.raise_for_status()
        print_task(f"[brt {tracking_number}] successfully sent webhook", YELLOW)
    except requests.exceptions.HTTPError as err:
        print(err)


def checker_brt_discord(
    tracking,
    brt_tracking_response,
    redictable,
    zip_code,
    order_number,
):
    settings = load_settings()
    webhook = settings["webhook"]

    description = "> You can't redirect your parcel, pleease wait."

    if redictable == "Yes":
        description = "> You can redirect your parcel!"

    data = {
        "username": "Uzumaki™",
        "avatar_url": LOGO,
        "content": " ",
        "embeds": [
            {
                "title": order_number,
                "url": brt_tracking_response,
                "color": 12298642,
                "description": description,
                "thumbnail": {"url": BRT_LOGO},
                "footer": {"text": "by Uzumaki Tools", "icon_url": LOGO},
                "fields": [
                    {"name": "Company", "value": "BRT", "inline": True},
                    {
                        "name": "Tracking Number",
                        "value": "||" + tracking + "||",
                        "inline": False,
                    },
                    {
                        "name": "Zip Code",
                        "value": "||" + zip_code + "||",
                        "inline": True,
                    },
                    {"name": "Redirectable", "value": redictable, "inline": False},
                ],
            }
        ],
    }

    result = requests.post(
        webhook, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )
    try:
        result.raise_for_status()
        print_task(f"[brt {order_number}] successfully sent webhook", YELLOW)
    except requests.exceptions.HTTPError as err:
        print(err)


def send_webhook_sda(tracking_number, date, city, status):
    settings = load_settings()
    webhook = settings["webhook"]

    url = (
        "https://www.sda.it/wps/portal/Servizi_online/dettaglio-spedizione?locale=it&tracing.letteraVettura="
        + tracking_number
    )

    data = {
        "username": "Uzumaki™",
        "avatar_url": LOGO,
        "content": " ",
        "embeds": [
            {
                "title": "Tracking Number",
                "url": url,
                "color": 12298642,
                "thumbnail": {"url": SDA_LOGO},
                "footer": {"text": "Powered by Uzumaki Tools", "icon_url": LOGO},
                "fields": [
                    {"name": "Company", "value": "SDA", "inline": True},
                    {"name": "Date", "value": date, "inline": True},
                    {"name": "City", "value": city, "inline": False},
                    {"name": "Status", "value": status, "inline": True},
                ],
            }
        ],
    }

    result = requests.post(
        webhook, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)


def send_webhook_brt(company, tracking_number, date, time, location, status):
    settings = load_settings()
    webhook = settings["webhook"]

    url = (
        "https://www.mybrt.it/it/mybrt/my-parcels/search?lang=en&parcelNumber="
        + tracking_number
    )

    data = {
        "username": "Uzumaki™",
        "avatar_url": LOGO,
        "content": " ",
        "embeds": [
            {
                "title": "Tracking Number",
                "url": url,
                "color": 12298642,
                "thumbnail": {"url": BRT_LOGO},
                "footer": {"text": "Powered by Uzumaki Tools", "icon_url": LOGO},
                "fields": [
                    {"name": "Company", "value": company.upper(), "inline": True},
                    {"name": "Status", "value": status, "inline": True},
                    {"name": "Date", "value": date, "inline": True},
                    {"name": "Time", "value": time, "inline": True},
                    {"name": "Branch", "value": location, "inline": True},
                ],
            }
        ],
    }

    result = requests.post(
        webhook, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)


def send_webhook(dataInfo):
    settings = load_settings()
    webhook = settings["webhook"]

    url = (
        "https://www.ups.com/track?loc=en_IT&tracknum="
        + dataInfo["tracking_number"]
        + "&requester=ST/trackdetails"
    )

    data = {
        "username": "Uzumaki™",
        "avatar_url": LOGO,
        "content": " ",
        "embeds": [
            {
                "title": "Tracking Number",
                "url": url,
                "color": 12298642,
                "footer": {"text": "Powered by Uzumaki Tools", "icon_url": LOGO},
                "thumbnail": {"url": UPS_LOGO},
                "fields": [
                    {"name": "Company", "value": "UPS", "inline": True},
                    {
                        "name": "Tracking Number",
                        "value": dataInfo["tracking_number"],
                        "inline": True,
                    },
                    {
                        "name": "Status",
                        "value": dataInfo["package_status"],
                        "inline": True,
                    },
                    {
                        "name": "Date",
                        "value": dataInfo["delivered_date"],
                        "inline": True,
                    },
                    {
                        "name": "Time",
                        "value": dataInfo["time_stamp"],
                        "inline": True,
                    },
                    {
                        "name": "Branch",
                        "value": dataInfo["location"],
                        "inline": True,
                    },
                ],
            }
        ],
    }
    result = requests.post(
        webhook,
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    try:
        result.raise_for_status()
        print_task(
            f"[ups {dataInfo['tracking_number']}] successfully sent webhook", GREEN
        )
    except requests.exceptions.HTTPError as err:
        print_task(f"[ups {dataInfo['tracking_number']}] error sending webhook", RED)


def webhook_nike(
    price: str,
    name: str,
    url_image: str,
    size: str,
    lineItemStatus: str,
    address: str,
    city: str,
    country: str,
    zip: str,
    tracklink: str,
    tracking_number: str,
    email: str,
):
    settings = load_settings()

    webhook = DiscordWebhook(
        url=settings["webhook"],
        rate_limit_retry=True,
        username="Uzumaki™",
        avatar_url=LOGO,
    )

    embed = DiscordEmbed(
        title="Tracking Number",
        description="> " + lineItemStatus.upper(),
        color=12298642,
        url=tracklink,
    )

    embed.set_thumbnail(url=url_image)

    embed.add_embed_field(name="Name", value=name, inline=False)
    embed.add_embed_field(name="Price", value=price + "€", inline=True)
    embed.add_embed_field(name="Size", value=size, inline=True)
    embed.add_embed_field(name="Address", value="||" + address + "||", inline=False)
    embed.add_embed_field(name="City", value="||" + city + "||", inline=True)
    embed.add_embed_field(name="Country", value="||" + country + "||", inline=True)
    embed.add_embed_field(name="Zip", value="||" + zip + "||", inline=True)
    embed.add_embed_field(
        name="Order Number", value="||" + tracking_number + "||", inline=True
    )
    embed.add_embed_field(name="Email", value="||" + email + "||", inline=False)

    embed.set_footer(text="Powered by Uzumaki Tools", icon_url=LOGO)

    webhook.add_embed(embed)

    response = webhook.execute()
    if "<Response [405]>" in str(response):
        print_task(f"[nike {tracking_number}] error Webhook Incorrect", RED)
    else:
        print_task(f"[nike {tracking_number}] successfully sent webhook", GREEN)


def webhook_newBalance(
    orderNumber,
    date,
    style,
    price,
    image,
    title,
    email,
    firstName,
    secondName,
    addy,
    zipCode,
    status,
    trackingLink,
):
    settings = load_settings()
    webhook = DiscordWebhook(
        url=settings["webhook"],
        rate_limit_retry=True,
        username="Uzumaki™",
        avatar_url=LOGO,
    )

    embed = DiscordEmbed(
        title=title,
        description="> " + status.upper(),
        color=12298642,
        url=trackingLink,
    )

    embed.set_thumbnail(url=image)

    embed.add_embed_field(name="Date", value=date, inline=True)
    embed.add_embed_field(name="Price", value=price, inline=True)
    embed.add_embed_field(name="Style", value=style, inline=True)
    embed.add_embed_field(
        name="Order Number", value="||" + orderNumber + "||", inline=False
    )
    embed.add_embed_field(name="Email", value="||" + email + "||", inline=False)
    embed.add_embed_field(name="First Name", value="||" + firstName + "||", inline=True)
    embed.add_embed_field(
        name="Second Name", value="||" + secondName + "||", inline=True
    )
    embed.add_embed_field(name="Address", value="||" + addy + "||", inline=True)
    embed.add_embed_field(name="Zip Code", value="||" + zipCode + "||", inline=True)

    embed.set_footer(text="Powered by Uzumaki Tools", icon_url=LOGO)

    webhook.add_embed(embed)

    response = webhook.execute()
    if "<Response [405]>" in str(response):
        print_task(f"[newBalance {orderNumber}] error Webhook Incorrect", RED)
    else:
        print_task(f"[newBalance {orderNumber}] successfully sent webhook", GREEN)


def webhook_courir(
    email,
    zipCode,
    title,
    orderNumber,
    image,
    orderedAt,
    expectedDelivery,
    status,
    trackingLink,
    trackingNumber,
    carrierCode,
):
    settings = load_settings()
    webhook = DiscordWebhook(
        url=settings["webhook"],
        rate_limit_retry=True,
        username="Uzumaki™",
        avatar_url=LOGO,
    )

    embed = DiscordEmbed(
        title=title,
        description="> " + status.upper(),
        color=12298642,
        url=trackingLink,
    )

    embed.set_thumbnail(url=image)

    embed.add_embed_field(
        name="Order Number", value="||" + orderNumber + "||", inline=False
    )
    embed.add_embed_field(name="Email", value="||" + email + "||", inline=False)
    embed.add_embed_field(
        name="Tracking Number", value="||" + trackingNumber + "||", inline=False
    )
    embed.add_embed_field(name="Zip Code", value="||" + zipCode + "||", inline=False)
    embed.add_embed_field(name="Carrier Code", value=carrierCode, inline=True)
    embed.add_embed_field(name="Ordered At", value=orderedAt, inline=True)
    embed.add_embed_field(
        name="Expected Delivery", value=expectedDelivery, inline=False
    )

    embed.set_footer(text="Powered by Uzumaki Tools", icon_url=LOGO)

    webhook.add_embed(embed)

    response = webhook.execute()
    if "<Response [405]>" in str(response):
        print_task(f"[courir {email}] error Webhook Incorrect", RED)
    else:
        print_task(f"[courir {email}] successfully sent webhook", GREEN)
