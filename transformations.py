"""
This module contains all data transformation logic used to convert
raw disaster API JSON into natural language narratives optimized
for real-time RAG and LLM-based reasoning.
"""

from datetime import datetime
from typing import Dict, Optional


def _parse_timestamp(timestamp: Optional[str]) -> str:
    """
    Safely parses an ISO timestamp into a readable UTC string.
    """
    if not timestamp:
        return "an unknown time"

    try:
        return datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M UTC")
    except ValueError:
        return "an unknown time"


def narrative_parser(data_point: Dict) -> str:
    """
    Converts a raw disaster API JSON object into a clear, descriptive
    English sentence suitable for vector indexing and LLM retrieval.

    Parameters
    ---------
    data_point : dict
        Raw JSON object from a disaster alert API.

    Returns
    -------
    str
        A human-readable narrative describing the disaster alert.
    """

    # Core fields (with safe fallbacks)
    title = data_point.get("title", "Unspecified Disaster Event")
    disaster_type = data_point.get("event_type", "disaster")
    severity = data_point.get("alert_level", "unknown severity")

    # Location handling
    country = data_point.get("country", "unknown location")
    region = data_point.get("region")
    location = f"{region}, {country}" if region else country

    # Time handling
    timestamp = _parse_timestamp(data_point.get("timestamp"))

    # Status flags
    is_active = data_point.get("status", "active").lower() == "active"

    status_phrase = (
        "This alert is currently active and requires attention."
        if is_active
        else "This alert is no longer active."
    )

    # Final narrative (this is what gets embedded & retrieved)
    narrative = (
        f"URGENT ALERT: A {severity} severity {disaster_type} event titled "
        f"'{title}' was reported in {location} at {timestamp}. "
        f"{status_phrase}"
    )

    return narrative


def extract_metadata(data_point: Dict) -> Dict:
    """
    Extracts structured metadata for filtering, sorting, or UI display.
    This data is NOT embedded but can be used for recency/severity logic.
    """

    return {
        "event_type": data_point.get("event_type"),
        "severity": data_point.get("alert_level"),
        "country": data_point.get("country"),
        "region": data_point.get("region"),
        "timestamp": data_point.get("timestamp"),
        "status": data_point.get("status", "active"),
    }