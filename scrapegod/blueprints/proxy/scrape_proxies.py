from datetime import datetime
import pycountry
import requests
from bs4 import BeautifulSoup
from rapidfuzz import process
from lib.util_datetime import tzware_datetime
from scrapegod.blueprints.proxy.models import AnonymityEnum, FreeProxy, ProtocolEnum

countries = [country.name for country in pycountry.countries]


# get the list of free proxies
def getProxies():
    """
    The function `getProxies` scrapes a website for free proxy information and categorizes the proxies
    based on their protocol, anonymity level, country, IP address, and port number.
    :return: The `getProxies` function returns a list of dictionaries, where each dictionary represents
    a proxy server with the following keys: 'ip', 'port', 'country', 'anonymity', and 'protocol'.
    """
    r = requests.get("https://free-proxy-list.net/", timeout=20)
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find("tbody")
    proxies = []
    for row in table:
        tds = row.find_all("td")
        if tds[5].text == "yes":
            protocol = ProtocolEnum.HTTPS.value
        else:
            protocol = ProtocolEnum.HTTP.value

        anonymity = tds[4].text
        if "elite" in anonymity.lower():
            anonymity = AnonymityEnum.ELITE.value
        elif "anonymous" in anonymity.lower():
            anonymity = AnonymityEnum.ANONYMOUS.value
        elif "transparent" in anonymity.lower():
            anonymity = AnonymityEnum.TRANSPARENT.value

        country, _, _ = process.extractOne(tds[3].text, countries)
        proxies.append(
            {
                "ip": tds[0].text,
                "port": tds[1].text,
                "country": country,
                "anonymity": anonymity,
                "protocol": protocol,
            }
        )
    return proxies


def check_proxy(ip):
    """
    The function `check_proxy` checks the validity of a proxy IP address by sending a request to a test
    endpoint and measuring the response time.

    :param ip: The `check_proxy` function you provided is used to check if a given proxy IP is working
    properly by making a request to https://httpbin.org/ip with that proxy. If the response is received
    within 5 seconds, it returns the status code of the response and the time taken to receive the
    :return: The `check_proxy` function returns a tuple containing the status code of the HTTP response
    and the time taken for the request to complete if the request is successful. If the request times
    out (takes more than 5 seconds), it returns `None, None`.
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0"
    }

    # if response takes more than 5 seconds, it is considered a bad proxy and we do not save it

    try:
        t1 = datetime.now()
        r = requests.get(
            "https://httpbin.org/ip",
            headers=headers,
            proxies={"http": ip, "https": ip},
            timeout=5,
        )
        t2 = datetime.now()
        return r.status_code, t2 - t1
    except requests.exceptions.ReadTimeout:
        return None, None


def extract(proxy):
    """
    The function extracts proxy information, checks its status using a specified URL, and updates or
    saves the proxy details in a database based on the response.

    :param proxy: The `extract` function takes a `proxy` dictionary as input. The `proxy` dictionary is
    expected to have keys such as 'ip', 'port', 'country', 'anonymity', and 'protocol' containing
    information about a proxy server
    :return: The function `extract(proxy)` is returning the `proxy` object after performing some
    operations on it.
    """
    ip_port = proxy["ip"] + ":" + proxy["port"]
    try:
        # change the url to https://httpbin.org/ip that doesnt block anything

        status_code, reponse_time = check_proxy(ip_port)
        if status_code == 200:
            if proxy["ip"] in FreeProxy.query.filter_by(ip_address=proxy["ip"]).all():
                # update the last checked and response time
                free_proxy = FreeProxy.query.filter_by(ip_address=proxy["ip"]).first()
                free_proxy.response_time = reponse_time.microseconds
                free_proxy.last_checked = tzware_datetime()
                free_proxy.save()
            else:

                free_proxy = FreeProxy(
                    ip_address=proxy["ip"],
                    port=proxy["port"],
                    country=proxy["country"],
                    anonymity=proxy["anonymity"],
                    protocol=proxy["protocol"],
                    active=True,
                    response_time=reponse_time.microseconds,
                    last_checked=tzware_datetime(),
                )
                free_proxy.save()

    except requests.ConnectionError as err:
        print(repr(err))
    return proxy
