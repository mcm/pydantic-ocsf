from typing import ClassVar

from ocsf.objects.object import Object


class San(Object):
    schema_name: ClassVar[str] = "san"

    # Required
    name: str
    type_: str
