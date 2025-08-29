from typing import ClassVar

from ocsf.events.remediation.remediation_activity import RemediationActivity
from ocsf.objects.network_connection_info import NetworkConnectionInfo


class NetworkRemediationActivity(RemediationActivity):
    schema_name: ClassVar[str] = "network_remediation_activity"
    class_id: int = 7004
    class_name: str = "Network Remediation Activity"

    # Required
    connection_info: NetworkConnectionInfo
