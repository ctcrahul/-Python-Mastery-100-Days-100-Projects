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
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# -----------------------------
# SCRAPER FUNCTION
# -----------------------------
def scrape_subreddit(subreddit_name, limit=50):
    subreddit = reddit.subreddit(subreddit_name)

    posts = []

    for post in subreddit.hot(limit=limit):
        posts.append({
            "title": post.title,
            "author": str(post.author),
            "score": post.score,
            "num_comments": post.num_comments,
            "created_utc": post.created_utc,
            "url": post.url,
            "selftext": post.selftext
        })
