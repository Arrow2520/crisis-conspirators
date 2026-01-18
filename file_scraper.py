import time
from typing import Generator
from llm_extractor import extract_disaster_info


NATURAL_KEYWORDS = [
    "flood", "earthquake", "tsunami",
    "wildfire", "forest fire",
    "hurricane", "cyclone", "typhoon",
    "storm", "tornado",
    "landslide", "mudslide",
    "volcano", "eruption",
    "drought", "heatwave", "heat wave"
]

def is_natural_disaster(text: str) -> bool:
    if not text:
        return False
    text = text.lower()
    return any(k in text for k in NATURAL_KEYWORDS)

def scrape_from_file(filepath: str, refresh_interval: int = 5) -> Generator:
    seen_titles = set()

    while True:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                raw = f.read().strip()
        except FileNotFoundError:
            print(f"Waiting for {filepath} to be created...")
            time.sleep(refresh_interval)
            continue

        if not raw:
            time.sleep(refresh_interval)
            continue

        blocks = raw.split("\n\n")

        for block in blocks:
            lines = [l.strip() for l in block.split("\n") if l.strip()]
            if len(lines) < 2:
                continue

            title = lines[0]
            content = "\n".join(lines[1:])

            if not is_natural_disaster(title + " " + content):
                continue

            if title in seen_titles:
                continue

            seen_titles.add(title)

            extracted = extract_disaster_info(title, content)

            d_type = extracted.get("disaster_type")
            if d_type is None or d_type == "unknown":
                print(f"SKIPPING (Not a disaster): {title}")
                continue

            record = {
                "title": title,
                "content": content,
                "event_type": "disaster",
                "status": "active",
                "timestamp": None,

                "alert_level": extracted.get("severity", "unknown"),
                "country": extracted.get("location", "unknown"),
                "region": None,

                "disaster_type": extracted.get("disaster_type", "unknown"),
                "deaths": extracted.get("deaths"),
                "injured": extracted.get("injured"),
                "summary": extracted.get("summary", ""),
            }

            print(f"FILE SCRAPED: {title}")
            yield record

        time.sleep(refresh_interval)