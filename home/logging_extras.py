import logging
from contextvars import ContextVar

# Context var to carry correlation across threads/async
REQUEST_ID_CTX = ContextVar("request_id", default="-")

class RequestIDFilter(logging.Filter):
    """Ensures every record has .request_id from contextvar (or '-')"""
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            record.request_id = REQUEST_ID_CTX.get()
        except Exception:
            record.request_id = "-"
        return True

class SafeFormatter(logging.Formatter):
    """Adds default fields so format strings never break."""
    def format(self, record: logging.LogRecord) -> str:
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        return super().format(record)