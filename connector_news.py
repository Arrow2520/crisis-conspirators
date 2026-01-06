import pathway
import time
from pathway.io.python import read


def news_stream():
    data = [
        {
            "id": "1",
            "title": "River level rising",
            "event_type": "flood",
            "alert_level": "moderate",
            "country": "India",
            "region": "Assam",
            "timestamp": "2026-01-05T10:00:00",
            "status": "active",
        },
        {
            "id": "1",
            "title": "River overflow warning issued",
            "event_type": "flood",
            "alert_level": "high",
            "country": "India",
            "region": "Assam",
            "timestamp": "2026-01-05T10:05:00",
            "status": "active",
        },
    ]

    for row in data:
        yield row
        time.sleep(10)   # simulate real‑time updates


def build_table():
    return read(news_stream())
