from typing import ClassVar

from pydantic import BaseModel


class AnalysisTarget(BaseModel):
    schema_name: ClassVar[str] = "analysis_target"

    # Required
    name: str

    # Optional
    type_: str | None = None
