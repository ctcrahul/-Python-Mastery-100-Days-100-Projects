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

    while stack and len(visited) < max_pages:
        current = stack.pop()
        if current in visited:
            continue

        try:
            res = requests.get(current, timeout=5)
            visited.add(current)
            words = clean_text(res.text)
            pages[current] = words

            links = extract_links(res.text, current)
            stack.extend(links[:3])

        except:
            pass

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

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    seed_url = "https://example.com"
    print("Crawling...")
    pages = crawl(seed_url)

    print("Building index...")
    index = build_index(pages)

    print("\nSearch Engine Ready.\n")
    while True:
        q = input("Search query (or exit): ")
        if q == "exit":
            break
        results = search(q, index)
        for url, score in results[:5]:
            print(f"{url}  (score={score})")
