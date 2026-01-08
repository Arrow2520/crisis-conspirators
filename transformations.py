import json
from datetime import datetime
from typing import Dict, Optional, Any


def _ensure_dict(data_point: Any) -> Dict:
    if isinstance(data_point, dict):
        return data_point

    # Pathway Json -> Python dict
    try:
        return json.loads(str(data_point))
    except Exception:
        return {}

def _parse_timestamp(timestamp: Optional[str]) -> str:
    if not timestamp:
        return "an unknown time"
    try:
        return datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M UTC")
    except ValueError:
        return "an unknown time"


def narrative_parser(data_point):
    data_point = _ensure_dict(data_point)

    title = data_point.get("title", "Unspecified Disaster Event")
    disaster_type = data_point.get("event_type", "disaster")
    severity = data_point.get("alert_level", "unknown severity")

    country = data_point.get("country", "unknown location")
    region = data_point.get("region")
    location = f"{region}, {country}" if region else country

    timestamp = _parse_timestamp(data_point.get("timestamp"))
    is_active = data_point.get("status", "active").lower() == "active"

    status_phrase = (
        "This alert is currently active and requires attention."
        if is_active else
        "This alert is no longer active."
    )

    return (
        f"URGENT ALERT: A {severity} severity {disaster_type} event titled "
        f"'{title}' was reported in {location} at {timestamp}. {status_phrase}"
    )


def extract_metadata(data_point):
    data_point = _ensure_dict(data_point)

    return {
        "event_type": data_point.get("event_type"),
        "severity": data_point.get("alert_level"),
        "country": data_point.get("country"),
        "region": data_point.get("region"),
        "timestamp": data_point.get("timestamp"),
        "status": data_point.get("status", "active"),
    }
