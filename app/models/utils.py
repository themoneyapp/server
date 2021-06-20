from datetime import datetime
from uuid import uuid1


__all__ = (
    "get_default_uuid",
    "get_current_datetime",
)


def get_current_datetime() -> datetime:
    """Get the current datetime.utcnow"""
    return datetime.utcnow()


def get_default_uuid() -> str:
    """Get a random uuid as string"""
    return str(uuid1())
