"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class DnsActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.1.0/data_types/dns_activity_activity_id
    """

    QUERY = 1  # The DNS query request.
    RESPONSE = 2  # The DNS query response.
    TRAFFIC = 6  # Bidirectional DNS request and response traffic.
