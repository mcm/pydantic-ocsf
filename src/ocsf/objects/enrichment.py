from datetime import datetime
from typing import Any, ClassVar

from pydantic import AnyUrl

from ocsf.objects.object import Object
from ocsf.objects.reputation import Reputation


class Enrichment(Object):
    schema_name: ClassVar[str] = "enrichment"

    # Required
    data: dict[str, Any]
    name: str
    value: str

    # Recommended
    created_time: datetime | None = None
    provider: str | None = None
    short_desc: str | None = None
    src_url: AnyUrl | None = None
    type_: str | None = None

    # Optional
    desc: str | None = None
    reputation: Reputation | None = None
