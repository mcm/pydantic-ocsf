"""The normalized script type ID. enumeration."""

from enum import IntEnum


class ScriptTypeId(IntEnum):
    """The normalized script type ID.

    See: https://schema.ocsf.io/1.7.0/data_types/script_type_id
    """

    UNKNOWN = 0  # The script type is unknown.
    WINDOWS_COMMAND_PROMPT = 1  #
    POWERSHELL = 2  #
    PYTHON = 3  #
    JAVASCRIPT = 4  #
    VBSCRIPT = 5  #
    UNIX_SHELL = 6  #
    VBA = 7  #
    OTHER = 99  # The script type is not mapped. See the <code>type</code> attribute which contains an event source specific value.
