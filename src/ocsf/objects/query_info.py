from datetime import datetime
from typing import Any, ClassVar

from ocsf.objects._entity import Entity


class QueryInfo(Entity):
    schema_name: ClassVar[str] = "query_info"

    # Required
    query_string: str

    # Recommended
    name: str | None = None
    uid: str | None = None

    # Optional
    bytes: int | None = None
    data: dict[str, Any] | None = None
    query_time: datetime | None = None
