# Price Compare

A Phase 1 price comparison application with a FastAPI backend and Streamlit frontend.

## Features

- Search Amazon India and Flipkart in parallel
- Normalize results into a common offer format
- Compare total prices and identify the lowest offer
- Show match confidence, availability, and product links
- Handle retailer failures without failing the whole search

> Retailer pages change frequently and may block automated requests. Use official or approved retailer APIs where available, and make sure your usage complies with each retailer's terms.

## Setup

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn api.main:app --reload
```

Start the frontend in another terminal:

```bash
streamlit run app.py
```

The API is available at `http://localhost:8000`, with interactive documentation at `http://localhost:8000/docs`.

The Streamlit application is available at `http://localhost:8501`.

## API

```text
GET /health
GET /api/v1/compare?q=iphone%2011%2064gb&minimum_score=0.55
```

## Project layout

```text
app.py                 Streamlit frontend
api/main.py            FastAPI application
src/models.py          Shared response models
src/services/          Search orchestration and matching
src/stores/            Store adapters
```
