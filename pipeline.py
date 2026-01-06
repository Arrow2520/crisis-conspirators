import pathway
from transformations import narrative_parser, extract_metadata
from connector_news import build_table

from pathway.xpacks.llm.vector_store import VectorStoreServer
from pathway.xpacks.llm.embedders import SentenceTransformerEmbedder

def run_vector_server():
    news_table = build_table()

    docs = news_table.select(
        text=pathway.apply(narrative_parser, pathway.this),
        metadata=pathway.apply(extract_metadata, pathway.this)
    )

    embedder = SentenceTransformerEmbedder("all-MiniLM-L6-v2")

    server = VectorStoreServer(
        docs=docs,
        embedder=embedder,
        parser=None,
        splitter=None
    )

    server.run_server(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_vector_server()

