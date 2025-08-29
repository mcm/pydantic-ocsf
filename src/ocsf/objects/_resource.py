from datetime import datetime
from typing import Any, ClassVar

from ocsf.objects._entity import Entity
from ocsf.objects.key_value_object import KeyValueObject


class Resource(Entity):
    schema_name: ClassVar[str] = "_resource"

    # Recommended
    name: str | None = None
    uid: str | None = None

    # Optional
    created_time: datetime | None = None
    data: dict[str, Any] | None = None
    labels: list[str] | None = None
    modified_time: datetime | None = None
    tags: list[KeyValueObject] | None = None
    type_: str | None = None
    uid_alt: str | None = None
