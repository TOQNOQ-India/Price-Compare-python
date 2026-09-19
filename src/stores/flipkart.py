from typing import List
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from src.models import ProductOffer
from src.services.parsing import parse_price
from src.stores.base import StoreAdapter


class FlipkartAdapter(StoreAdapter):
    name = "Flipkart"

    def search(self, query: str) -> List[ProductOffer]:
        url = "https://www.flipkart.com/search?q={}".format(quote_plus(query))
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15,
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        offers = []

        cards = soup.select("div._1AtVbE") or soup.select("div._2kHMtA")
        for card in cards[:10]:
            title_node = card.select_one("._4rR01T, .s1Q9rs")
            price_node = card.select_one("._30jeq3")
            link_node = card.select_one("a")
            if not title_node or not price_node or not link_node:
                continue

            href = link_node.get("href", "")
            product_url = href if href.startswith("http") else "https://www.flipkart.com{}".format(href)
            offers.append(ProductOffer(
                store=self.name,
                title=title_node.get_text(" ", strip=True),
                url=product_url,
                price=parse_price(price_node.get_text(strip=True)),
                availability="Available",
            ))
        return offers
