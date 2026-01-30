"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class WebResourcesActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.0.0/data_types/web_resources_activity_activity_id
    """

    CREATE = 1  # One or more web resources were created.
    READ = 2  # One or more web resources were read / viewed.
    UPDATE = 3  # One or more web resources were updated.
    DELETE = 4  # One or more web resources were deleted.
    SEARCH = 5  # A search was performed on one or more web resources.
    IMPORT = 6  # One or more web resources were imported into an Application.
    EXPORT = 7  # One or more web resources were exported from an Application.
    SHARE = 8  # One or more web resources were shared.
