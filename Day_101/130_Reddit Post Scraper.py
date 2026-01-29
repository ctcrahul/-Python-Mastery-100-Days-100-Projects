# Reddit Post Scraper (Single File)
# Scrapes posts from a subreddit and saves to CSV

import praw
import pandas as pd

# -----------------------------
# REDDIT API CREDENTIALS
# -----------------------------
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
USER_AGENT = "reddit_scraper_by_your_username"

# -----------------------------
# CONNECT TO REDDIT
# -----------------------------
