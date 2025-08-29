from typing import ClassVar

from ocsf.events.discovery.discovery_result import DiscoveryResult
from ocsf.objects.peripheral_device import PeripheralDevice


class PeripheralDeviceQuery(DiscoveryResult):
    schema_name: ClassVar[str] = "peripheral_device_query"
    class_id: int = 5014
    class_name: str = "Peripheral Device Query"

    # Required
    peripheral_device: PeripheralDevice
