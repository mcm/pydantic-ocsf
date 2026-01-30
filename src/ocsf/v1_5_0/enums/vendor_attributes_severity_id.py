"""The finding severity ID, as reported by the Vendor (Finding Provider). enumeration."""

from enum import IntEnum


class VendorAttributesSeverityId(IntEnum):
    """The finding severity ID, as reported by the Vendor (Finding Provider).

    See: https://schema.ocsf.io/1.5.0/data_types/vendor_attributes_severity_id
    """

    UNKNOWN = 0  # The event/finding severity is unknown.
    INFORMATIONAL = 1  # Informational message. No action required.
    LOW = 2  # The user decides if action is needed.
    MEDIUM = 3  # Action is required but the situation is not serious at this time.
    HIGH = 4  # Action is required immediately.
    CRITICAL = 5  # Action is required immediately and the scope is broad.
    FATAL = 6  # An error occurred but it is too late to take remedial action.
    OTHER = 99  # The event/finding severity is not mapped. See the <code>severity</code> attribute, which contains a data source specific value.
