import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import math

# -----------------------------
# CRAWLER
# -----------------------------
def crawl(url, max_pages=5):
    visited = set()
    pages = {}

    def extract_links(html, base):
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            link = a["href"]
            if link.startswith("http"):
                links.append(link)
        return links

    def clean_text(html):
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text().lower()
        return re.findall(r"[a-z]{3,}", text)

    stack = [url]
    return pages

# -----------------------------
# BUILD INVERTED INDEX
# -----------------------------
def build_index(pages):
    index = defaultdict(set)
    for url, words in pages.items():
        for word in words:
            index[word].add(url)
    return index

# -----------------------------
# SEARCH ENGINE
# -----------------------------
def search(query, index):
    terms = query.lower().split()
    scores = defaultdict(int)

    for term in terms:
        for url in index.get(term, []):
            scores[url] += 1

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked
