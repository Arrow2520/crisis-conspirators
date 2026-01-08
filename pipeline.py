import pathway as pw
from file_scraper import scrape_from_file
from transformations import narrative_parser, extract_metadata
from pathway.io.python import ConnectorSubject
from pathway.xpacks.llm.vector_store import VectorStoreServer
from pathway.xpacks.llm.embedders import SentenceTransformerEmbedder

# --- 1. Define the Schema ---
class InputSchema(pw.Schema):
    data: dict

# --- 2. Define the Connector Subject ---
class FileSubject(ConnectorSubject):
    def __init__(self, path, refresh_interval=5):
        super().__init__()
        self.path = path
        self.refresh_interval = refresh_interval

    def run(self):
        # iterate the generator and push data into the 'data' column
        for record in scrape_from_file(self.path, refresh_interval=self.refresh_interval):
            self.next(data=record)

# --- 3. Build the Table ---
def build_scraper_table():
    subject = FileSubject("disasters.txt", refresh_interval=5)

    return pw.io.python.read(subject, schema=InputSchema)

# --- 4. Build the Vector Server ---
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
        threaded=False,
    )