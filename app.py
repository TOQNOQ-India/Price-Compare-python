import requests
import streamlit as st


API_URL = "http://localhost:8000"

st.set_page_config(page_title="Price Compare", page_icon="🛒", layout="wide")
st.title("🛒 Price Compare")
st.caption("Compare product offers from supported stores.")

query = st.text_input(
    "Product name",
    placeholder="Example: Apple iPhone 11 64GB",
)
minimum_score = st.slider(
    "Minimum match confidence",
    min_value=0.0,
    max_value=1.0,
    value=0.55,
    step=0.05,
)

if st.button("Compare prices", type="primary", disabled=not query.strip()):
    try:
        with st.spinner("Searching stores..."):
            response = requests.get(
                "{}/api/v1/compare".format(API_URL),
                params={"q": query.strip(), "minimum_score": minimum_score},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
    except requests.RequestException as error:
        st.error("The API is unavailable. Start it with: uvicorn api.main:app --reload")
        st.caption(str(error))
    else:
        if data.get("cheapest_price") is not None:
            st.success(
                "Lowest price: ₹{:,} on {}".format(
                    data["cheapest_price"], data["cheapest_store"]
                )
            )

        if data.get("failed_stores"):
            st.warning("Some stores failed: " + "; ".join(data["failed_stores"]))

        offers = data.get("offers", [])
        if not offers:
            st.info("No matching products were found.")

        for offer in offers:
            with st.container(border=True):
                left, middle, right = st.columns([3, 1, 1])
                with left:
                    st.subheader(offer["title"])
                    st.write("Store: **{}**".format(offer["store"]))
                    st.write("Match confidence: {:.0%}".format(offer["match_score"]))
                    st.write(offer.get("availability") or "Availability unknown")
                with middle:
                    if offer.get("price") is not None:
                        st.metric("Price", "₹{:,}".format(offer["price"]))
                    else:
                        st.metric("Price", "Unavailable")
                with right:
                    st.link_button("View product", offer["url"])
