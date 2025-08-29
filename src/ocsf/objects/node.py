from typing import Any, ClassVar

from ocsf.objects.object import Object


class Node(Object):
    schema_name: ClassVar[str] = "node"

    # Required
    uid: str

    # Recommended
    name: str | None = None

    # Optional
    data: dict[str, Any] | None = None
    desc: str | None = None
    type_: str | None = None
