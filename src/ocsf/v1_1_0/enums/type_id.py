"""The normalized account type identifier. enumeration."""

from enum import IntEnum


class TypeId(IntEnum):
    """The normalized account type identifier.

    See: https://schema.ocsf.io/1.1.0/data_types/type_id
    """

    UNKNOWN = 0  # The account type is unknown.
    LDAP_ACCOUNT = 1  #
    WINDOWS_ACCOUNT = 2  #
    AWS_IAM_USER = 3  #
    AWS_IAM_ROLE = 4  #
    GCP_ACCOUNT = 5  #
    AZURE_AD_ACCOUNT = 6  #
    MAC_OS_ACCOUNT = 7  #
    APPLE_ACCOUNT = 8  #
    LINUX_ACCOUNT = 9  #
    AWS_ACCOUNT = 10  #
    OTHER = 99  # The account type is not mapped.
