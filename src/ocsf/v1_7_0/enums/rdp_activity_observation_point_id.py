"""The normalized identifier of the observation point. The observation point identifier indicates whether the source network endpoint, destination network endpoint, or neither served as the observation point for the activity. enumeration."""

from enum import IntEnum


class RdpActivityObservationPointId(IntEnum):
    """The normalized identifier of the observation point. The observation point identifier indicates whether the source network endpoint, destination network endpoint, or neither served as the observation point for the activity.

    See: https://schema.ocsf.io/1.7.0/data_types/rdp_activity_observation_point_id
    """

    UNKNOWN = 0  # The observation point is unknown.
    SOURCE = 1  # The source network endpoint is the observation point.
    DESTINATION = 2  # The destination network endpoint is the observation point.
    NEITHER = 3  # Neither the source nor destination network endpoint is the observation point.
    BOTH = 4  # Both the source and destination network endpoint are the observation point. This typically occurs in localhost or internal communications where the source and destination are the same endpoint, often resulting in a <code>connection_info.direction</code> of <code>Local</code>.
    OTHER = 99  # The observation point is not mapped. See the <code>observation_point</code> attribute for a data source specific value.
