"""The normalized identifier of the activity that triggered the event. enumeration."""

from enum import IntEnum


class ScanActivityActivityId(IntEnum):
    """The normalized identifier of the activity that triggered the event.

    See: https://schema.ocsf.io/1.2.0/data_types/scan_activity_activity_id
    """

    STARTED = 1  # The scan was started.
    COMPLETED = 2  # The scan was completed.
    CANCELLED = 3  # The scan was cancelled.
    DURATION_VIOLATION = (
        4  # The allocated scan time was insufficient to complete the requested scan.
    )
    PAUSE_VIOLATION = 5  # The scan was paused, either by the user or by program constraints (e.g. scans that are suspended during certain time intervals), and not resumed within the allotted time.
    ERROR = 6  # The scan could not be completed due to an internal error.
    PAUSED = 7  # The scan was paused.
    RESUMED = 8  # The scan was resumed from the pause point.
    RESTARTED = 9  # The scan restarted from the beginning of the file enumeration.
    DELAYED = 10  # The user delayed the scan.
