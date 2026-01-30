"""The type of the Managed Entity. It is recommended to also populate the <code>type</code> attribute with the associated label, or the source specific name if <code>Other</code>. enumeration."""

from enum import IntEnum


class ManagedEntityTypeId(IntEnum):
    """The type of the Managed Entity. It is recommended to also populate the <code>type</code> attribute with the associated label, or the source specific name if <code>Other</code>.

    See: https://schema.ocsf.io/1.7.0/data_types/managed_entity_type_id
    """

    DEVICE = 1  # A managed Device entity.  This item corresponds to population of the <code>device</code> attribute.
    USER = 2  # A managed User entity.  This item corresponds to population of the <code>user</code> attribute.
    GROUP = 3  # A managed Group entity.  This item corresponds to population of the <code>group</code> attribute.
    ORGANIZATION = 4  # A managed Organization entity.  This item corresponds to population of the <code>org</code> attribute.
    POLICY = 5  # A managed Policy entity.  This item corresponds to population of the <code>policy</code> attribute.
    EMAIL = 6  # A managed Email entity.  This item corresponds to population of the <code>email</code> attribute.
    NETWORK_ZONE = 7  # A managed Network Zone entity. Populate the <code>name</code> attribute with the zone name and/or the <code>uid</code> attribute with the zone ID. Additional zone information can be added to the <code>data</code> attribute.
