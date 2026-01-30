"""The type of software package. enumeration."""

from enum import IntEnum


class AffectedPackageTypeId(IntEnum):
    """The type of software package.

    See: https://schema.ocsf.io/1.7.0/data_types/affected_package_type_id
    """

    APPLICATION = 1  # An application software package.
    OPERATING_SYSTEM = 2  # An operating system software package.
