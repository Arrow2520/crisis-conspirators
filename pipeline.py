import os
import pathway as pw
from pathway.io.python import ConnectorSubject
from pathway.xpacks.llm.vector_store import VectorStoreServer
from pathway.xpacks.llm.embedders import SentenceTransformerEmbedder
from transformations import narrative_parser, extract_metadata
from file_scraper import scrape_from_file
from scraper import scrape_articles

# ---------------- Schema ----------------
class InputSchema(pw.Schema):
    data: dict

# ---------------- Connector ----------------
class DisasterSubject(ConnectorSubject):
    def run(self):
        mode = os.getenv("INGEST_MODE", "file")

        if mode == "news":
            websites = [
                "http://feeds.bbci.co.uk/news/world/rss.xml",
                "https://www.aljazeera.com/xml/rss/all.xml",
                "https://rss.cnn.com/rss/edition_world.rss",
            ]
            for record in scrape_articles(
                website_urls=websites,
                refresh_interval=10,
            ):
                self.next(data=record)

        else:
            for record in scrape_from_file(
                filepath="disasters.txt",
                refresh_interval=5,
            ):
                self.next(data=record)

# ---------------- Table ----------------
def build_scraper_table():
    subject = DisasterSubject()
    return pw.io.python.read(subject, schema=InputSchema)

# ---------------- Vector Server ----------------
def build_vector_server():
    table = build_scraper_table()

    docs = table.select(
        data=pw.apply(narrative_parser, pw.this.data),
        _metadata=pw.apply(extract_metadata, pw.this.data),
    )

    embedder = SentenceTransformerEmbedder("all-MiniLM-L6-v2")

    return VectorStoreServer(docs, embedder=embedder)

# ---------------- Main ----------------
if __name__ == "__main__":
    server = build_vector_server()
    server.run_server(host="0.0.0.0", port=8000)
