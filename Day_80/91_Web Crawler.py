""
Project 91 — Web Crawler (BFS, Domain-Limited)

Run:
    pip install requests beautifulsoup4
    python web_crawler.py https://example.com

Features:
- BFS crawl
- Same-domain restriction
- URL normalization
- Max depth & page limits
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
from collections import deque
import sys


MAX_PAGES = 50
MAX_DEPTH = 3
TIMEOUT = 5
def normalize(url):
    url, _ = urldefrag(url)  # remove #fragment
    return url.rstrip("/")


def same_domain(url, base_netloc):
    return urlparse(url).netloc == base_netloc


def crawl(start_url):
    visited = set()
    queue = deque([(start_url, 0)])

    parsed = urlparse(start_url)
    base_netloc = parsed.netloc

    print(f"Starting crawl: {start_url}\n")

    while queue and len(visited) < MAX_PAGES:
        url, depth = queue.popleft()

        if depth > MAX_DEPTH or url in visited:
            continue
