"""The normalized identifier of the relationship between two software components. enumeration."""

from enum import IntEnum


class RelationshipId(IntEnum):
    """The normalized identifier of the relationship between two software components.

    See: https://schema.ocsf.io/1.7.0/data_types/relationship_id
    """

    UNKNOWN = 0  # The relationship is unknown.
    DEPENDS_ON = 1  # The component is a dependency of another component. Can be used to define both direct and transitive dependencies.
    OTHER = 99  # The relationship is not mapped. See the <code>relationship</code> attribute, which contains a data source specific value.
