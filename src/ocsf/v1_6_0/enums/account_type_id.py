"""The normalized account type identifier. enumeration."""

from enum import IntEnum


class AccountTypeId(IntEnum):
    """The normalized account type identifier.

    See: https://schema.ocsf.io/1.6.0/data_types/account_type_id
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
    GCP_PROJECT = 11  #
    OCI_COMPARTMENT = 12  #
    AZURE_SUBSCRIPTION = 13  #
    SALESFORCE_ACCOUNT = 14  #
    GOOGLE_WORKSPACE = 15  #
    SERVICENOW_INSTANCE = 16  #
    M365_TENANT = 17  #
    EMAIL_ACCOUNT = 18  #
    OTHER = 99  # The account type is not mapped.
