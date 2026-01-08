import json
from datetime import datetime
from typing import Dict, Optional, Any


def _ensure_dict(data_point: Any) -> Dict:
    if isinstance(data_point, dict):
        return data_point

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


def narrative_parser(data):
    data = _ensure_dict(data)

    return (
        f"Disaster type: {data.get('disaster_type', 'unknown')}. "
        f"Location: {data.get('country', 'unknown')}. "
        f"Severity: {data.get('alert_level', 'unknown')}. "
        f"Deaths: {data.get('deaths', 'unknown')}. "
        f"Injured: {data.get('injured', 'unknown')}. "
        f"Summary: {data.get('summary', '')}"
    )

def extract_metadata(data_point):
    data_point = _ensure_dict(data_point)

    return {
        "event_type": data_point.get("event_type"),
        "disaster_type": data_point.get("disaster_type"),
        "severity": data_point.get("alert_level"),
        "country": data_point.get("country"),
        "region": data_point.get("region"),
        "timestamp": data_point.get("timestamp"),
        "status": data_point.get("status", "active"),
    }

