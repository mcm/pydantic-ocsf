"""The category unique identifier of the event. enumeration."""

from enum import IntEnum


class PatchStateCategoryUid(IntEnum):
    """The category unique identifier of the event.

    See: https://schema.ocsf.io/1.6.0/data_types/patch_state_category_uid
    """

    UNCATEGORIZED = 0  #
