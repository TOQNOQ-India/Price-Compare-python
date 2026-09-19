from src.services.parsing import match_score, parse_price


def test_parse_price():
    assert parse_price("₹39,999") == 39999
    assert parse_price("INR 1,299") == 1299
    assert parse_price(None) is None


def test_match_score_prefers_same_product():
    same = match_score("iphone 11 64gb", "Apple iPhone 11 64 GB")
    different = match_score("iphone 11 64gb", "Samsung Galaxy S24 256GB")
    assert same > different
