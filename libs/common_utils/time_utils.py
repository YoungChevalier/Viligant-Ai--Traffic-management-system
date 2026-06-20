from datetime import datetime, timezone

def utc_now() -> datetime:
    """
    Returns the current UTC time as a timezone-aware datetime object.
    """
    return datetime.now(timezone.utc)

def parse_iso_datetime(value: str) -> datetime:
    """
    Parses an ISO 8601 formatted string into a datetime object.
    """
    # Replace 'Z' with '+00:00' to support older Python versions
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

def to_iso_datetime(dt: datetime) -> str:
    """
    Converts a datetime object to an ISO 8601 formatted string.
    """
    return dt.isoformat()
