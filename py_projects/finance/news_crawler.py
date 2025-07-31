import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("Financial News Browser")

NEWS_URL = "https://finance.yahoo.com/"

def get_yahoo_finance_headlines():
    res = requests.get(NEWS_URL)
    soup = BeautifulSoup(res.text, "html.parser")
    headlines = []
    for item in soup.find_all("h3"):
        a = item.find("a")
        if a and a.text:
            link = a["href"]
            if not link.startswith("http"):
                link = "https://finance.yahoo.com" + link
            headlines.append((a.text.strip(), link))
    return headlines

# Add a text input for keyword search
keyword = st.text_input("Enter a keyword (e.g., company name):").strip().lower()

st.header("Latest Yahoo Finance Headlines")
headlines = get_yahoo_finance_headlines()

# Filter headlines by keyword if provided
if keyword:
    filtered = [(title, url) for title, url in headlines if keyword in title.lower()]
    if filtered:
        for title, url in filtered:
            st.markdown(f"- [{title}]({url})")
    else:
        st.write("No news found for that keyword.")
else:
    for title, url in headlines:
        st.markdown(f"- [{title}]({url})")