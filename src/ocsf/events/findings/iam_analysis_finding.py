from typing import ClassVar

from pydantic import model_validator

from ocsf.events.findings.finding import Finding
from ocsf.objects.access_analysis_result import AccessAnalysisResult
from ocsf.objects.application import Application
from ocsf.objects.identity_activity_metrics import IdentityActivityMetrics
from ocsf.objects.permission_analysis_result import PermissionAnalysisResult
from ocsf.objects.remediation import Remediation
from ocsf.objects.resource_details import ResourceDetails
from ocsf.objects.user import User


class IAMAnalysisFinding(Finding):
    schema_name: ClassVar[str] = "iam_analysis_finding"
    class_id: int = 2008
    class_name: str = "IAM Analysis Finding"

    # Recommended
    applications: list[Application] | None = None
    identity_activity_metrics: IdentityActivityMetrics | None = None
    permission_analysis_results: list[PermissionAnalysisResult] | None = None
    resources: list[ResourceDetails] | None = None
    user: User | None = None

    # Optional
    access_analysis_result: AccessAnalysisResult | None = None
    remediation: Remediation | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(
            getattr(self, field) is None
            for field in [
                "access_analysis_result",
                "applications",
                "identity_activity_metrics",
                "permission_analysis_results",
            ]
        ):
            raise ValueError(
                "At least one of `access_analysis_result`, `applications`, `identity_activity_metrics`, `permission_analysis_results` must be provided"
            )
        return self
