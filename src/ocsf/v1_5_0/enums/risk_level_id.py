"""The normalized risk level id. enumeration."""

from enum import IntEnum


class RiskLevelId(IntEnum):
    """The normalized risk level id.

    See: https://schema.ocsf.io/1.5.0/data_types/risk_level_id
    """

    INFO = 0  #
    LOW = 1  #
    MEDIUM = 2  #
    HIGH = 3  #
    CRITICAL = 4  #
    OTHER = 99  # The risk level is not mapped. See the <code>risk_level</code> attribute, which contains a data source specific value.
