from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.attack import Attack
from ocsf.objects.key_value_object import KeyValueObject
from ocsf.objects.kill_chain_phase import KillChainPhase
from ocsf.objects.object import Object
from ocsf.objects.observable import Observable
from ocsf.objects.product import Product
from ocsf.objects.trait import Trait


class SeverityId(Enum):
    UNKNOWN = 0
    INFORMATIONAL = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5
    FATAL = 6
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return SeverityId[obj]
        else:
            return SeverityId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "INFORMATIONAL": "Informational",
            "LOW": "Low",
            "MEDIUM": "Medium",
            "HIGH": "High",
            "CRITICAL": "Critical",
            "FATAL": "Fatal",
            "OTHER": "Other",
        }
        return name_map[super().name]


class RelatedEvent(Object):
    schema_name: ClassVar[str] = "related_event"

    # Required
    uid: str

    # Recommended
    severity_id: SeverityId | None = None
    type_uid: int | None = None

    # Optional
    attacks: list[Attack] | None = None
    count: int | None = None
    created_time: datetime | None = None
    desc: str | None = None
    first_seen_time: datetime | None = None
    kill_chain: list[KillChainPhase] | None = None
    last_seen_time: datetime | None = None
    modified_time: datetime | None = None
    observables: list[Observable] | None = None
    product: Product | None = None
    product_uid: str | None = None
    severity: str | None = None
    status: str | None = None
    tags: list[KeyValueObject] | None = None
    title: str | None = None
    traits: list[Trait] | None = None
    type_: str | None = None
    type_name: str | None = None
