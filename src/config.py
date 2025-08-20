import urllib.parse
from dataclasses import dataclass
from typing import List, Literal, Optional
from src.models import District, ResultLimit


@dataclass
class ScraperConfig:
    locations: List[District]
    property_type: Literal["dom", "mieszkanie"] = "mieszkanie"
    listing_type: Literal["sprzedaz", "wynajem"] = "sprzedaz"
    limit: ResultLimit = ResultLimit.MEDIUM
    price_min: Optional[int] = None
    price_max: Optional[int] = None
    direction: Optional[Literal["DESC", "ASC"]] = None

    def get_url(self, page: int = 1) -> str:
        if len(self.locations) == 1:
            district = self.locations[0].value
            base_url = f"https://www.otodom.pl/pl/wyniki/{self.listing_type}/{self.property_type}/{district}"
            params = []
            params.append(f"limit={self.limit.value}")
            params.append("ownerTypeSingleSelect=ALL")
            params.append("by=DEFAULT")
            params.append("direction=DESC")
        else:
            base_url = f"https://www.otodom.pl/pl/wyniki/{self.listing_type}/{self.property_type}/wiele-lokalizacji"
            locations_list = [district.value for district in self.locations]
            locations_string = "[" + ",".join(locations_list) + "]"
            locations_encoded = urllib.parse.quote(locations_string)
            params = []
            params.append(f"limit={self.limit.value}")
            params.append("ownerTypeSingleSelect=ALL")
            params.append(f"locations={locations_encoded}")
            params.append("by=DEFAULT")
            params.append("direction=DESC")

        if page > 1:
            params.append(f"page={page}")
        if self.price_min is not None:
            params.append(f"priceMin={self.price_min}")
        if self.price_max is not None:
            params.append(f"priceMax={self.price_max}")
        if self.direction is not None:
            params = [p for p in params if not p.startswith("direction=")]
            params.append(f"direction={self.direction}")

        query_string = "&".join(params)
        return f"{base_url}?{query_string}"
