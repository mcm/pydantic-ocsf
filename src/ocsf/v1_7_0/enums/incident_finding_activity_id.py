"""The normalized identifier of the Incident activity. enumeration."""

from enum import IntEnum


class IncidentFindingActivityId(IntEnum):
    """The normalized identifier of the Incident activity.

    See: https://schema.ocsf.io/1.7.0/data_types/incident_finding_activity_id
    """

    CREATE = 1  # Reports the creation of an Incident.
    UPDATE = 2  # Reports updates to an Incident.
    CLOSE = 3  # Reports closure of an Incident .
