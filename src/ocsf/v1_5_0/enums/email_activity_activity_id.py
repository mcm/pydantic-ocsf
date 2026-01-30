"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class EmailActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.5.0/data_types/email_activity_activity_id
    """

    SEND = 1  #
    RECEIVE = 2  #
    SCAN = 3  # Email being scanned (example: security scanning)
    TRACE = 4  # Follow an email message as it travels through an organization. The <code>message_trace_uid</code> should be populated when selected.
