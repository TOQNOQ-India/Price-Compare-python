from typing import List, Optional

from pydantic import BaseModel, Field


class ProductOffer(BaseModel):
    store: str
    title: str
    url: str
    price: Optional[int] = None
    shipping: int = 0
    image_url: Optional[str] = None
    availability: Optional[str] = None
    match_score: float = Field(default=0.0, ge=0.0, le=1.0)
    error: Optional[str] = None

    @property
    def total_price(self) -> Optional[int]:
        if self.price is None:
            return None
        return self.price + self.shipping


class ComparisonResponse(BaseModel):
    query: str
    offers: List[ProductOffer]
    cheapest_store: Optional[str] = None
    cheapest_price: Optional[int] = None
    searched_stores: List[str]
    failed_stores: List[str] = []
