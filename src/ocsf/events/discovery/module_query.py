from typing import ClassVar

from ocsf.events.discovery.discovery_result import DiscoveryResult
from ocsf.objects.module import Module
from ocsf.objects.process import Process


class ModuleQuery(DiscoveryResult):
    schema_name: ClassVar[str] = "module_query"
    class_id: int = 5011
    class_name: str = "Module Query"

    # Required
    module: Module
    process: Process
