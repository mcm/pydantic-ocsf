from typing import ClassVar

from ocsf.events.discovery.discovery_result import DiscoveryResult
from ocsf.objects.process import Process


class ProcessQuery(DiscoveryResult):
    schema_name: ClassVar[str] = "process_query"
    class_id: int = 5015
    class_name: str = "Process Query"

    # Required
    process: Process
