from .config import ScraperConfig
from .models import District, ResultLimit
from .scraper import PropertyScrapper
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    config = ScraperConfig(locations=[District.MOKOTOW, District.WILANOW], limit=ResultLimit.SMALL)
    scraper = PropertyScrapper(config=config)
    scraper.scrape_multiple_pages(2)
    print(scraper.properties)

if __name__ == "__main__":
    main()
