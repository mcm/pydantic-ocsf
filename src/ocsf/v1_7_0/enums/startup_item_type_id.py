"""The startup item type identifier. enumeration."""

from enum import IntEnum


class StartupItemTypeId(IntEnum):
    """The startup item type identifier.

    See: https://schema.ocsf.io/1.7.0/data_types/startup_item_type_id
    """

    UNKNOWN = 0  # The type is unknown.
    KERNEL_MODE_DRIVER = 1  # Kernel mode driver.
    USER_MODE_DRIVER = 2  # User mode driver.
    SERVICE = 3  # A background process typically managed by the operating system, e.g., a service process on Windows or a systemd-managed daemon on Linux.
    USER_MODE_APPLICATION = 4  # An application that runs in the user space.
    AUTOLOAD = 5  # The macOS Autoload Application.
    SYSTEM_EXTENSION = (
        6  # System extensions on macOS enables 3rd parties to extend the capabilities of macOS.
    )
    KERNEL_EXTENSION = 7  # Kernel extensions on macOS includes Apple provided pre-installs and 3rd party installs which enables support for specific hardware or software features not natively supported by macOS.
    SCHEDULED_JOB__TASK = 8  # A job or task that runs on a configured schedule.
    OTHER = 99  # The startup item type is not mapped. See the <code>type</code> attribute, which contains data source specific values.
