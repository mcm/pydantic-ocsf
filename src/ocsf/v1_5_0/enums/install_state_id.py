"""The normalized install state ID of the Advisory. enumeration."""

from enum import IntEnum


class InstallStateId(IntEnum):
    """The normalized install state ID of the Advisory.

    See: https://schema.ocsf.io/1.5.0/data_types/install_state_id
    """

    UNKNOWN = 0  # The normalized install state is unknown.
    INSTALLED = 1  # The item is installed.
    NOT_INSTALLED = 2  # The item is not installed.
    INSTALLED_PENDING_REBOOT = 3  # The item is installed pending reboot operation.
    OTHER = 99  # The install state is not mapped. See the <code>install_state</code> attribute, which contains a data source specific value.
