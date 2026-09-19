import re
from difflib import SequenceMatcher


def normalize_text(value: str) -> str:
    value = value.casefold()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def match_score(query: str, title: str) -> float:
    return SequenceMatcher(
        None,
        normalize_text(query),
        normalize_text(title),
    ).ratio()


def parse_price(value: Optional[str]) -> Optional[int]:
    if not value:
        return None

    cleaned = re.sub(r"[^0-9.]", "", value)
    if not cleaned:
        return None

    try:
        return round(float(cleaned))
    except ValueError:
        return None
