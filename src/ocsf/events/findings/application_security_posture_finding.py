from typing import ClassVar

from pydantic import model_validator

from ocsf.events.findings.finding import Finding
from ocsf.objects.application import Application
from ocsf.objects.compliance import Compliance
from ocsf.objects.remediation import Remediation
from ocsf.objects.resource_details import ResourceDetails
from ocsf.objects.vulnerability import Vulnerability


class ApplicationSecurityPostureFinding(Finding):
    schema_name: ClassVar[str] = "application_security_posture_finding"
    class_id: int = 2007
    class_name: str = "Application Security Posture Finding"

    # Recommended
    application: Application | None = None
    compliance: Compliance | None = None
    remediation: Remediation | None = None
    resources: list[ResourceDetails] | None = None
    vulnerabilities: list[Vulnerability] | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(
            getattr(self, field) is None for field in ["application", "compliance", "remediation", "vulnerabilities"]
        ):
            raise ValueError(
                "At least one of `application`, `compliance`, `remediation`, `vulnerabilities` must be provided"
            )
        return self
