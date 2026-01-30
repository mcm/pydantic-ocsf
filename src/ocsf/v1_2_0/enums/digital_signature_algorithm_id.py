"""The identifier of the normalized digital signature algorithm. enumeration."""

from enum import IntEnum


class DigitalSignatureAlgorithmId(IntEnum):
    """The identifier of the normalized digital signature algorithm.

    See: https://schema.ocsf.io/1.2.0/data_types/digital_signature_algorithm_id
    """

    UNKNOWN = 0  #
    DSA = 1  # Digital Signature Algorithm (DSA).
    RSA = 2  # Rivest-Shamir-Adleman (RSA) Algorithm.
    ECDSA = 3  # Elliptic Curve Digital Signature Algorithm.
    AUTHENTICODE = 4  # Microsoft Authenticode Digital Signature Algorithm.
    OTHER = 99  #
