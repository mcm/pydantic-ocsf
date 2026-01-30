"""The run state ID of the job. enumeration."""

from enum import IntEnum


class JobRunStateId(IntEnum):
    """The run state ID of the job.

    See: https://schema.ocsf.io/1.7.0/data_types/job_run_state_id
    """

    UNKNOWN = 0  #
    READY = 1  #
    QUEUED = 2  #
    RUNNING = 3  #
    STOPPED = 4  #
    OTHER = 99  #
