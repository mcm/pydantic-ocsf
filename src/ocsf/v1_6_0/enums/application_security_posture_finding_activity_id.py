"""The normalized identifier of the finding activity. enumeration."""

from enum import IntEnum


class ApplicationSecurityPostureFindingActivityId(IntEnum):
    """The normalized identifier of the finding activity.

    See: https://schema.ocsf.io/1.6.0/data_types/application_security_posture_finding_activity_id
    """

    CREATE = 1  # A finding was created.
    UPDATE = 2  # A finding was updated.
    CLOSE = 3  # A finding was closed.
