import logging
import time
import pandas as pd
import os
from typing import List
from .models.property import Property
from .scraper.property_scraper import PropertyScraper
from .scraper.search_params import PropertySearchQuery
from .models.types import District, PropertyType, ResultLimit

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

WARSAW_DISTRICTS: List[District] = list(District)
PROPERTY_TYPES: List[PropertyType] = list(PropertyType)
MAX_PROPERTIES: int = 500

def get_output_directory(property_type: PropertyType) -> str:
    """Get output directory based on property type"""
    base_dir = "./data/raw"
    
    if property_type == PropertyType.APARTMENT:
        return os.path.join(base_dir, "apartments")
    elif property_type == PropertyType.HOUSE:
        return os.path.join(base_dir, "houses")
    else:
        # Fallback for other property types
        return os.path.join(base_dir, property_type.name.lower())

def batch_scrape(
    district: District,
    property_type: PropertyType,
    limit: ResultLimit,
    max_properties: int,
):
    """Scrape one district-property type"""
    logger.info(f"Scraping {district.name} - {property_type.name}")
    
    try:
        config = PropertySearchQuery(
            locations=[district],
            property_type=property_type,
            limit=limit,
        )
        scraper = PropertyScraper(config=config)
        pages_needed: int = int((max_properties / limit.value) + 1)
        scraper.scrape_multiple_pages(pages_needed)

        properties: List[Property] = scraper.get_properties()[:max_properties]

        # Create directory structure based on property type
        output_dir = get_output_directory(property_type)
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{district.name.lower()}_{property_type.name.lower()}.csv"
        filepath = os.path.join(output_dir, filename)
        
        if properties:
            df = pd.DataFrame([prop.__dict__ for prop in properties])
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            logger.info(f"Saved {len(properties)} properties to {filepath}")
        else:
            logger.warning(f"No properties found for {district.name} - {property_type.name}")

        return properties

    except Exception as e:
        logger.error(f"Failed {district.name} - {property_type.name}: {e}")
        return []


def run():
    """Main scraping function"""
    logger.info("Starting property scraping...")
    
    total_scraped = 0
    
    for district in WARSAW_DISTRICTS:
        for property_type in PROPERTY_TYPES:
            properties = batch_scrape(
                district=district,
                property_type=property_type,
                limit=ResultLimit.XLARGE,
                max_properties=MAX_PROPERTIES,
            )
            total_scraped += len(properties)
            
            logger.info("Waiting 2 seconds before next scrape...")
            time.sleep(2)
    
    logger.info(f"Scraping completed! Total properties: {total_scraped}")
    logger.info("Check ./data/raw/apartments/ and ./data/raw/houses/ for results")


if __name__ == "__main__":
    run()
