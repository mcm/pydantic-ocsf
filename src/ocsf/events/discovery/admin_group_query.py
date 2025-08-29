from typing import ClassVar

from ocsf.events.discovery.discovery_result import DiscoveryResult
from ocsf.objects.group import Group
from ocsf.objects.user import User


class AdminGroupQuery(DiscoveryResult):
    schema_name: ClassVar[str] = "admin_group_query"
    class_id: int = 5009
    class_name: str = "Admin Group Query"

    # Required
    group: Group

    # Recommended
    users: list[User] | None = None
