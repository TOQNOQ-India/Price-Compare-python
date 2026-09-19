from typing import List

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from src.services.comparator import compare_prices
from src.stores.amazon import AmazonAdapter
from src.stores.flipkart import FlipkartAdapter

app = FastAPI(title="Price Compare API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

ADAPTERS = [AmazonAdapter(), FlipkartAdapter()]


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/v1/compare")
def compare(
    q: str = Query(..., min_length=2, max_length=200),
    minimum_score: float = Query(0.55, ge=0.0, le=1.0),
):
    query = q.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    return compare_prices(query, ADAPTERS, minimum_score)
