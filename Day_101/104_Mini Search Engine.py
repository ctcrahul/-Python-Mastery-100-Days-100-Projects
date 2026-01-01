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
