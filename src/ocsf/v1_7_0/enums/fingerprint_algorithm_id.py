"""The identifier of the normalized hash algorithm, which was used to create the digital fingerprint. enumeration."""

from enum import IntEnum


class FingerprintAlgorithmId(IntEnum):
    """The identifier of the normalized hash algorithm, which was used to create the digital fingerprint.

    See: https://schema.ocsf.io/1.7.0/data_types/fingerprint_algorithm_id
    """

    UNKNOWN = 0  #
    MD5 = 1  # MD5 message-digest algorithm producing a 128-bit (16-byte) hash value.
    SHA_1 = 2  # Secure Hash Algorithm 1 producing a 160-bit (20-byte) hash value.
    SHA_256 = 3  # Secure Hash Algorithm 2 producing a 256-bit (32-byte) hash value.
    SHA_512 = 4  # Secure Hash Algorithm 2 producing a 512-bit (64-byte) hash value.
    CTPH = 5  # The ssdeep generated fuzzy checksum. Also known as Context Triggered Piecewise Hash (CTPH).
    TLSH = 6  # The TLSH fuzzy hashing algorithm.
    QUICKXORHASH = 7  # Microsoft simple non-cryptographic hash algorithm that works by XORing the bytes in a circular-shifting fashion.
    SHA_224 = 8  # Secure Hash Algorithm 2 producing a 224-bit (28-byte) hash value.
    SHA_384 = 9  # Secure Hash Algorithm 2 producing a 384-bit (48-byte) hash value.
    SHA_512_224 = 10  # Secure Hash Algorithm 2 producing a 512-bit (64-byte) hash value truncated to a 224-bit (28-byte) hash value.
    SHA_512_256 = 11  # Secure Hash Algorithm 2 producing a 512-bit (64-byte) hash value truncated to a 256-bit (32-byte) hash value.
    SHA3_224 = 12  # Secure Hash Algorithm 3 producing a 224-bit (28-byte) hash value.
    SHA3_256 = 13  # Secure Hash Algorithm 3 producing a 256-bit (32-byte) hash value.
    SHA3_384 = 14  # Secure Hash Algorithm 3 producing a 384-bit (48-byte) hash value.
    SHA3_512 = 15  # Secure Hash Algorithm 3 producing a 512-bit (64-byte) hash value.
    XXHASH_H3_64_BIT = 16  # xxHash H3 producing a 64-bit hash value.
    XXHASH_H3_128_BIT = 17  # xxHash H3 producing a 128-bit hash value.
    OTHER = 99  #
