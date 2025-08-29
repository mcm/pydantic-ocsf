from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.certificate import Certificate
from ocsf.objects.fingerprint import Fingerprint
from ocsf.objects.object import Object


class AlgorithmId(Enum):
    UNKNOWN = 0
    DSA = 1
    RSA = 2
    ECDSA = 3
    AUTHENTICODE = 4
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return AlgorithmId[obj]
        else:
            return AlgorithmId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "DSA": "DSA",
            "RSA": "RSA",
            "ECDSA": "ECDSA",
            "AUTHENTICODE": "Authenticode",
            "OTHER": "Other",
        }
        return name_map[super().name]


class StateId(Enum):
    UNKNOWN = 0
    VALID = 1
    EXPIRED = 2
    REVOKED = 3
    SUSPENDED = 4
    PENDING = 5
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return StateId[obj]
        else:
            return StateId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "VALID": "Valid",
            "EXPIRED": "Expired",
            "REVOKED": "Revoked",
            "SUSPENDED": "Suspended",
            "PENDING": "Pending",
            "OTHER": "Other",
        }
        return name_map[super().name]


class DigitalSignature(Object):
    schema_name: ClassVar[str] = "digital_signature"

    # Required
    algorithm_id: AlgorithmId

    # Recommended
    certificate: Certificate | None = None

    # Optional
    algorithm: str | None = None
    created_time: datetime | None = None
    developer_uid: str | None = None
    digest: Fingerprint | None = None
    state: str | None = None
    state_id: StateId | None = None
