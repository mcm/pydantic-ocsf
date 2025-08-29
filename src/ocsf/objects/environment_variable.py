from typing import ClassVar

from ocsf.objects.object import Object


class EnvironmentVariable(Object):
    allowed_profiles: ClassVar[None] = None
    schema_name: ClassVar[str] = "environment_variable"

    # Required
    name: str
    value: str
