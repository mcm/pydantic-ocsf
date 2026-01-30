"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class ScriptActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.7.0/data_types/script_activity_activity_id
    """

    EXECUTE = 1  #
