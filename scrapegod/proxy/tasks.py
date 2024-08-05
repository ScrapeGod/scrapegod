import logging
from scrapegod.proxy.scrape_proxies import getProxies, extract
from scrapegod.app import create_celery_app
import random
import concurrent.futures

bill_flow_logger = logging.getLogger("bill_flow")

celery = create_celery_app()


@celery.task
def extract_free_proxies():

    proxylist = getProxies()
    #print(len(proxylist))

    #check them all with futures super quick
    # this will automatically write free proxies to free_proxies.txt
    with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(extract, proxylist)

extract_free_proxies()
