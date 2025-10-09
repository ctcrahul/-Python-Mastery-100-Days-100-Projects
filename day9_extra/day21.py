
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

# Step 4: Extract Headings
def get_headings(soup):
  headings = [heading.text.strip() for heading in soup.find_all(['h2', 'h3', 'h4'])]
  return headings

# Step 5: Extract Related Links
def get_related_links(soup):
  links = []
  for a_tag in soup.find_all('a', href=True):
    href = a_tag['href']
    if href.startswith('/wiki/') and ":" not in href:
      links.append(f"https://en.wikipedia.org{href}")
  return list(set(links))[:5]

# Step 6: Main Program
def main():
  topic = input("Enter a topic to search on Wikipedia: ").strip()
  page_content = get_wikipedia_page(topic)

  if page_content:
    soup = BeautifulSoup(page_content, 'html.parser')
    title = get_article_title(soup)
    summary = get_article_summary(soup)
    headings = get_headings(soup)
    related_links = get_related_links(soup)

    print("\n--- Wikipedia Article Details ---")
    print(f"\nTitle: {title}")
    print(f"\nSummary: {summary}")
    print("\nHeadings:")
    for heading in headings[:5]:
      print(f"- {heading}")

   
