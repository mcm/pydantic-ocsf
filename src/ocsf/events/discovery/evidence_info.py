from typing import ClassVar

from pydantic import model_validator

from ocsf.events.discovery.discovery_result import DiscoveryResult
from ocsf.objects.device import Device
from ocsf.objects.query_evidence import QueryEvidence


class EvidenceInfo(DiscoveryResult):
    schema_name: ClassVar[str] = "evidence_info"
    class_id: int = 5040
    class_name: str = "Live Evidence Info"

    # Required
    device: Device
    query_evidence: QueryEvidence

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(getattr(self, field) is None for field in ["device.hostname", "device.mac", "device.name"]):
            raise ValueError("At least one of `device.hostname`, `device.mac`, `device.name` must be provided")
        return self
