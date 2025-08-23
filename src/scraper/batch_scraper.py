import logging
import pandas as pd
import os
from typing import List
from ..models.property import Property
from .property_scraper import PropertyScraper
from .search_params import PropertySearchQuery
from ..models.types import District, PropertyType, ResultLimit

logger = logging.getLogger(__name__)


class BatchScraper:
    """Handles batch scraping operations for multiple districts and property types"""

    def __init__(self, base_output_dir: str = "./data/raw"):
        self.base_output_dir = base_output_dir

    def get_output_directory(self, property_type: PropertyType) -> str:
        """Get output directory based on property type"""

        if property_type == PropertyType.APARTMENT:
            return os.path.join(self.base_output_dir, "apartments")
        elif property_type == PropertyType.HOUSE:
            return os.path.join(self.base_output_dir, "houses")
        else:
            # Fallback for other property types
            return os.path.join(self.base_output_dir, property_type.name.lower())

    def scrape_district_type(
        self,
        district: District,
        property_type: PropertyType,
        limit: ResultLimit,
        max_properties: int,
    ) -> int:
        """Scrape one district-property type combination"""

        logger.info(f"Scraping {district.name} - {property_type.name}")

        try:
            # Configure and run scraper
            config = PropertySearchQuery(
                locations=[district],
                property_type=property_type,
                limit=limit,
            )

            scraper = PropertyScraper(config=config)
            pages_needed: int = int((max_properties / limit.value) + 1)
            scraper.scrape_multiple_pages(pages_needed)

            properties: List[Property] = scraper.get_properties()[:max_properties]

            # Save results
            self._save_properties(properties, district, property_type)

            return len(properties)

        except Exception as e:
            logger.error(f"Failed {district.name} - {property_type.name}: {e}")
            return 0

    def _save_properties(
        self,
        properties: List[Property],
        district: District,
        property_type: PropertyType,
    ) -> None:
        """Save properties to CSV file"""

        # Create directory structure based on property type
        output_dir = self.get_output_directory(property_type)
        os.makedirs(output_dir, exist_ok=True)

        filename = f"{district.name.lower()}_{property_type.name.lower()}{"s"}.csv"
        filepath = os.path.join(output_dir, filename)

        if properties:
            df = pd.DataFrame([prop.__dict__ for prop in properties])
            df.to_csv(filepath, index=False, encoding="utf-8-sig")
            logger.info(f"Saved {len(properties)} properties to {filepath}")
        else:
            logger.warning(
                f"No properties found for {district.name} - {property_type.name}"
            )

    def scrape_multiple_combinations(
        self,
        districts: List[District],
        property_types: List[PropertyType],
        limit: ResultLimit,
        max_properties: int,
        delay_seconds: int = 2,
    ) -> int:
        """Scrape multiple district-property type combinations"""
        import time

        total_scraped = 0

        for district in districts:
            for property_type in property_types:
                count = self.scrape_district_type(
                    district=district,
                    property_type=property_type,
                    limit=limit,
                    max_properties=max_properties,
                )
                total_scraped += count

                # Add delay between scrapes (except for the last one)
                if not (
                    district == districts[-1] and property_type == property_types[-1]
                ):
                    logger.info(
                        f"Waiting {delay_seconds} seconds before next scrape..."
                    )
                    time.sleep(delay_seconds)

        return total_scraped
