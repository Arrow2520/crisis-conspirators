# Crisis Intel LIVE: Real-Time Disaster Monitoring & Intelligence

A Live AI system for real-time disaster awareness, severity analysis, and interactive intelligence — powered by Pathway's streaming engine and LLM-driven reasoning.

## ⚖️ **Instructions for Judges (Start Here)**

**Objective**: Verify the "Live AI" capability where the system updates its knowledge base instantly without restarting.

**Setup**: Ensure you have your .env file with GROQ_API_KEY.

**Launch**: Run ./start.sh (or use Docker).

**Step 1** - Initial Query:

Open http://localhost:5000.

Ask: "Is there a flood in Kolkata?"

Result: The bot should reply that it has no current data on this.

**Step 2** - Inject Live Data:

Open disasters.txt in the root folder.

Paste the following line (strictly in the following format as the first line serves as title and the second line as the article for the news) and save:

Severe flooding in Kolkata.\
72 hours of heavy rainfall caused severe waterlogging across Kolkata affecting thousands.

**Step 3** - Instant Verification:

Immediately ask the bot again: "Is there a flood in Kolkata?"

Result: The bot will now confirm the flood and provide details.

NOTE: No restart or re-indexing is required.

## 📖 **Overview**

Crisis Intel LIVE is a real-time Retrieval-Augmented Generation (RAG) application that continuously ingests disaster-related data streams, enriches them using LLM-based intelligence, and serves up-to-date, context-aware answers through an interactive chatbot interface.

Unlike traditional static RAG systems, Crisis Intel LIVE updates its knowledge base instantly as new disaster information arrives — demonstrating the core principles of Live AI as required by the Pathway Dynamic RAG challenge.

## 🎯 **Problem Statement Alignment**

* This project directly addresses the Pathway Hackathon Challenge: Dynamic RAG Playground, by:

* Connecting to dynamic, continuously updating data sources.

* Performing incremental streaming transformations.

* Maintaining an always-fresh vector index.

* Demonstrating instant response changes when new data appears.

* Integrating LLMs for real-time reasoning and summarization.

## ⚙️ **System Capabilities**

* Live Disaster Ingestion: Handles news feeds and simulated text streams.

* Custom Pathway Connector: Ingests raw text and converts it to a structured stream.

* Streaming NLP + Feature Engineering: Real-time processing of text data.

* LLM-based Intelligence: Severity classification and information extraction using Groq.

* Real-time Vector Store: Powered by Pathway LLM xPack.

* Interactive Chatbot: Flask + RAG frontend.

* Zero-Downtime Updates: Instant knowledge updates without restarts.

## 🏗 **Architecture**

* The architecture relies on Pathway's event-driven engine to propagate updates from source to index instantly.

* Live Data Sources: RSS feeds and text streams.

* Custom Connector: Ingests raw text and converts it to a structured stream.

* Streaming Transformations: Applies LLM extraction (Groq) and metadata parsing.

* Vector Store: Pathway incrementally indexes the processed documents.

* RAG Backend: Flask API retrieves relevant contexts and generates answers.

* Frontend: Web-based chat interface.

## 📂 **Repository Structure**
```
crisis-conspirators/
│
├── app.py                 # Flask backend + chatbot API
├── pipeline.py            # Pathway streaming + vector store
├── llm_extractor.py       # LLM-based disaster intelligence
├── transformations.py     # Streaming feature engineering
├── scraper.py             # Live RSS news ingestion
├── file_scraper.py        # Simulated streaming via text file
├── connector_scraper.py   # Custom Pathway connector
├── disasters.txt          # Editable live disaster stream
├── start.sh               # Quick start script for judges
├── Dockerfile             # Container configuration
│
├── templates/             # Flask HTML templates
├── static/                # CSS + JS assets
│
├── requirements.txt       # Python dependencies
├── .env                   # API keys & configuration
└── LICENSE
```

## 🚀 **Running the Project**
First configure the API key in a .env file (in root directory), by creating one from https://console.groq.com/home
GROQ_API_KEY=your_api_key_here

### **Option A: Docker**

* Build the Image:

`docker build -t crisis-intel` .


* Run the Container:

`docker run -p 5000:5000 -p 8000:8000 --env-file .env crisis-intel`
Pathway runs at: http://localhost:8000

Web App runs at: http://localhost:5000\
* Open [http://localhost:5000](http://localhost:5000) in browser.

### **Option B: Quick Start Script**

* We have provided a convenience script to start both the Pathway backend and the Flask frontend.

* Configure Environment:
   Create a .env file in the root directory:

   GROQ_API_KEY=your_api_key_here


* Run the Script:

`chmod +x start.sh`
`./start.sh`

* Pathway runs at: http://localhost:8000

* Web App runs at: http://localhost:5000\
* Open [http://localhost:5000](http://localhost:5000) in browser.

### **Option C: Manual Setup**

* Configure Environment:
   Create a `.env` file in the root directory:

   `GROQ_API_KEY=your_api_key_here`

* Setup Environment:

`python -m venv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`


* Start Pathway Vector Server:
  This starts the data ingestion pipeline and vector index.

`python pipeline.py`


* Start Flask App:
  In a new terminal window:

`python app.py`
* Pathway runs at: http://localhost:8000

* Web App runs at: http://localhost:5000\
* Open [http://localhost:5000](http://localhost:5000) in browser.

## 🧠 **LLM Integration & Streaming**

### Streaming Transformations

All data transformations are executed incrementally using Pathway tables:

* NLP parsing & Metadata extraction

* Severity classification & Narrative generation

* Vector indexing

* No batch reprocessing is required — only delta updates propagate.

### LLM Stages

* Pre-Index Intelligence (LLM Extractor): Each incoming article is processed to extract disaster type, severity, location, and a factual summary.

* RAG Answer Generation: User queries are answered using Pathway vector retrieval + LLM reasoning over the latest indexed facts.

## 📊 **Example Scenario**

User Query (Before Data Exists):

User: "Any disaster in Kolkata?"

Bot: "The latest data stream does not contain enough information yet."

Live Update:

Add to disasters.txt: "Severe flooding in Kolkata..."

Same Query (Instant Update):

User: "Any disaster in Kolkata?"

Bot: "There is a severe flood in Kolkata caused by continuous rainfall..."

## 🔄 Data Ingestion Modes (Streaming Sources)

Crisis Intel LIVE is designed with a **pluggable ingestion layer**, allowing it to operate on multiple real-time data sources without changing downstream logic.

### Mode 1: Simulated Live Stream (Default – Judge Friendly)

- **Source**: `disasters.txt`
- **Connector**: Custom Pathway **Python Connector**
- **Behavior**:
  - The file is continuously monitored in streaming mode.
  - New disaster entries are ingested instantly.
  - Editing the file triggers real-time updates **without restarting the system**.

This mode is enabled by default to ensure **deterministic, reproducible evaluation** for judges.

---

### Mode 2: Live News Scraping (Optional)

- **Source**: Real-world RSS feeds and news websites
- **Connector**: Pathway Python Connector wrapping a web scraper
- **Libraries used**:
  - `feedparser`
  - `newspaper3k`
- **Processing pipeline**:
  - Articles are fetched continuously
  - Each article is enriched using an LLM
  - Results are incrementally indexed into the vector store

This mode demonstrates how the system can be extended to **production-grade live data feeds**.

---

## 🔧 Switching Between File Stream and Live News

The ingestion source is selected **centrally** in `pipeline.py`, without modifying any transformation, embedding, or retrieval logic.

### Default (File-Based Stream)

`table = build_scraper_table(mode="file")`

### Live News Scraping

`table = build_scraper_table(mode="news")`

## 🔮 **Scalability & Extensions**

* Data Sources: Replace file streams with Kafka or CDC pipelines.

* Deployment: Docker / Kubernetes integration.

* Analytics: Add temporal windows and alert thresholds.

* Domains: Extend to Epidemic monitoring, Infrastructure failures, or Financial risk intelligence.

## 💡 **Key Learnings**

* Streaming-first thinking fundamentally changes system design.

* LLMs are most effective before indexing to create cleaner retrieval contexts.

* Pathway removes traditional batch reprocessing bottlenecks.

* Live AI is about behavior change, not just static answers.
