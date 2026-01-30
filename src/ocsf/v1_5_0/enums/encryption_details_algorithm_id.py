"""The encryption algorithm used. enumeration."""

from enum import IntEnum


class EncryptionDetailsAlgorithmId(IntEnum):
    """The encryption algorithm used.

    See: https://schema.ocsf.io/1.5.0/data_types/encryption_details_algorithm_id
    """

    DES = 1  # Data Encryption Standard Algorithm
    TRIPLEDES = 2  # Triple Data Encryption Standard Algorithm
    AES = 3  # Advanced Encryption Standard Algorithm.
    RSA = 4  # Rivest-Shamir-Adleman Algorithm
    ECC = 5  # Elliptic Curve Cryptography Algorithm
    SM2 = 6  # ShangMi Cryptographic Algorithm
