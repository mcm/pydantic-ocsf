"""The run state ID of the startup item. enumeration."""

from enum import IntEnum


class StartupItemRunStateId(IntEnum):
    """The run state ID of the startup item.

    See: https://schema.ocsf.io/1.5.0/data_types/startup_item_run_state_id
    """

    STOPPED = 1  # The service is not running.
    START_PENDING = 2  # The service is starting.
    STOP_PENDING = 3  # The service is stopping.
    RUNNING = 4  # The service is running.
    CONTINUE_PENDING = 5  # The service is pending continue.
    PAUSE_PENDING = 6  # The service is pending pause.
    PAUSED = 7  # The service is paused.
    RESTART_PENDING = 8  # The service is pending restart.
