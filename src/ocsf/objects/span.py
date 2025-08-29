from datetime import datetime
from typing import ClassVar

from ocsf.objects.object import Object
from ocsf.objects.service import Service


class Span(Object):
    schema_name: ClassVar[str] = "span"

    # Required
    end_time: datetime
    start_time: datetime
    uid: str

    # Optional
    duration: int | None = None
    message: str | None = None
    operation: str | None = None
    parent_uid: str | None = None
    service: Service | None = None
    status_code: str | None = None
