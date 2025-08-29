from datetime import datetime
from typing import ClassVar

from ocsf.objects.object import Object


class Epss(Object):
    schema_name: ClassVar[str] = "epss"

    # Required
    score: str

    # Recommended
    created_time: datetime | None = None
    version: str | None = None

    # Optional
    percentile: float | None = None
