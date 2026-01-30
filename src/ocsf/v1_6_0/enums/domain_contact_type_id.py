"""The normalized domain contact type ID. enumeration."""

from enum import IntEnum


class DomainContactTypeId(IntEnum):
    """The normalized domain contact type ID.

    See: https://schema.ocsf.io/1.6.0/data_types/domain_contact_type_id
    """

    REGISTRANT = 1  # The contact information provided is for the domain registrant.
    ADMINISTRATIVE = 2  # The contact information provided is for the domain administrator.
    TECHNICAL = 3  # The contact information provided is for the domain technical lead.
    BILLING = 4  # The contact information provided is for the domain billing lead.
    ABUSE = 5  # The contact information provided is for the domain abuse contact.
