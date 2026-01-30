"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class WebResourceAccessActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.6.0/data_types/web_resource_access_activity_activity_id
    """

    ACCESS_GRANT = 1  # The incoming request has permission to the web resource.
    ACCESS_DENY = 2  # The incoming request does not have permission to the web resource.
    ACCESS_REVOKE = (
        3  # The incoming request's access has been revoked due to security policy enforcements.
    )
    ACCESS_ERROR = 4  # An error occurred during processing the request.
