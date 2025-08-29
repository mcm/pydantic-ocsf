from typing import ClassVar

from ocsf.events.discovery.discovery_result import DiscoveryResult
from ocsf.objects.file import File


class FileQuery(DiscoveryResult):
    schema_name: ClassVar[str] = "file_query"
    class_id: int = 5007
    class_name: str = "File Query"

    # Required
    file: File
