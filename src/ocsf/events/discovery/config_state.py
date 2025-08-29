from typing import ClassVar

from ocsf.events.discovery.discovery import Discovery
from ocsf.objects.actor import Actor
from ocsf.objects.assessment import Assessment
from ocsf.objects.cis_benchmark_result import CisBenchmarkResult
from ocsf.objects.device import Device


class ConfigState(Discovery):
    schema_name: ClassVar[str] = "config_state"
    class_id: int = 5002
    class_name: str = "Device Config State"

    # Required
    device: Device

    # Recommended
    cis_benchmark_result: CisBenchmarkResult | None = None

    # Optional
    actor: Actor | None = None
    assessments: list[Assessment] | None = None
