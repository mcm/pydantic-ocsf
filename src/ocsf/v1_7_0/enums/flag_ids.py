"""The list of DNS answer header flag IDs. enumeration."""

from enum import IntEnum


class FlagIds(IntEnum):
    """The list of DNS answer header flag IDs.

    See: https://schema.ocsf.io/1.7.0/data_types/flag_ids
    """

    AUTHORITATIVE_ANSWER = 1  #
    TRUNCATED_RESPONSE = 2  #
    RECURSION_DESIRED = 3  #
    RECURSION_AVAILABLE = 4  #
    AUTHENTIC_DATA = 5  #
    CHECKING_DISABLED = 6  #
