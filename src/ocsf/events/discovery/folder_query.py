from typing import ClassVar

from ocsf.events.discovery.discovery_result import DiscoveryResult
from ocsf.objects.file import File


class FolderQuery(DiscoveryResult):
    schema_name: ClassVar[str] = "folder_query"
    class_id: int = 5008
    class_name: str = "Folder Query"

    # Required
    folder: File
