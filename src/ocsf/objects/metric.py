from typing import ClassVar

from ocsf.objects.object import Object


class Metric(Object):
    schema_name: ClassVar[str] = "metric"

    # Required
    name: str
    value: str
