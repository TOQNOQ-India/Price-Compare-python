from typing import List
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from src.models import ProductOffer
from src.services.parsing import parse_price
from src.stores.base import StoreAdapter


class AmazonAdapter(StoreAdapter):
    name = "Amazon"

    def search(self, query: str) -> List[ProductOffer]:
        url = "https://www.amazon.in/s?k={}".format(quote_plus(query))
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15,
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        offers = []

        for item in soup.select("[data-component-type='s-search-result']")[:10]:
            title_node = item.select_one("h2 a span")
            price_node = item.select_one(".a-price-whole")
            link_node = item.select_one("h2 a")
            if not title_node or not price_node or not link_node:
                continue

            href = link_node.get("href", "")
            offers.append(ProductOffer(
                store=self.name,
                title=title_node.get_text(" ", strip=True),
                url="https://www.amazon.in{}".format(href),
                price=parse_price(price_node.get_text(strip=True)),
                availability="Available",
            ))
        return offers
