from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.object import Object


class AlgorithmId(Enum):
    UNKNOWN = 0
    DES = 1
    TRIPLEDES = 2
    AES = 3
    RSA = 4
    ECC = 5
    SM2 = 6
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
            "DES": "DES",
            "TRIPLEDES": "TripleDES",
            "AES": "AES",
            "RSA": "RSA",
            "ECC": "ECC",
            "SM2": "SM2",
            "OTHER": "Other",
        }
        return name_map[super().name]


class EncryptionDetails(Object):
    schema_name: ClassVar[str] = "encryption_details"

    # Recommended
    algorithm_id: AlgorithmId | None = None
    type_: str | None = None

    # Optional
    algorithm: str | None = None
    key_length: int | None = None
    key_uid: str | None = None
