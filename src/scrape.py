import logging
from typing import List
from .scraper.batch_scraper import BatchScraper  # New module
from .models.types import District, PropertyType, ResultLimit

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

WARSAW_DISTRICTS: List[District] = list(District)
PROPERTY_TYPES: List[PropertyType] = list(PropertyType)
MAX_PROPERTIES: int = 500


def run():
    """Main scraping function - orchestrates the entire scraping process"""
    logger.info("Starting property scraping...")

    batch_scraper = BatchScraper()

    total_scraped = batch_scraper.scrape_multiple_combinations(
        districts=WARSAW_DISTRICTS,
        property_types=PROPERTY_TYPES,
        limit=ResultLimit.XLARGE,
        max_properties=MAX_PROPERTIES,
        delay_seconds=2,  # Add delay parameter
    )

    logger.info(f"Scraping completed! Total properties: {total_scraped}")
    logger.info("Check ./data/raw/apartments/ and ./data/raw/houses/ for results")


if __name__ == "__main__":
    run()
