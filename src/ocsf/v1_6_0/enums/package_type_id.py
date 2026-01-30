"""The type of software package. enumeration."""

from enum import IntEnum


class PackageTypeId(IntEnum):
    """The type of software package.

    See: https://schema.ocsf.io/1.6.0/data_types/package_type_id
    """

    APPLICATION = 1  # An application software package.
    OPERATING_SYSTEM = 2  # An operating system software package.
