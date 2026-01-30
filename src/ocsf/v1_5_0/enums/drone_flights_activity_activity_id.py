"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class DroneFlightsActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.5.0/data_types/drone_flights_activity_activity_id
    """

    UNKNOWN = 0  # The event activity is unknown.
    CAPTURE = 1  # Remote ID information from an Unmanned System is being captured (collected).
    RECORD = 2  # Unmanned System activity is being recorded.
    OTHER = 99  # The event activity is not mapped. See the <code>activity_name</code> attribute, which contains a data source specific value.
