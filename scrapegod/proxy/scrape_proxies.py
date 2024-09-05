import requests
from bs4 import BeautifulSoup


# get the list of free proxies
def getProxies():
    r = requests.get("https://free-proxy-list.net/")
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find("tbody")
    proxies = []
    for row in table:
        if row.find_all("td")[4].text == "elite proxy":
            proxy = ":".join([row.find_all("td")[0].text, row.find_all("td")[1].text])
            proxies.append(proxy)
        else:
            pass
    return proxies


def write_to_file(filename, content):
    # Open the file in append mode. If it doesn't exist, it will be created.
    with open(filename, "a") as file:
        file.write(content + "\n")  # Append the content followed by a newline character


def extract(proxy):
    file_name = "free_proxy.txt"
    # this was for when we took a list into the function, without conc futures.
    # proxy = random.choice(proxylist)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0"
    }
    try:
        # change the url to https://httpbin.org/ip that doesnt block anything
        r = requests.get(
            "https://httpbin.org/ip",
            headers=headers,
            proxies={"http": proxy, "https": proxy},
            timeout=3,
        )
        if r.status_code == 200:
            write_to_file(filename=file_name, content=proxy)

    except requests.ConnectionError as err:
        print(repr(err))
    return proxy
