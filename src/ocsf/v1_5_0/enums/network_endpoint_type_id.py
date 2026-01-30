"""The network endpoint type ID. enumeration."""

from enum import IntEnum


class NetworkEndpointTypeId(IntEnum):
    """The network endpoint type ID.

    See: https://schema.ocsf.io/1.5.0/data_types/network_endpoint_type_id
    """

    UNKNOWN = 0  # The type is unknown.
    OTHER = 99  # The type is not mapped. See the <code>type</code> attribute, which contains a data source specific value.
