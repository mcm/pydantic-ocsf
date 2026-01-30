"""The normalized status identifier indicating the applicability of this policy restriction. enumeration."""

from enum import IntEnum


class AdditionalRestrictionStatusId(IntEnum):
    """The normalized status identifier indicating the applicability of this policy restriction.

    See: https://schema.ocsf.io/1.6.0/data_types/additional_restriction_status_id
    """

    APPLICABLE = 1  # This restriction is currently applicable and being enforced.
    INAPPLICABLE = 2  # This restriction is not applicable.
    EVALUATION_ERROR = 3  # This restriction could not be properly evaluated due to an error.
