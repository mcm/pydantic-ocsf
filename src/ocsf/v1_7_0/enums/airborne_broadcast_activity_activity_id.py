"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class AirborneBroadcastActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.7.0/data_types/airborne_broadcast_activity_activity_id
    """

    UNKNOWN = 0  # The event activity is unknown.
    CAPTURE = 1  # ADS-B information is being captured (collected).
    RECORD = 2  # ADS-B information is being recorded, for example by a standalone transceiver.
    OTHER = 99  # The event activity is not mapped. See the <code>activity_name</code> attribute, which contains a data source specific value.
