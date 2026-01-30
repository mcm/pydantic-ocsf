"""The normalized status identifier of the Finding, set by the consumer. enumeration."""

from enum import IntEnum


class ComplianceFindingStatusId(IntEnum):
    """The normalized status identifier of the Finding, set by the consumer.

    See: https://schema.ocsf.io/1.5.0/data_types/compliance_finding_status_id
    """

    NEW = 1  # The Finding is new and yet to be reviewed.
    IN_PROGRESS = 2  # The Finding is under review.
    SUPPRESSED = 3  # The Finding was reviewed, determined to be benign or a false positive and is now suppressed.
    RESOLVED = 4  # The Finding was reviewed, remediated and is now considered resolved.
    ARCHIVED = 5  # The Finding was archived.
