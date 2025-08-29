from typing import ClassVar

from ocsf.objects._entity import Entity


class Extension(Entity):
    schema_name: ClassVar[str] = "extension"

    # Required
    name: str
    uid: str
    version: str
