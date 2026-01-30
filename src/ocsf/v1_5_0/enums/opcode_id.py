"""The DNS opcode ID specifies the normalized query message type as defined in <a target='_blank' href='https://www.rfc-editor.org/rfc/rfc5395.html'>RFC-5395</a>. enumeration."""

from enum import IntEnum


class OpcodeId(IntEnum):
    """The DNS opcode ID specifies the normalized query message type as defined in <a target='_blank' href='https://www.rfc-editor.org/rfc/rfc5395.html'>RFC-5395</a>.

    See: https://schema.ocsf.io/1.5.0/data_types/opcode_id
    """

    QUERY = 0  # Standard query
    INVERSE_QUERY = 1  # Inverse query, obsolete
    STATUS = 2  # Server status request
    RESERVED = 3  # Reserved, not used
    NOTIFY = 4  # Zone change notification
    UPDATE = 5  # Dynamic DNS update
    DSO_MESSAGE = 6  # DNS Stateful Operations (DSO)
    OTHER = 99  # The DNS Opcode is not defined by the RFC. See the <code>opcode</code> attribute, which contains a data source specific value.
