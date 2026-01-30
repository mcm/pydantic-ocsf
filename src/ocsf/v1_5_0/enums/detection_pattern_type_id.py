"""Specifies the type of detection pattern used to identify the associated threat indicator. enumeration."""

from enum import IntEnum


class DetectionPatternTypeId(IntEnum):
    """Specifies the type of detection pattern used to identify the associated threat indicator.

    See: https://schema.ocsf.io/1.5.0/data_types/detection_pattern_type_id
    """

    UNKNOWN = 0  # The type is not mapped.
    STIX = 1  #
    PCRE = 2  #
    SIGMA = 3  #
    SNORT = 4  #
    SURICATA = 5  #
    YARA = 6  #
    OTHER = 99  # The detection pattern type is not mapped. See the <code>detection_pattern_type</code> attribute, which contains a data source specific value.
