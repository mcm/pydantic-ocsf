"""<p>The direction of the email relative to the scanning host or organization.</p>Email scanned at an internet gateway might be characterized as inbound to the organization from the Internet, outbound from the organization to the Internet, or internal within the organization. Email scanned at a workstation might be characterized as inbound to, or outbound from the workstation. enumeration."""

from enum import IntEnum


class EmailActivityDirectionId(IntEnum):
    """<p>The direction of the email relative to the scanning host or organization.</p>Email scanned at an internet gateway might be characterized as inbound to the organization from the Internet, outbound from the organization to the Internet, or internal within the organization. Email scanned at a workstation might be characterized as inbound to, or outbound from the workstation.

    See: https://schema.ocsf.io/1.6.0/data_types/email_activity_direction_id
    """

    UNKNOWN = 0  # The email direction is unknown.
    INBOUND = 1  # Email Inbound, from the Internet or outside network destined for an entity inside network.
    OUTBOUND = 2  # Email Outbound, from inside the network destined for an entity outside network.
    INTERNAL = 3  # Email Internal, from inside the network destined for an entity inside network.
    OTHER = 99  #
