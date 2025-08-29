from typing import ClassVar

from ocsf.events.discovery.discovery_result import DiscoveryResult
from ocsf.objects.kernel import Kernel


class KernelObjectQuery(DiscoveryResult):
    schema_name: ClassVar[str] = "kernel_object_query"
    class_id: int = 5006
    class_name: str = "Kernel Object Query"

    # Required
    kernel: Kernel
