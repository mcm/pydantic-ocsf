from typing import ClassVar

from ocsf.events.discovery.discovery_result import DiscoveryResult
from ocsf.objects.startup_item import StartupItem


class StartupItemQuery(DiscoveryResult):
    schema_name: ClassVar[str] = "startup_item_query"
    class_id: int = 5022
    class_name: str = "Startup Item Query"

    # Required
    startup_item: StartupItem
