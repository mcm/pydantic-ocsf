from typing import ClassVar

from ocsf.events.remediation.remediation_activity import RemediationActivity
from ocsf.objects.process import Process


class ProcessRemediationActivity(RemediationActivity):
    schema_name: ClassVar[str] = "process_remediation_activity"
    class_id: int = 7003
    class_name: str = "Process Remediation Activity"

    # Required
    process: Process
