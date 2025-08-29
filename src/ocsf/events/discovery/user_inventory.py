from typing import ClassVar

from ocsf.events.discovery.discovery import Discovery
from ocsf.objects.actor import Actor
from ocsf.objects.user import User


class UserInventory(Discovery):
    schema_name: ClassVar[str] = "user_inventory"
    class_id: int = 5003
    class_name: str = "User Inventory Info"

    # Required
    user: User

    # Optional
    actor: Actor | None = None
