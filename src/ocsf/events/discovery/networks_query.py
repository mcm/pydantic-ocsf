from typing import ClassVar

from ocsf.events.discovery.discovery_result import DiscoveryResult
from ocsf.objects.network_interface import NetworkInterface


class NetworksQuery(DiscoveryResult):
    schema_name: ClassVar[str] = "networks_query"
    class_id: int = 5013
    class_name: str = "Networks Query"

    # Required
    network_interfaces: list[NetworkInterface]
