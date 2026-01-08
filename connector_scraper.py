import pathway as pw
from pathway.io.python import ConnectorSubject
from scraper import scrape_articles   # your generator


class NewsScraperSubject(ConnectorSubject):
    def __init__(self, website_urls, refresh_interval=60):
        super().__init__()
        self.website_urls = website_urls
        self.refresh_interval = refresh_interval

    def run(self):
        for article in scrape_articles(
            self.website_urls,
            refresh_interval=self.refresh_interval,
        ):
            # VERY IMPORTANT:
            # We normalize into the SAME keys expected by transformations.py
            self.next(
                data={
                    "title": article.get("title", "Unknown Event"),
                    "event_type": article.get("event_type", "disaster"),
                    "alert_level": article.get("severity", "unknown"),
                    "country": article.get("country", "unknown"),
                    "region": article.get("region"),
                    "timestamp": article.get("timestamp"),
                    "status": article.get("status", "active"),
                }
            )


# ------ Pathway Schema -------
class ScraperSchema(pw.Schema):
    data: dict   # raw structured object for the transformations module


# ------ Function the pipeline imports -------
def build_scraper_table():
    subject = NewsScraperSubject(
        website_urls=[
            "http://feeds.bbci.co.uk/news/world/rss.xml",
            "https://www.aljazeera.com/xml/rss/all.xml",
            "https://rss.cnn.com/rss/edition_world.rss",
        ],
        refresh_interval=30,
    )

    return pw.io.python.read(subject, schema=ScraperSchema)
