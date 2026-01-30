"""The normalized identifier of the file content confidentiality indicator. enumeration."""

from enum import IntEnum


class DataClassificationConfidentialityId(IntEnum):
    """The normalized identifier of the file content confidentiality indicator.

    See: https://schema.ocsf.io/1.6.0/data_types/data_classification_confidentiality_id
    """

    UNKNOWN = 0  # The confidentiality is unknown.
    NOT_CONFIDENTIAL = 1  #
    CONFIDENTIAL = 2  #
    SECRET = 3  #
    TOP_SECRET = 4  #
    PRIVATE = 5  #
    RESTRICTED = 6  #
    OTHER = 99  # The confidentiality is not mapped. See the <code>confidentiality</code> attribute, which contains a data source specific value.
