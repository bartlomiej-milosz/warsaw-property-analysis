from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import requests
import urllib
from bs4 import BeautifulSoup
from .config import ScraperConfig
import logging

logger = logging.getLogger(__name__)

BASE_URL: str = "https://www.otodom.pl"
HEADERS: Dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (compatible; PropertyScraper/1.0; Educational purpose)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pl-PL,pl;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


@dataclass
class Property:
    link: str
    price: Optional[int] = None
    location: Optional[str] = None


class PropertyScrapper:
    def __init__(self, config: ScraperConfig):
        self.config: ScraperConfig = config
        self.properties: List[Property] = []
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def _extract_links(self, card_elements) -> List[str]:
        """Helper function for extracting href from given <a> element"""
        card_links: List[str] = []
        for listing_card in card_elements:
            href = listing_card.get("href")
            if href:
                full_url = urllib.parse.urljoin(BASE_URL, href)
                card_links.append(full_url)
        logger.info(f"Extracted {len(card_links)} valid links")
        return card_links

    def _get_listing_card_links(self, page: int = 1) -> List[str]:
        """Retrieves all property listing URLs from the specified page"""

        if page < 1:
            raise ValueError("Page must be 1 or greater")

        try:
            logger.info(f"Fetching page {page}")
            url: str = self.config.get_url(page=page)
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            listing_card_elements = soup.find_all("a", {"data-cy": "listing-item-link"})
            logger.info(f"Found {len(listing_card_elements)} listings")
            return self._extract_links(listing_card_elements)
        except requests.RequestException as e:
            logger.error(f"Error fetching page {page}: {e}")
            return []

    def _get_price(self, soup: BeautifulSoup) -> Optional[int]:
        """Extract price from listing detail page"""
        try:
            price_tag = soup.find(
                "strong",
                {
                    "data-cy": "adPageHeaderPrice",
                    "data-sentry-element": "Price",
                    "data-sentry-source-file": "AdPrice.tsx",
                },
            )

            if price_tag:
                price_text = price_tag.text.strip()
                price_numbers = "".join(filter(str.isdigit, price_text))
                return int(price_numbers) if price_numbers else None

            return None
        except Exception as e:
            logger.warning(f"Could not extract price: {e}")
            return None

    def _get_location(self, soup: BeautifulSoup) -> str:
        """Extract location from listing detail page"""
        try:
            location_tag = soup.find(
                "a",
                {
                    "data-sentry-element": "StyledLink",
                    "data-sentry-source-file": "MapLink.tsx",
                },
            )
            if location_tag:
                return location_tag.text
            return None
        except Exception as e:
            logger.warning(f"Could not extract location: {e}")
            return None

    def _extract_all_details(self, soup: BeautifulSoup) -> Dict[str, Any]:
        property_data: Dict[str, Any] = {}

        property_data["price"] = self._get_price(soup)
        property_data["location"] = self._get_location(soup)

        return property_data

    def scrape_single_page_details(self, page: int = 1) -> List[Property]:
        """Scrape one page and return properties"""

        page_properties: List[Property] = []
        listing_card_links: List[str] = self._get_listing_card_links(page=page)
        for detail_link in listing_card_links:
            try:
                logger.info(f"Scraping: {detail_link}")

                response = self.session.get(detail_link)
                soup = BeautifulSoup(response.content, "html.parser")

                property_data: Dict[str, Any] = self._extract_all_details(soup)

                property_obj = Property(
                    link=detail_link,
                    price=property_data.get("price"),
                    location=property_data.get("location"),
                )
                page_properties.append(property_obj)

                logger.info(f"Scraped: {property_obj}")
            except Exception as e:
                logger.error(f"Failed to scrape {detail_link}: {e}")
                continue
        return page_properties

    def scrape_multiple_pages(self, max_pages: int) -> None:
        """Scrape multiple pages"""
        logger.info(f"Starting scrape for {max_pages} pages")

        for page in range(1, max_pages + 1):
            logger.info(f"Processing page {page}/{max_pages}")

            page_properties: List[Property] = self.scrape_single_page_details(page)
            self.properties.extend(page_properties)

            logger.info(f"Page {page} done: {len(page_properties)} properties")

        logger.info(f"Finished! Total: {len(self.properties)} properties")
