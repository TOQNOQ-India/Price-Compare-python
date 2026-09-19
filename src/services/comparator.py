from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

from src.models import ComparisonResponse, ProductOffer
from src.services.parsing import match_score


def compare_prices(query: str, adapters: list, minimum_score: float) -> ComparisonResponse:
    offers: List[ProductOffer] = []
    failures: List[str] = []

    with ThreadPoolExecutor(max_workers=len(adapters)) as executor:
        tasks = {executor.submit(adapter.search, query): adapter.name for adapter in adapters}
        for task in as_completed(tasks):
            store_name = tasks[task]
            try:
                for offer in task.result():
                    offer.match_score = match_score(query, offer.title)
                    if offer.match_score >= minimum_score:
                        offers.append(offer)
            except Exception as error:
                failures.append("{}: {}".format(store_name, str(error)))

    offers.sort(key=lambda offer: (
        offer.price is None,
        offer.price if offer.price is not None else float("inf"),
        -offer.match_score,
    ))

    cheapest = next((offer for offer in offers if offer.price is not None), None)
    return ComparisonResponse(
        query=query,
        offers=offers,
        cheapest_store=cheapest.store if cheapest else None,
        cheapest_price=cheapest.price if cheapest else None,
        searched_stores=[adapter.name for adapter in adapters],
        failed_stores=failures,
    )
