from typing import ClassVar

from ocsf.events.discovery.discovery_result import DiscoveryResult
from ocsf.objects.service import Service


class ServiceQuery(DiscoveryResult):
    schema_name: ClassVar[str] = "service_query"
    class_id: int = 5016
    class_name: str = "Service Query"

    # Required
    service: Service
