"""Identifies the type of a disk drive, i.e. fixed, removable, etc. enumeration."""

from enum import IntEnum


class DriveTypeId(IntEnum):
    """Identifies the type of a disk drive, i.e. fixed, removable, etc.

    See: https://schema.ocsf.io/1.5.0/data_types/drive_type_id
    """

    UNKNOWN = 0  # The drive type is unknown.
    REMOVABLE = 1  # The drive has removable media; for example, a floppy drive, thumb drive, or flash card reader.
    FIXED = 2  # The drive has fixed media; for example, a hard disk drive or flash drive.
    REMOTE = 3  # The drive is a remote (network) drive.
    CD_ROM = 4  # The drive is a CD-ROM drive.
    RAM_DISK = 5  # The drive is a RAM disk.
    OTHER = 99  # The drive type is not mapped. See the <code>drive_type</code> attribute, which contains a data source specific value.
