"""The start type ID of the startup item. enumeration."""

from enum import IntEnum


class StartTypeId(IntEnum):
    """The start type ID of the startup item.

    See: https://schema.ocsf.io/1.7.0/data_types/start_type_id
    """

    UNKNOWN = 0  # The start type is unknown.
    AUTO = 1  # Service started automatically during system startup.
    BOOT = 2  # Device driver started by the system loader.
    ON_DEMAND = 3  # Started on demand. For example, by the Windows Service Control Manager when a process calls the <i>StartService</i> function.
    DISABLED = 4  # The service is disabled, and cannot be started.
    ALL_LOGINS = 5  # Started on all user logins.
    SPECIFIC_USER_LOGIN = 6  # Started on specific user logins.
    SCHEDULED = 7  # Stared according to a schedule.
    SYSTEM_CHANGED = 8  # Started when a system item, such as a file or registry key, changes.
    OTHER = 99  # The start type is not mapped. See the <code>start_type</code> attribute, which contains a data source specific value.
