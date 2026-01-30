"""The type identifier of the operating system. enumeration."""

from enum import IntEnum


class OsTypeId(IntEnum):
    """The type identifier of the operating system.

    See: https://schema.ocsf.io/1.0.0/data_types/os_type_id
    """

    WINDOWS = 100  #
    WINDOWS_MOBILE = 101  #
    LINUX = 200  #
    ANDROID = 201  #
    MACOS = 300  #
    IOS = 301  #
    IPADOS = 302  #
    SOLARIS = 400  #
    AIX = 401  #
    HP_UX = 402  #
