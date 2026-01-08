import pathway as pw
# from connector_scraper import build_scraper_table
from file_scraper import scrape_from_file
from transformations import narrative_parser, extract_metadata
from pathway.io.python import ConnectorSubject
from pathway.xpacks.llm.vector_store import VectorStoreServer
from pathway.xpacks.llm.embedders import SentenceTransformerEmbedder

def build_scraper_table():
    gen = scrape_from_file("disasters.txt", refresh_interval=5)

    return pw.io.python.read(
        pw.io.python.generator(gen),
        format="json",
    )



def build_vector_server():
    table = build_scraper_table()

    docs = table.select(
        data=pw.apply(narrative_parser, pw.this.data),
        _metadata=pw.apply(extract_metadata, pw.this.data),
    )

    embedder = SentenceTransformerEmbedder("all-MiniLM-L6-v2")

    server = VectorStoreServer(
        docs,
        embedder=embedder,
    )

    return server

if __name__ == "__main__":
    server = build_vector_server()

    server.run_server(
        host="0.0.0.0",
        port=8000,
        threaded=False,   # leave blocking
    )
