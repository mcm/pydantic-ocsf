"""The normalized identifier of the data classification category. enumeration."""

from enum import IntEnum


class DataClassificationCategoryId(IntEnum):
    """The normalized identifier of the data classification category.

    See: https://schema.ocsf.io/1.7.0/data_types/data_classification_category_id
    """

    UNKNOWN = 0  # The type is not mapped. See the <code>data_type</code> attribute, which contains a data source specific value.
    PERSONAL = 1  # Any Personally Identifiable Information (PII), Electronic Personal Health Information (ePHI), or similarly personal information. E.g., full name, home address, date of birth, etc.
    GOVERNMENTAL = 2  # Any sensitive government identification number related to a person or other classified material. E.g., Passport numbers, driver license numbers, business identification, taxation identifiers, etc.
    FINANCIAL = 3  # Any financially-related sensitive information or Cardholder Data (CHD). E.g., banking account numbers, credit card numbers, International Banking Account Numbers (IBAN), SWIFT codes, etc.
    BUSINESS = 4  # Any business-specific sensitive data such as intellectual property, trademarks, copyrights, human resource data, Board of Directors meeting minutes, and similar.
    MILITARY_AND_LAW_ENFORCEMENT = 5  # Any mission-specific sensitive data for military, law enforcement, or other government agencies such as specifically classified data, weapon systems information, or other planning data.
    SECURITY = 6  # Any sensitive security-related data such as passwords, passkeys, IP addresses, API keys, credentials and similar secrets. E.g., AWS Access Secret Key, SaaS API Keys, user passwords, database credentials, etc.
    OTHER = 99  # Any other type of data classification or a multi-variate classification made up of several other classification categories.
