"""The DNS opcode ID specifies the normalized query message type. enumeration."""

from enum import IntEnum


class DnsQueryOpcodeId(IntEnum):
    """The DNS opcode ID specifies the normalized query message type.

    See: https://schema.ocsf.io/1.1.0/data_types/dns_query_opcode_id
    """

    QUERY = 0  # Standard query
    INVERSE_QUERY = 1  # Inverse query, obsolete
    STATUS = 2  # Server status request
    RESERVED = 3  # Reserved, not used
    NOTIFY = 4  # Zone change notification
    UPDATE = 5  # Dynamic DNS update
    DSO_MESSAGE = 6  # DNS Stateful Operations (DSO)
