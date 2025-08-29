from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.object import Object


class TypeId(Enum):
    SERVER_NAME = 0
    MAXIMUM_FRAGMENT_LENGTH = 1
    STATUS_REQUEST = 5
    SUPPORTED_GROUPS = 10
    SIGNATURE_ALGORITHMS = 13
    USE_SRTP = 14
    HEARTBEAT = 15
    APPLICATION_LAYER_PROTOCOL_NEGOTIATION = 16
    SIGNED_CERTIFICATE_TIMESTAMP = 18
    CLIENT_CERTIFICATE_TYPE = 19
    SERVER_CERTIFICATE_TYPE = 20
    PADDING = 21
    PRE_SHARED_KEY = 41
    EARLY_DATA = 42
    SUPPORTED_VERSIONS = 43
    COOKIE = 44
    PSK_KEY_EXCHANGE_MODES = 45
    CERTIFICATE_AUTHORITIES = 47
    OID_FILTERS = 48
    POST_HANDSHAKE_AUTH = 49
    SIGNATURE_ALGORITHMS_CERT = 50
    KEY_SHARE = 51
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return TypeId[obj]
        else:
            return TypeId(obj)

    @enum_property
    def name(self):
        name_map = {
            "SERVER_NAME": "server_name",
            "MAXIMUM_FRAGMENT_LENGTH": "maximum_fragment_length",
            "STATUS_REQUEST": "status_request",
            "SUPPORTED_GROUPS": "supported_groups",
            "SIGNATURE_ALGORITHMS": "signature_algorithms",
            "USE_SRTP": "use_srtp",
            "HEARTBEAT": "heartbeat",
            "APPLICATION_LAYER_PROTOCOL_NEGOTIATION": "application_layer_protocol_negotiation",
            "SIGNED_CERTIFICATE_TIMESTAMP": "signed_certificate_timestamp",
            "CLIENT_CERTIFICATE_TYPE": "client_certificate_type",
            "SERVER_CERTIFICATE_TYPE": "server_certificate_type",
            "PADDING": "padding",
            "PRE_SHARED_KEY": "pre_shared_key",
            "EARLY_DATA": "early_data",
            "SUPPORTED_VERSIONS": "supported_versions",
            "COOKIE": "cookie",
            "PSK_KEY_EXCHANGE_MODES": "psk_key_exchange_modes",
            "CERTIFICATE_AUTHORITIES": "certificate_authorities",
            "OID_FILTERS": "oid_filters",
            "POST_HANDSHAKE_AUTH": "post_handshake_auth",
            "SIGNATURE_ALGORITHMS_CERT": "signature_algorithms_cert",
            "KEY_SHARE": "key_share",
            "OTHER": "Other",
        }
        return name_map[super().name]


class TLSExtension(Object):
    schema_name: ClassVar[str] = "tls_extension"

    # Required
    type_id: TypeId

    # Recommended
    data: dict[str, Any] | None = None

    # Optional
    type_: str | None = None
