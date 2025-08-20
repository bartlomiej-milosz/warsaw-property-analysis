import logging

from .scraper.property_scraper import PropertyScraper
from .scraper.search_params import PropertySearchQuery
from .models.types import District, ResultLimit

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    config = PropertySearchQuery(locations=[District.MOKOTOW], limit=ResultLimit.SMALL)
    scraper = PropertyScraper(config=config)
    scraper.scrape_multiple_pages(10)
    print(scraper.properties)

if __name__ == "__main__":
    main()
