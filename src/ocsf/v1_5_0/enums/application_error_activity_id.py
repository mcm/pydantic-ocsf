"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class ApplicationErrorActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.5.0/data_types/application_error_activity_id
    """

    GENERAL_ERROR = 1  # The application has experienced an error.
    TRANSLATION_ERROR = 2  # The application has experienced an error translating (mapping) a raw event to OCSF. Including the original raw event in the raw_data field is highly recommended.
