"""The TLS extension type identifier. See <a target='_blank' href='https://datatracker.ietf.org/doc/html/rfc8446#page-35'>The Transport Layer Security (TLS) extension page</a>. enumeration."""

from enum import IntEnum


class TlsExtensionTypeId(IntEnum):
    """The TLS extension type identifier. See <a target='_blank' href='https://datatracker.ietf.org/doc/html/rfc8446#page-35'>The Transport Layer Security (TLS) extension page</a>.

    See: https://schema.ocsf.io/1.6.0/data_types/tls_extension_type_id
    """

    SERVER_NAME = 0  # The Server Name Indication extension.
    MAXIMUM_FRAGMENT_LENGTH = 1  # The Maximum Fragment Length Negotiation extension.
    STATUS_REQUEST = 5  # The Certificate Status Request extension.
    SUPPORTED_GROUPS = 10  # The Supported Groups extension.
    SIGNATURE_ALGORITHMS = 13  # The Signature Algorithms extension.
    USE_SRTP = 14  # The Use SRTP data protection extension.
    HEARTBEAT = 15  # The Heartbeat extension.
    APPLICATION_LAYER_PROTOCOL_NEGOTIATION = (
        16  # The Application-Layer Protocol Negotiation extension.
    )
    SIGNED_CERTIFICATE_TIMESTAMP = 18  # The Signed Certificate Timestamp extension.
    CLIENT_CERTIFICATE_TYPE = 19  # The Client Certificate Type extension.
    SERVER_CERTIFICATE_TYPE = 20  # The Server Certificate Type extension.
    PADDING = 21  # The Padding extension.
    PRE_SHARED_KEY = 41  # The Pre Shared Key extension.
    EARLY_DATA = 42  # The Early Data extension.
    SUPPORTED_VERSIONS = 43  # The Supported Versions extension.
    COOKIE = 44  # The Cookie extension.
    PSK_KEY_EXCHANGE_MODES = 45  # The Pre-Shared Key Exchange Modes extension.
    CERTIFICATE_AUTHORITIES = 47  # The Certificate Authorities extension.
    OID_FILTERS = 48  # The OID Filters extension.
    POST_HANDSHAKE_AUTH = 49  # The Post-Handshake Client Authentication extension.
    SIGNATURE_ALGORITHMS_CERT = 50  # The Signature Algorithms extension.
    KEY_SHARE = 51  # The Key Share extension.
