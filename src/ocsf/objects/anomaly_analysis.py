from typing import ClassVar

from pydantic import BaseModel

from ocsf.objects.analysis_target import AnalysisTarget
from ocsf.objects.anomaly import Anomaly
from ocsf.objects.baseline import Baseline


class AnomalyAnalysis(BaseModel):
    schema_name: ClassVar[str] = "anomaly_analysis"

    # Required
    analysis_targets: list[AnalysisTarget]
    anomalies: list[Anomaly]

    # Recommended
    baselines: list[Baseline] | None = None
