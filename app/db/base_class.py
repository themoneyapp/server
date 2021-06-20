from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()  # type: ignore
class Base(object):
    id: Any
    __name__: str
