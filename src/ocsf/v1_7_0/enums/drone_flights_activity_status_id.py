"""The normalized Operational status identifier for the Unmanned Aerial System (UAS). enumeration."""

from enum import IntEnum


class DroneFlightsActivityStatusId(IntEnum):
    """The normalized Operational status identifier for the Unmanned Aerial System (UAS).

    See: https://schema.ocsf.io/1.7.0/data_types/drone_flights_activity_status_id
    """

    UNDECLARED = 1  # The operational status is not reported.
    GROUND = 2  # The Unmanned Aerial System (UAS) is grounded.
    AIRBORNE = 3  # The Unmanned Aerial System (UAS) is airborne.
    EMERGENCY = 4  # The Unmanned Aerial System (UAS) is reporting an emergency status.
    REMOTE_ID_SYSTEM_FAILURE = 5  # The Unmanned Aerial System (UAS) is reporting the Remote ID beacon or device is malfunctioning or has failed.
    RESERVED = 6  # An ASTM Reserved status is reported.
