"""The normalized identifier of the authentication type used to authorize a flight plan or mission. enumeration."""

from enum import IntEnum


class DroneFlightsActivityAuthProtocolId(IntEnum):
    """The normalized identifier of the authentication type used to authorize a flight plan or mission.

    See: https://schema.ocsf.io/1.6.0/data_types/drone_flights_activity_auth_protocol_id
    """

    UNKNOWN = 0  # The authentication type is unknown.
    NONE_ = 1  #
    UAS_ID_SIGNATURE = 2  #
    OPERATOR_ID_SIGNATURE = 3  #
    MESSAGE_SET_SIGNATURE = 4  #
    AUTHENTICATION_PROVIDED_BY_NETWORK_REMOTE_ID = 5  #
    SPECIFIC_AUTHENTICATION_METHOD = 6  #
    RESERVED = 7  #
    PRIVATE_USER = 8  #
    OTHER = 99  # The authentication type is not mapped. See the <code>auth_protocol</code> attribute, which contains a data source specific value.
