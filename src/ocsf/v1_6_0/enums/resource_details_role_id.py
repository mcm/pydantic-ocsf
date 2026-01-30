"""The normalized identifier of the resource's role in the context of the event or finding. enumeration."""

from enum import IntEnum


class ResourceDetailsRoleId(IntEnum):
    """The normalized identifier of the resource's role in the context of the event or finding.

    See: https://schema.ocsf.io/1.6.0/data_types/resource_details_role_id
    """

    TARGET = 1  # The resource is the primary target or subject of the event/finding.
    ACTOR = 2  # The resource is acting as the initiator or performer in the context of the event/finding.
    AFFECTED = 3  # The resource was impacted or affected by the event/finding.
    RELATED = 4  # The resource is related to or associated with the event/finding.
