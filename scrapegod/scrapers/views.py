from flask import Blueprint, render_template, request
from scrapegod.scrapers.amazon import scrap_amazon

scraper = Blueprint(
    "scraper", __name__, template_folder='templates', url_prefix="/"
)

@scraper.route("/", methods=["GET"])
def scrape_news():
    url = request.args.get('url')
    scraped_data = []
    if url:
        scraped_data = scrap_amazon(url)

    return render_template(
        "index.html", scraped_data=scraped_data
    )
