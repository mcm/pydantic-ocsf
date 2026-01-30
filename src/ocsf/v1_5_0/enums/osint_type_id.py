"""The OSINT indicator type ID. enumeration."""

from enum import IntEnum


class OsintTypeId(IntEnum):
    """The OSINT indicator type ID.

    See: https://schema.ocsf.io/1.5.0/data_types/osint_type_id
    """

    UNKNOWN = 0  # The indicator type is ambiguous or there is not a related indicator for the OSINT object.
    IP_ADDRESS = 1  # An IPv4 or IPv6 address.
    DOMAIN = 2  # A full-qualified domain name (FQDN), subdomain, or partial domain.
    HOSTNAME = 3  # A hostname or computer name.
    HASH = 4  # Any type of hash e.g., MD5, SHA1, SHA2, BLAKE, BLAKE2, SSDEEP, VHASH, etc. generated from a file, malware sample, request header, or otherwise used to identify a pertinent artifact.
    URL = 5  # A Uniform Resource Locator (URL) or Uniform Resource Indicator (URI).
    USER_AGENT = 6  # A User Agent typically seen in HTTP request headers.
    DIGITAL_CERTIFICATE = (
        7  # The serial number, fingerprint, or full content of an X.509 digital certificate.
    )
    EMAIL = 8  # The contents of an email or any related information to an email object.
    EMAIL_ADDRESS = 9  # An email address.
    VULNERABILITY = 10  # A CVE ID, CWE ID, or other identifier for a weakness, exploit, bug, or misconfiguration.
    FILE = 11  # A file or metadata about a file.
    REGISTRY_KEY = 12  # A Windows Registry Key.
    REGISTRY_VALUE = 13  # A Windows Registry Value.
    COMMAND_LINE = (
        14  # A partial or full Command Line used to invoke scripts or other remote commands.
    )
    OTHER = 99  # The indicator type is not directly listed.
