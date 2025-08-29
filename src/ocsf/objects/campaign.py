from typing import ClassVar

from ocsf.objects.object import Object


class Campaign(Object):
    schema_name: ClassVar[str] = "campaign"

    # Required
    name: str
