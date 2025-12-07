import logging
from datetime import datetime, timezone

def setup_logger(name: str):
    """
    Set up and return a logger with the given name.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

def current_utc_time():
    """
    Return the current UTC time as a timezone-aware datetime.
    """
    return datetime.now(timezone.utc)

def ensure_utc(dt: datetime):
    """
    Ensure a datetime is timezone-aware in UTC.
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
