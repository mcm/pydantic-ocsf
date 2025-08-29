from datetime import datetime
from typing import ClassVar

from ocsf.objects._entity import Entity
from ocsf.objects.group import Group


class Table(Entity):
    schema_name: ClassVar[str] = "table"

    # Recommended
    name: str | None = None
    uid: str | None = None

    # Optional
    created_time: datetime | None = None
    desc: str | None = None
    groups: list[Group] | None = None
    modified_time: datetime | None = None
    size: int | None = None
