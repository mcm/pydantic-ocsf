from datetime import datetime
from typing import ClassVar

from ocsf.objects.object import Object
from ocsf.objects.service import Service
from ocsf.objects.span import Span


class Trace(Object):
    schema_name: ClassVar[str] = "trace"

    # Required
    uid: str

    # Optional
    duration: int | None = None
    end_time: datetime | None = None
    flags: list[str] | None = None
    service: Service | None = None
    span: Span | None = None
    start_time: datetime | None = None
