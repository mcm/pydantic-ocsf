"""The normalized datastore resource type identifier. enumeration."""

from enum import IntEnum


class ThreatActorTypeId(IntEnum):
    """The normalized datastore resource type identifier.

    See: https://schema.ocsf.io/1.5.0/data_types/threat_actor_type_id
    """

    UNKNOWN = 0  # The threat actor type is unknown.
    NATION_STATE = 1  #
    CYBERCRIMINAL = 2  #
    HACKTIVISTS = 3  #
    INSIDER = 4  #
    OTHER = 99  # The threat actor type is not mapped.
