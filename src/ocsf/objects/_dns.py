from typing import ClassVar

from ocsf.objects.object import Object


class Dns(Object):
    schema_name: ClassVar[str] = "_dns"

    # Recommended
    class_: str | None = None
    packet_uid: int | None = None
    type_: str | None = None
