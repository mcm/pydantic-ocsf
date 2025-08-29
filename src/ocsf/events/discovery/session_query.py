from typing import ClassVar

from ocsf.events.discovery.discovery_result import DiscoveryResult
from ocsf.objects.session import Session


class SessionQuery(DiscoveryResult):
    schema_name: ClassVar[str] = "session_query"
    class_id: int = 5017
    class_name: str = "User Session Query"

    # Required
    session: Session
