"""The operating area type identifier. enumeration."""

from enum import IntEnum


class UnmannedSystemOperatingAreaTypeId(IntEnum):
    """The operating area type identifier.

    See: https://schema.ocsf.io/1.7.0/data_types/unmanned_system_operating_area_type_id
    """

    UNKNOWN_UNDECLARED = 0  # The UA type is empty or not declared.
    TAKEOFF_LOCATION = 1  #
    FIXED_LOCATION = 2  #
    DYNAMIC_LOCATION = 3  #
    OTHER = 99  #
