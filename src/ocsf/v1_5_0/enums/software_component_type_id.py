"""The type of software component. enumeration."""

from enum import IntEnum


class SoftwareComponentTypeId(IntEnum):
    """The type of software component.

    See: https://schema.ocsf.io/1.5.0/data_types/software_component_type_id
    """

    FRAMEWORK = 1  # A software framework.
    LIBRARY = 2  # A software library.
    OPERATING_SYSTEM = 3  # An operating system. Useful for SBOMs of container images.
