"""The identifier of the JA4+ fingerprint type. enumeration."""

from enum import IntEnum


class Ja4FingerprintTypeId(IntEnum):
    """The identifier of the JA4+ fingerprint type.

    See: https://schema.ocsf.io/1.7.0/data_types/ja4_fingerprint_type_id
    """

    UNKNOWN = 0  #
    JA4 = 1  # TLS Client Fingerprint.
    JA4SERVER = 2  # TLS Server Response/Session Fingerprint.
    JA4HTTP = 3  # HTTP Client Fingerprint.
    JA4LATENCY = 4  # Latency Measurement/Light Distance Fingerprint.
    JA4X509 = 5  # X509 TLS Certificate Fingerprint.
    JA4SSH = 6  # SSH Traffic Fingerprint.
    JA4TCP = 7  # Passive TCP Client Fingerprint.
    JA4TCPSERVER = 8  # Passive TCP Server Fingerprint.
    JA4TCPSCAN = 9  # Active TCP Server Fingerprint.
    OTHER = 99  #
