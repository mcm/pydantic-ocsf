from typing import ClassVar

from ocsf.objects.object import Object


class HttpHeader(Object):
    schema_name: ClassVar[str] = "http_header"

    # Required
    name: str
    value: str
