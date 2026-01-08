import time
from typing import Generator, List

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


def scrape_from_file(path: str, refresh_interval: int = 10) -> Generator:
    """
    Continuously watches the file and yields NEW disaster records when added.
    """

    seen: List[str] = []

    while True:
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"File not found: {path}")
            time.sleep(refresh_interval)
            continue

        for line in lines:
            if line in seen:
                continue

            seen.append(line)

            # filter non-natural disasters
            if not is_natural_disaster(line):
                continue

            record = {
                "title": line,
                "event_type": "disaster",
                "alert_level": "unknown",
                "country": "unknown",
                "region": None,
                "timestamp": None,
                "status": "active",
            }

            print("SCRAPED:", record)

            yield record

        time.sleep(refresh_interval)
