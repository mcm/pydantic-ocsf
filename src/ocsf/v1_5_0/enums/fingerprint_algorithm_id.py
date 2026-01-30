"""The identifier of the normalized hash algorithm, which was used to create the digital fingerprint. enumeration."""

from enum import IntEnum


class FingerprintAlgorithmId(IntEnum):
    """The identifier of the normalized hash algorithm, which was used to create the digital fingerprint.

    See: https://schema.ocsf.io/1.5.0/data_types/fingerprint_algorithm_id
    """

    UNKNOWN = 0  #
    MD5 = 1  # MD5 message-digest algorithm producing a 128-bit (16-byte) hash value.
    SHA_1 = 2  # Secure Hash Algorithm 1 producing a 160-bit (20-byte) hash value.
    SHA_256 = 3  # Secure Hash Algorithm 2 producing a 256-bit (32-byte) hash value.
    SHA_512 = 4  # Secure Hash Algorithm 2 producing a 512-bit (64-byte) hash value.
    CTPH = 5  # The ssdeep generated fuzzy checksum. Also known as Context Triggered Piecewise Hash (CTPH).
    TLSH = 6  # The TLSH fuzzy hashing algorithm.
    QUICKXORHASH = 7  # Microsoft simple non-cryptographic hash algorithm that works by XORing the bytes in a circular-shifting fashion.
    OTHER = 99  #
