"""The normalized impact of the finding. enumeration."""

from enum import IntEnum


class ImpactId(IntEnum):
    """The normalized impact of the finding.

    See: https://schema.ocsf.io/1.2.0/data_types/impact_id
    """

    UNKNOWN = 0  # The normalized impact is unknown.
    LOW = 1  #
    MEDIUM = 2  #
    HIGH = 3  #
    CRITICAL = 4  #
    OTHER = 99  # The impact is not mapped. See the <code>impact</code> attribute, which contains a data source specific value.
