from transformations import *
test={
  "title": "River water level rising",
  "event_type": "flood",
  "alert_level": "high",
  "country": "India",
  "region": "Assam",
  "timestamp": "2026-01-01T06:30:00",
  "status": "active"
}

print(narrative_parser(test))