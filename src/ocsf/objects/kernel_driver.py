from typing import ClassVar

from ocsf.objects.file import File
from ocsf.objects.object import Object


class KernelDriver(Object):
    allowed_profiles: ClassVar[None] = None
    schema_name: ClassVar[str] = "kernel_driver"

    # Required
    file: File
