from typing import ClassVar

from ocsf.ocsf_object import OcsfObject


class Object(OcsfObject):
    allowed_profiles: ClassVar[None] = None
    schema_name: ClassVar[str] = "object"
