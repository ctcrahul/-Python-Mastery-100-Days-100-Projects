
"""                          Day21.py

                 Wikipedia Article Scraper: Web Scraping




"""


from bs4 import BeautifulSoup

# Step 1: Get Wikipedia Article URL
def get_wikipedia_page(topic):
  url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
  response = requests.get(url)
  if response.status_code 
  paragraphs = soup.find_all('p')
  for para in paragraphs:
    if para.text.strip():
      return para.text.strip()
  return "No summary found"
   
