from typing import ClassVar

from ocsf.objects.package import Package
from ocsf.objects.remediation import Remediation


class AffectedPackage(Package):
    schema_name: ClassVar[str] = "affected_package"

    # Optional
    fixed_in_version: str | None = None
    path: str | None = None
    remediation: Remediation | None = None
