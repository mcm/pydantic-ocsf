from typing import ClassVar

from ocsf.events.discovery.discovery import Discovery
from ocsf.objects.actor import Actor
from ocsf.objects.device import Device


class InventoryInfo(Discovery):
    schema_name: ClassVar[str] = "inventory_info"
    class_id: int = 5001
    class_name: str = "Device Inventory Info"

    # Required
    device: Device

    # Optional
    actor: Actor | None = None
