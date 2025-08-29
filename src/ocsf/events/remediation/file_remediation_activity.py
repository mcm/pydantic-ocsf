from typing import ClassVar

from ocsf.events.remediation.remediation_activity import RemediationActivity
from ocsf.objects.file import File


class FileRemediationActivity(RemediationActivity):
    schema_name: ClassVar[str] = "file_remediation_activity"
    class_id: int = 7002
    class_name: str = "File Remediation Activity"

    # Required
    file: File
