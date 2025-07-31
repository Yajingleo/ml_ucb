import streamlit as st
import requests
import collections
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Set, List
import argparse


# NEWS_URL = st.text_input("Enter a website to read:").strip().lower()


def crawl_headlines(url: str, 
                max_page: int = 100, 
                max_search = 1000) -> Set[str]:
    links = set()
    headlines = set()
    queue = collections.deque([url])
    count = 0
    while queue and len(links) < max_page and count < max_search:
        count += 1
        current_url = queue.popleft()
        if current_url in links:
            continue
        links.add(current_url)

        try: 
            res = requests.get(current_url)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, "html.parser")

            # find all heading tags
            for tag in ["h1", "h2", "h3"]:
                for heading in soup.find_all(tag):
                    text = heading.text.strip()
                    if text:
                        # print(text)
                        headlines.add((text, current_url))

            # find all anchor tags
            for a in soup.find_all("a", href=True):
                link = a["href"]
                if link.startswith("http"):
                    # print(link)
                    queue.append(link)
        except Exception as e:
            print("Error: ", e)
            pass
    return headlines


if __name__ == "__main__":
    st.title("Financial News Browser")

    NEWS_URL = "https://finance.sina.com.cn/"
    
    # Add a text input for keyword search
    url = st.text_input("Enter a url to crawl:").strip().lower()

    # Add a text input for keyword search
    keyword = st.text_input("Enter a keyword to extract:").strip().lower()

    if url:
        NEWS_URL = url
    else:
        pass

    # Crawl links from the specified URL
    headlines = crawl_headlines(NEWS_URL, 10)
    
    # Filter headlines by keyword if provided
    if keyword:
        filtered = [(title, url) for title, url in headlines 
                    if keyword in title.lower()]
        if filtered:
            for title, url in filtered:
                st.markdown(f"- [{title}]({url})")
        else:
            st.write("No news found for that keyword.")
    else:
        for title in headlines:
            st.markdown(f"- [{title}]({url})")

