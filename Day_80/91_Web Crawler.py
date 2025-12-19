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
