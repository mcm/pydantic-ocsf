"""The normalized identifier for the ticket status. enumeration."""

from enum import IntEnum


class TicketStatusId(IntEnum):
    """The normalized identifier for the ticket status.

    See: https://schema.ocsf.io/1.7.0/data_types/ticket_status_id
    """

    NEW = 1  # The ticket is new and yet to be reviewed.
    IN_PROGRESS = 2  # The ticket is actively being worked on.
    NOTIFIED = 3  # Relevant parties have been notified about the ticket.
    ON_HOLD = 4  # Work on the ticket is temporarily suspended.
    RESOLVED = 5  # The ticket is resolved and a solution is implemented, pending confirmation or verification from the requestor.
    CLOSED = 6  # The ticket has been completed and closed.
    CANCELED = 7  # The ticket has been canceled and will not be processed.
    REOPENED = 8  # The ticket was previously closed, but has been reopened.
