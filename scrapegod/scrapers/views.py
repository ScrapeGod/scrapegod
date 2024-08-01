from flask import Blueprint, render_template, request, jsonify
from scrapegod.scrapers.amazon import scrap_amazon

scraper = Blueprint(
    "scraper", __name__, template_folder='templates', url_prefix="/"
)

@scraper.route("/amazon/scrape", methods=["POST", "GET"])
def scrape_news():
    data = request.json  # Get JSON data from request body
    url = data.get('url')  # Retrieve 'url' from the JSON data
    properties = data.get('properties')  # Retrieve 'properties' from the JSON data
    
    scraped_data = []
    if url:
        scraped_data = scrap_amazon(url)
    scraped_data = {
        "statusCode": 200,
        "result": scraped_data,  # Example result
        "html": "<html>Example HTML</html>"  # Example HTML
    }


    return jsonify(scraped_data)
