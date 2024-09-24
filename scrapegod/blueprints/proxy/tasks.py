import logging
from scrapegod.blueprints.proxy.scrape_proxies import getProxies, extract
from scrapegod.app import create_celery_app

celery = create_celery_app()
proxy_logger = logging.getLogger("proxy")


@celery.task
def extract_free_proxies():
    proxylist = getProxies()
    for proxy in proxylist:
        extract(proxy)


# extract_free_proxies()
