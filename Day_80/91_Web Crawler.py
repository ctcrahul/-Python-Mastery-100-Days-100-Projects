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

        print(f"[DEPTH {depth}] {url}")
        visited.add(url)

        try:
            resp = requests.get(url, timeout=TIMEOUT)
            if "text/html" not in resp.headers.get("Content-Type", ""):
                continue
        except Exception:
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.find_all("a", href=True):
            link = normalize(urljoin(url, a["href"]))
            if same_domain(link, base_netloc) and link not in visited:
                queue.append((link, depth + 1))

    print(f"\nCrawled {len(visited)} pages.")
    return visited

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python web_crawler.py <url>")
        sys.exit(1)

    crawl(sys.argv[1])
