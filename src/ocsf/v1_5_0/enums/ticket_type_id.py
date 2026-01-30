"""The normalized identifier for the ticket type. enumeration."""

from enum import IntEnum


class TicketTypeId(IntEnum):
    """The normalized identifier for the ticket type.

    See: https://schema.ocsf.io/1.5.0/data_types/ticket_type_id
    """

    UNKNOWN = 0  #
    INTERNAL = 1  #
    EXTERNAL = 2  #
    OTHER = 99  #
