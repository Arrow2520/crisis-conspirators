from flask import Flask, request, jsonify
import os
import requests
from groq import Groq
from dotenv import load_dotenv
from pipeline import build_vector_server
from flask import Flask, request, jsonify, render_template
import pathway as pw
import threading
from pathway.xpacks.llm.vector_store import VectorStoreClient

load_dotenv()

app = Flask(__name__)

vector_server = build_vector_server()
vector_client = VectorStoreClient(url="http://localhost:8000")

def start_pathway():
    pw.run()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def retrieve_context(user_query: str, k: int = 5):
    try:
        results = vector_client.query(
            query=user_query,
            k=k,
        )
    except Exception as e:
        print("Vector store error:", e)
        return []

    return [r["text"] for r in results]



def generate_answer(question: str, context_docs: list[str]):

    context_block = "\n\n---\n".join(context_docs)

    prompt = f"""
You are a real-time disaster intelligence assistant.

You must ONLY use the information provided in the CONTEXT below.
If information is missing, say: "The latest data stream does not contain enough information yet."

QUESTION:
{question}

CONTEXT:
{context_block}

Answer clearly and concisely. Include location and severity if mentioned.
"""

    resp = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return resp.choices[0].message.content

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    print(" /ask endpoint hit")
    data = request.get_json()
    question = data.get("question")
    print(" Question:", question)

    print(" Retrieving context...")
    docs = retrieve_context(question)
    if not docs:
        return jsonify({
            "answer": "No active disaster information is currently available.",
            "sources": []
        })
    print(" Retrieved docs:", len(docs))

    print(" Generating answer...")
    answer = generate_answer(question, docs)

    print(" Done")
    return jsonify({"answer": answer, "sources": docs})


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)