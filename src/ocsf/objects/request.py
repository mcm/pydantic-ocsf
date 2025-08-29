from typing import Any, ClassVar

from ocsf.objects.container import Container
from ocsf.objects.object import Object


class Request(Object):
    allowed_profiles: ClassVar[None] = None
    schema_name: ClassVar[str] = "request"

    # Required
    uid: str

    # Optional
    containers: list[Container] | None = None
    data: dict[str, Any] | None = None
    flags: list[str] | None = None
