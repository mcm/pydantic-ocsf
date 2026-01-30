"""The CVSS depth represents a depth of the equation used to calculate CVSS score. enumeration."""

from enum import IntEnum


class CvssDepth(IntEnum):
    """The CVSS depth represents a depth of the equation used to calculate CVSS score.

    See: https://schema.ocsf.io/1.0.0/data_types/cvss_depth
    """
