"""The normalized identifier of the databucket type. enumeration."""

from enum import IntEnum


class DatabucketTypeId(IntEnum):
    """The normalized identifier of the databucket type.

    See: https://schema.ocsf.io/1.6.0/data_types/databucket_type_id
    """

    UNKNOWN = 0  #
    S3 = 1  #
    AZURE_BLOB = 2  #
    GCP_BUCKET = 3  #
    OTHER = 99  #
