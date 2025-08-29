from typing import ClassVar

from ocsf.objects._entity import Entity


class Organization(Entity):
    schema_name: ClassVar[str] = "organization"

    # Recommended
    name: str | None = None
    ou_name: str | None = None
    uid: str | None = None

    # Optional
    ou_uid: str | None = None
