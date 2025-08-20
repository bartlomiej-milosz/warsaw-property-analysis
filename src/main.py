from .config import ScraperConfig
from .models import District, ResultLimit
from .scraper import PropertyScrapper
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    config = ScraperConfig([District.MOKOTOW], ResultLimit.SMALL)
    scraper = PropertyScrapper(config)
    results = scraper.get_listing_card_links(1)
    print(results)

if __name__ == "__main__":
    main()
