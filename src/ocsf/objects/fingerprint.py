from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.object import Object


class AlgorithmId(Enum):
    UNKNOWN = 0
    MD5 = 1
    SHA_1 = 2
    SHA_256 = 3
    SHA_512 = 4
    CTPH = 5
    TLSH = 6
    QUICKXORHASH = 7
    SHA_224 = 8
    SHA_384 = 9
    SHA_512_224 = 10
    SHA_512_256 = 11
    SHA3_224 = 12
    SHA3_256 = 13
    SHA3_384 = 14
    SHA3_512 = 15
    XXHASH_H3_64_BIT = 16
    XXHASH_H3_128_BIT = 17
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
            "MD5": "MD5",
            "SHA_1": "SHA-1",
            "SHA_256": "SHA-256",
            "SHA_512": "SHA-512",
            "CTPH": "CTPH",
            "TLSH": "TLSH",
            "QUICKXORHASH": "quickXorHash",
            "SHA_224": "SHA-224",
            "SHA_384": "SHA-384",
            "SHA_512_224": "SHA-512/224",
            "SHA_512_256": "SHA-512/256",
            "SHA3_224": "SHA3-224",
            "SHA3_256": "SHA3-256",
            "SHA3_384": "SHA3-384",
            "SHA3_512": "SHA3-512",
            "XXHASH_H3_64_BIT": "xxHash H3 64-bit",
            "XXHASH_H3_128_BIT": "xxHash H3 128-bit",
            "OTHER": "Other",
        }
        return name_map[super().name]


class Fingerprint(Object):
    schema_name: ClassVar[str] = "fingerprint"

    # Required
    algorithm_id: AlgorithmId
    value: str

    # Optional
    algorithm: str | None = None
