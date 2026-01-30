"""The normalized risk level id. enumeration."""

from enum import IntEnum


class SecurityFindingRiskLevelId(IntEnum):
    """The normalized risk level id.

    See: https://schema.ocsf.io/1.1.0/data_types/security_finding_risk_level_id
    """

    INFO = 0  #
    LOW = 1  #
    MEDIUM = 2  #
    HIGH = 3  #
    CRITICAL = 4  #
