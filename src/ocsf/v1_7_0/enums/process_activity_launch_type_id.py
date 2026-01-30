"""The normalized identifier for the specific type of <code>Launch</code> activity. enumeration."""

from enum import IntEnum


class ProcessActivityLaunchTypeId(IntEnum):
    """The normalized identifier for the specific type of <code>Launch</code> activity.

    See: https://schema.ocsf.io/1.7.0/data_types/process_activity_launch_type_id
    """

    UNKNOWN = 0  # The launch type is unknown or not specified.
    SPAWN = 1  # Denotes that the <code>Launch</code> event represents atomic creation of a new process on Windows. This launch type ID may also be used to represent both steps of Unix process creation in a single <code>Launch</code> event.
    FORK = 2  # Denotes that the <code>Launch</code> event represents the "fork" step of Unix process creation, where a process creates a clone of itself in a parent-child relationship. WSL1 pico processes on Windows also use the 2-step Unix model.
    EXEC = 3  # Denotes that the <code>Launch</code> event represents the "exec" step of Unix process creation, where a process replaces its executable image, command line, and environment. WSL1 pico processes on Windows also use the 2-step Unix model.
    OTHER = 99  # The launch type is not mapped. See the <code>launch_type</code> attribute, which contains a data source specific value.
