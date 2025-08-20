from typing import List
import requests
import urllib
from bs4 import BeautifulSoup
from src.config import ScraperConfig
from src.models import District, ResultLimit


headers = {
    "User-Agent": "Mozilla/5.0 (compatible; PropertyScraper/1.0; Educational purpose)"
}


def get_listing_card_links(card_elements: List) -> List[str]:
    card_links: List[str] = []
    base: str = "https://www.otodom.pl"

    for anchor in card_elements:
        href = anchor.get("href")
        if href:
            full_url = urllib.parse.urljoin(base, href)
            card_links.append(full_url)
    return card_links


def get_listing_detail_prices(listing_card_links: List[str]) -> List[str]:
    prices: List[str] = []
    for url in listing_card_links:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
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
            prices.append(price_text)
            print(f"  Found price: {price_text}")
        else:
            print("No price found")
            prices.append("No price")
    return prices


def main():
    config = ScraperConfig([District.MOKOTOW], ResultLimit.SMALL)
    page: int = 1

    data_set = []
    while page <= 3:
        url: str = config.get_url(page=page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        listing_card_elements = soup.find_all("a", {"data-cy": "listing-item-link"})
        listing_card_links: List[str] = get_listing_card_links(listing_card_elements)

        prices = get_listing_detail_prices(listing_card_links)
        print(prices)
        data_set.append(prices)
        page += 1
    print(data_set)


if __name__ == "__main__":
    main()
