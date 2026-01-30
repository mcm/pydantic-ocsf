"""The category unique identifier of the event. enumeration."""

from enum import IntEnum


class IncidentFindingCategoryUid(IntEnum):
    """The category unique identifier of the event.

    See: https://schema.ocsf.io/1.7.0/data_types/incident_finding_category_uid
    """

    UNCATEGORIZED = 0  #
