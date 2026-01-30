"""The normalized identifier of the signature state. enumeration."""

from enum import IntEnum


class DigitalSignatureStateId(IntEnum):
    """The normalized identifier of the signature state.

    See: https://schema.ocsf.io/1.7.0/data_types/digital_signature_state_id
    """

    VALID = 1  # The digital signature is valid.
    EXPIRED = 2  # The digital signature is invalid because its timestamp does not fall within the certificate's validity period.
    REVOKED = 3  # The digital signature is invalid due to certificate revocation.
    SUSPENDED = 4  # The digital signature is invalid due to certificate suspension.
    PENDING = 5  # The digital signature state is pending.
    UNTRUSTED = 6  # The digital signature is invalid because the certificate is rooted in an untrusted CA or is an untrusted self-signed certificate.
    DISTRUSTED = 7  # The digital signature is invalid because the certificate is explicitly distrusted. Note that whereas revocation is global, distrust reflects local IT/security policy.
    WRONGUSAGE = 8  # The digital signature is invalid because the certificate is not intended for code signing purposes.
    BAD = 9  # The digital signature is cryptographically invalid, e.g. a mismatched digest. This indicates possible tampering.
    BROKEN = 10  # The digital signature is malformed and could not be processed.
