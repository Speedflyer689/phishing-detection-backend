from datetime import datetime, timezone

def get_current_utc_time():
    """
    Returns the current UTC time as a datetime object
    """
    return datetime.now(timezone.utc)

def get_current_utc_timestamp():
    """
    Returns the current UTC timestamp as an integer
    """
    return int(datetime.now(timezone.utc).timestamp())

def get_current_utc_iso_string():
    """
    Returns the current UTC time in ISO 8601 format string
    """
    return datetime.now(timezone.utc).isoformat()