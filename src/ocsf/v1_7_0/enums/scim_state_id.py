"""The normalized state ID of the SCIM resource to reflect its activation status. enumeration."""

from enum import IntEnum


class ScimStateId(IntEnum):
    """The normalized state ID of the SCIM resource to reflect its activation status.

    See: https://schema.ocsf.io/1.7.0/data_types/scim_state_id
    """

    UNKNOWN = 0  # The provisioning state of the SCIM resource is unknown.
    PENDING = 1  # The SCIM resource is Pending activation or creation.
    ACTIVE = 2  # The SCIM resource is in an Active state, or otherwise enabled.
    FAILED = 3  # The SCIM resource is in a Failed state.
    DELETED = 4  # The SCIM resource is in a Deleted state, or otherwise disabled.
    OTHER = 99  # The provisioning state of the SCIM resource is not mapped. See the <code>state</code> attribute, which contains a data source specific value.
