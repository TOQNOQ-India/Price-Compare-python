from abc import ABC, abstractmethod
from typing import List

from src.models import ProductOffer


class StoreAdapter(ABC):
    name = "Store"

    @abstractmethod
    def search(self, query: str) -> List[ProductOffer]:
        raise NotImplementedError
