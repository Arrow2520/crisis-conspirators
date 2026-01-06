import requests
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

VECTOR_URL = "http://localhost:8000/query"

def ask_rag(question: str):
    res = requests.post(VECTOR_URL, json={"query": question, "k": 3})
    docs = res.json()["documents"]

    context = "\n\n".join([d["text"] for d in docs])

    prompt = f"""
    Use the information below ONLY.

    Context:
    {context}

    Question: {question}
    """
    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content
