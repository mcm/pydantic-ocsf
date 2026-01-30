"""The normalized identifier of the file content confidentiality indicator. enumeration."""

from enum import IntEnum


class FileConfidentialityId(IntEnum):
    """The normalized identifier of the file content confidentiality indicator.

    See: https://schema.ocsf.io/1.0.0/data_types/file_confidentiality_id
    """

    UNKNOWN = 0  #
    NOT_CONFIDENTIAL = 1  #
    CONFIDENTIAL = 2  #
    SECRET = 3  #
    TOP_SECRET = 4  #
    OTHER = 99  #
