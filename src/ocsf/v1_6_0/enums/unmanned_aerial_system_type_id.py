"""The UAS type identifier. enumeration."""

from enum import IntEnum


class UnmannedAerialSystemTypeId(IntEnum):
    """The UAS type identifier.

    See: https://schema.ocsf.io/1.6.0/data_types/unmanned_aerial_system_type_id
    """

    UNKNOWN_UNDECLARED = 0  # The UAS type is empty or not declared.
    AIRPLANE = 1  #
    HELICOPTER = 2  # Can also be a Multi-rotor Unmanned Aircraft (e.g., Quad-copter).
    GYROPLANE = 3  #
    HYBRID_LIFT = 4  # Fixed wing aircraft that can take off vertically.
    ORNITHOPTER = 5  #
    GLIDER = 6  #
    KITE = 7  #
    FREE_BALLOON = 8  #
    CAPTIVE_BALLOON = 9  #
    AIRSHIP = 10  # E.g., a blimp.
    FREE_FALL_PARACHUTE = 11  # Parachutes, or objects without any power or propulsion mechanism.
    ROCKET = 12  #
    TETHERED_POWERED_AIRCRAFT = 13  #
    GROUND_OBSTACLE = 14  #
    OTHER = 99  #
