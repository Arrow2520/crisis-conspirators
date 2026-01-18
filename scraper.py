import time
from typing import Generator
import feedparser
from newspaper import Article
from llm_extractor import extract_disaster_info

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
    try:
        feed = feedparser.parse(website)
        urls = [entry.link for entry in feed.entries]
        return urls
    except Exception as e:
        print(f"Error parsing feed {website}: {e}")
        return []


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

                if not is_natural_disaster(title + " " + text):
                    continue

                extracted = extract_disaster_info(title, text)

                d_type = extracted.get("disaster_type")
                if d_type is None or d_type == "unknown":
                    print(f"SKIPPING (Not a disaster): {title}")
                    continue

                record = {
                    "title": title,
                    "content": text,
                    "event_type": "disaster",
                    "status": "active",
                    "timestamp": None,
                    "alert_level": extracted.get("severity", "unknown"),
                    "country": extracted.get("location", "unknown"),
                    "region": None,
                    "disaster_type": extracted.get("disaster_type", "unknown"),
                    "deaths": extracted.get("deaths"),
                    "injured": extracted.get("injured"),
                    "summary": extracted.get("summary", ""),
                }

                print("SCRAPED:", record)
                yield record

        time.sleep(refresh_interval)