import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.3-70b-versatile"


def extract_disaster_info(title: str, content: str) -> dict:
    """
    Uses LLM to extract structured disaster information from a news article.
    Returns a dictionary with normalized fields.
    """

    prompt = f"""
You are a disaster analysis system.

From the following news article, extract the information below.

Return ONLY valid JSON. Do not include explanations or markdown.

Fields:
- disaster_type (e.g. flood, earthquake, cyclone, wildfire)
- severity (minor | moderate | severe | catastrophic)
- location (city, country if possible)
- deaths (number or null)
- injured (number or null)
- summary (max 2 factual sentences)

Article Title:
{title}

Article Content:
{content}
"""

    try:
        response = groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        raw_text = response.choices[0].message.content.strip()

        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")

        print("RAW LLM OUTPUT:\n", raw_text)

        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        clean_json = raw_text[start:end]

        data = json.loads(clean_json)

        print("LLM EXTRACTED:", data)
        return {
            "disaster_type": data.get("disaster_type", "unknown"),
            "severity": data.get("severity", "unknown"),
            "location": data.get("location", "unknown"),
            "deaths": data.get("deaths"),
            "injured": data.get("injured"),
            "summary": data.get("summary", ""),
        }

    except Exception as e:
        print("LLM EXTRACTION FAILED:", e)

        return {
            "disaster_type": "unknown",
            "severity": "unknown",
            "location": "unknown",
            "deaths": None,
            "injured": None,
            "summary": title,
        }
