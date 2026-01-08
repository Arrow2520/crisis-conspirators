import time
from typing import Generator
import feedparser
from newspaper import Article

NATURAL_KEYWORDS = [
    "flood", "earthquake", "tsunami",
    "wildfire", "forest fire",
    "hurricane", "cyclone", "typhoon",
    "storm", "tornado",
    "landslide", "mudslide",
    "volcano", "eruption",
    "drought", "heatwave", "heat wave"
]

def is_natural_disaster(text: str) -> bool:
    if not text:
        return False
    text = text.lower()
    return any(k in text for k in NATURAL_KEYWORDS)

def list_articles(website: str):
    feed = feedparser.parse(website)

    urls = []
    for entry in feed.entries:
        urls.append(entry.link)

    return urls


def scrape_articles(website_urls: list[str], refresh_interval: int) -> Generator:
    indexed_articles = set()

    while True:
        for website in website_urls:
            articles = list_articles(website)

            for url in articles:
                if url in indexed_articles:
                    continue

                try:
                    art = Article(url)
                    art.download()
                    art.parse()

                    text = art.text
                    title = art.title

                except Exception as e:
                    print("FAILED TO PARSE:", url, e)
                    continue

                indexed_articles.add(url)

                record = {
                    "data": {
                        "title": title,
                        "event_type": "disaster",
                        "alert_level": "unknown",
                        "country": "unknown",
                        "region": None,
                        "timestamp": None,
                        "status": "active",
                    }
                }

                # Ignore non-natural disaster events
                if not is_natural_disaster(record["data"].get("title", "")):
                    continue

                print("SCRAPED:", record)

                yield record

        time.sleep(refresh_interval)
