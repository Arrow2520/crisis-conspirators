import pathway as pw
import time


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
        time.sleep(10)


@pw.io.stream
def build_table():
    for row in news_stream():
        yield row
