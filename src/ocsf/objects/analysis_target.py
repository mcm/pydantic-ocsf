from typing import ClassVar

from ocsf.ocsf_object import OcsfObject


class AnalysisTarget(OcsfObject):
    allowed_profiles: ClassVar[None] = None
    schema_name: ClassVar[str] = "analysis_target"

    # Required
    name: str

    # Optional
    type_: str | None = None
