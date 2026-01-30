"""The normalized status identifier of the Incident. enumeration."""

from enum import IntEnum


class IncidentFindingStatusId(IntEnum):
    """The normalized status identifier of the Incident.

    See: https://schema.ocsf.io/1.2.0/data_types/incident_finding_status_id
    """

    NEW = 1  # The service desk has received the incident but has not assigned it to an agent.
    IN_PROGRESS = 2  # The incident has been assigned to an agent but has not been resolved. The agent is actively working with the user to diagnose and resolve the incident.
    ON_HOLD = (
        3  # The incident requires some information or response from the user or from a third party.
    )
    RESOLVED = 4  # The service desk has confirmed that the incident is resolved.
    CLOSED = 5  # The incident is resolved and no further action is necessary.
