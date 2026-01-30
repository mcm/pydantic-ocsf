"""The normalized priority. Priority identifies the relative importance of the incident or finding. It is a measurement of urgency. enumeration."""

from enum import IntEnum


class IncidentFindingPriorityId(IntEnum):
    """The normalized priority. Priority identifies the relative importance of the incident or finding. It is a measurement of urgency.

    See: https://schema.ocsf.io/1.7.0/data_types/incident_finding_priority_id
    """

    UNKNOWN = 0  # No priority is assigned.
    LOW = 1  # Application or personal procedure is unusable, where a workaround is available or a repair is possible.
    MEDIUM = 2  # Non-critical function or procedure is unusable or hard to use causing operational disruptions with no direct impact on a service's availability. A workaround is available.
    HIGH = 3  # Critical functionality or network access is interrupted, degraded or unusable, having a severe impact on services availability. No acceptable alternative is possible.
    CRITICAL = 4  # Interruption making a critical functionality inaccessible or a complete network interruption causing a severe impact on services availability. There is no possible alternative.
    OTHER = 99  # The priority is not normalized.
