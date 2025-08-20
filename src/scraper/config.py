from typing import Dict


HEADERS: Dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (compatible; PropertyScraper/1.0; Educational purpose)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pl-PL,pl;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

PROPERTY_DETAILS = {
    "area": "Powierzchnia:",
    "rooms": "Liczba pokoi:",
    "heating": "Ogrzewanie:",
    "floor": "Piętro:",
    "maintenance_fee": "Czynsz:",
    "condition": "Stan wykończenia:",
    "market": "Rynek:",
    "ownership": "Forma własności:",
    "advertiser_type": "Typ ogłoszeniodawcy:",
}

BUILDING_DETAILS = {
    "year_built": "Rok budowy:",
    "elevator": "Winda:",
    "building_type": "Rodzaj zabudowy:",
    "windows": "Okna:",
    "security": "Bezpieczeństwo:",
}

ALL_DETAILS = {**PROPERTY_DETAILS, **BUILDING_DETAILS}
