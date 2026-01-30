"""The normalized state identifier of a security finding. enumeration."""

from enum import IntEnum


class SecurityFindingStateId(IntEnum):
    """The normalized state identifier of a security finding.

    See: https://schema.ocsf.io/1.1.0/data_types/security_finding_state_id
    """

    NEW = 1  # The finding is new and yet to be reviewed.
    IN_PROGRESS = 2  # The finding is under review.
    SUPPRESSED = (
        3  # The finding was reviewed, considered as a false positive and is now suppressed.
    )
    RESOLVED = 4  # The finding was reviewed and remediated and is now considered resolved.
