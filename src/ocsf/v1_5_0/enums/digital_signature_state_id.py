"""The normalized identifier of the signature state. enumeration."""

from enum import IntEnum


class DigitalSignatureStateId(IntEnum):
    """The normalized identifier of the signature state.

    See: https://schema.ocsf.io/1.5.0/data_types/digital_signature_state_id
    """

    VALID = 1  # The digital signature is valid.
    EXPIRED = 2  # The digital signature is not valid due to expiration of certificate.
    REVOKED = 3  # The digital signature is invalid due to certificate revocation.
    SUSPENDED = 4  # The digital signature is invalid due to certificate suspension.
    PENDING = 5  # The digital signature state is pending.
