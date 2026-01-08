# Crisis Intel LIVE: Real-Time Disaster

# Monitoring & Intelligence


A Live AI system for real-time disaster awareness, severity analysis, and
interactive intelligence — powered by Pathway's streaming engine and
LLM-driven reasoning.


## Overview

**Crisis Intel LIVE** is a **real-time Retrieval-Augmented Generation (RAG)** application that
continuously ingests disaster-related data streams, enriches them using LLM-based
intelligence, and serves **up-to-date, context-aware answers** through an interactive chatbot
interface.
Unlike traditional static RAG systems, Crisis Intel LIVE **updates its knowledge base instantly**
as new disaster information arrives — demonstrating the core principles of **Live AI** as required
by the Pathway Dynamic RAG challenge.

## Problem Statement Alignment

This project directly addresses the **Pathway Hackathon Challenge: Dynamic RAG
Playground** , by:
● Connecting to **dynamic, continuously updating data sources**.
● Performing **incremental streaming transformations**.
● Maintaining an **always-fresh vector index**.
● Demonstrating **instant response changes** when new data appears.
● Integrating **LLMs for real-time reasoning and summarization**.

## System Capabilities

```
● Live Disaster Ingestion (news feeds + simulated streams)
● Custom Pathway Python Connector
● Streaming NLP + Feature Engineering
● LLM-based severity classification & information extraction
● Real-time Vector Store (Pathway LLM xPack)
● Interactive Chatbot (Flask + RAG)
● Instant updates without restarts or re-indexing
```
## Architecture

The architecture relies on Pathway's event-driven engine to propagate updates from source
to index instantly.


1. **Live Data Sources** : RSS feeds and text streams.
2. **Custom Connector** : Ingests raw text and converts it to a structured stream.
3. **Streaming Transformations** : Applies LLM extraction (Groq) and metadata parsing.
4. **Vector Store** : Pathway incrementally indexes the processed documents.
5. **RAG Backend** : Flask API retrieves relevant contexts and generates answers.
6. **Frontend** : Web-based chat interface.

## Repository Structure

crisis-conspirators/
│
├── app.py # Flask backend + chatbot API
├── pipeline.py # Pathway streaming + vector store
├── llm_extractor.py # LLM-based disaster intelligence
├── transformations.py # Streaming feature engineering
├── scraper.py # Live RSS news ingestion
├── file_scraper.py # Simulated streaming via text file
├── connector_scraper.py # Custom Pathway connector
├── disasters.txt # Editable live disaster stream
│
├── templates/ # Flask HTML templates
├── static/ # CSS + JS assets
│
├── requirements.txt
├── .env # API keys & configuration
├── .gitignore
└── LICENSE

## Live Data Ingestion (Requirement 1)

### Implemented Approaches

1. **Custom Python Connector (Pathway)** : Converts file updates and web scraping into a
    live stream.
2. **Simulated Streaming (disasters.txt)** : New disaster entries are picked up **without**
    **restarting**.
3. **Optional Live RSS Feeds** : Demonstrates real-time ingestion from web sources.
This satisfies the requirement for **at least one live or simulated data feed**.

## Streaming Transformations (Requirement 3)

All data transformations are executed **incrementally** using Pathway tables:


● NLP parsing
● Metadata extraction
● Severity classification
● Narrative generation
● Vector indexing
No batch reprocessing is required — only **delta updates propagate**.

## LLM Integration (Requirement 4)

LLMs are used in **two real-time stages** :

### 1. Pre-Index Intelligence (LLM Extractor)

Each incoming article is processed once to extract:
● Disaster type
● Severity (minor -> catastrophic)
● Location
● Death / injury counts
● Short factual summary
This ensures **high-quality, structured embeddings**.

### 2. RAG Answer Generation

User queries are answered using:
● Pathway vector retrieval
● LLM reasoning over **latest indexed facts**

## Example Scenario (Demonstrable Dynamism)

### Step 1: User Query (Before Data Exists)

User: Any disaster in Kolkata?
Bot: The latest data stream does not contain enough information yet.

### Step 2: Add to disasters.txt

Severe flooding in Kolkata
72 hours of heavy rainfall caused severe waterlogging across Kolkata...

### Step 3: Same Query (Instant Update)

User: Any disaster in Kolkata?
Bot: There is a severe flood in Kolkata caused by continuous rainfall...


**No restart. No re-index. Instant knowledge update.**

## Running the Project

### 1. Setup Environment

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 2. Configure Environment Variables

Create a .env file in the root directory:
GROQ_API_KEY=your_api_key_here

### 3. Start Pathway Vector Server

This starts the data ingestion pipeline and vector index.
python pipeline.py
_Runs at: [http://localhost:8000](http://localhost:8000)_

### 4. Start Flask App

In a new terminal, start the web server.
python app.py
_Runs at: [http://localhost:5000](http://localhost:5000)_

## Testing & Reliability

```
● LLM extraction has safe fallbacks.
● Streaming ingestion is idempotent.
● Duplicate events are ignored.
● System remains live even if LLM temporarily fails.
```
## Scalability & Extensions

```
● Replace file streams with Kafka or CDC pipelines.
```

```
● Deploy using Docker.
● Add temporal windows and alert thresholds.
● Extend to: Epidemic monitoring, Infrastructure failures, Financial risk intelligence.
```
## Key Learnings

```
● Streaming-first thinking changes system design.
● LLMs are most effective before indexing for cleaner retrieval.
● Pathway removes reprocessing bottlenecks.
● Live AI is about behavior change, not static answers.
```

