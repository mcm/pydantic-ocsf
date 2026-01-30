"""The normalized state ID of the Identity Provider to reflect its configuration or activation status. enumeration."""

from enum import IntEnum


class IdpStateId(IntEnum):
    """The normalized state ID of the Identity Provider to reflect its configuration or activation status.

    See: https://schema.ocsf.io/1.6.0/data_types/idp_state_id
    """

    UNKNOWN = 0  # The configuration state of the Identity Provider is unknown.
    ACTIVE = 1  # The Identity Provider is in an Active state, or otherwise enabled.
    SUSPENDED = 2  # The Identity Provider is in a Suspended state.
    DEPRECATED = 3  # The Identity Provider is in a Deprecated state, or is otherwise disabled.
    DELETED = 4  # The Identity Provider is in a Deleted state.
    OTHER = 99  # The configuration state of the Identity Provider is not mapped. See the <code>state</code> attribute, which contains a data source specific value.
