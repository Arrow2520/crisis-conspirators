from flask import Flask, request, jsonify
from dotenv import load_dotenv
from rag import ask_rag

load_dotenv()
app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    q = request.json.get("question")
    answer = ask_rag(q)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(port=5000)
