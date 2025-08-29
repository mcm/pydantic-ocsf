from typing import ClassVar

from pydantic import AnyUrl

from ocsf.objects._entity import Entity


class D3FTechnique(Entity):
    schema_name: ClassVar[str] = "d3f_technique"

    # Recommended
    name: str | None = None
    uid: str | None = None

    # Optional
    src_url: AnyUrl | None = None
