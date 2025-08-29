from typing import ClassVar

from ocsf.objects._entity import Entity


class Feature(Entity):
    allowed_profiles: ClassVar[None] = None
    schema_name: ClassVar[str] = "feature"

    # Recommended
    name: str | None = None
    uid: str | None = None
    version: str | None = None
