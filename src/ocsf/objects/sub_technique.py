from typing import ClassVar

from pydantic import AnyUrl

from ocsf.objects._entity import Entity


class SubTechnique(Entity):
    schema_name: ClassVar[str] = "sub_technique"

    # Recommended
    name: str | None = None
    uid: str | None = None

    # Optional
    src_url: AnyUrl | None = None
