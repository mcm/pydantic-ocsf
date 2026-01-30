"""TLS Extension object."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum


class TlsExtension(OCSFBaseModel):
    """The TLS Extension object describes additional attributes that extend the base Transport Layer Security (TLS) object.

    See: https://schema.ocsf.io/1.2.0/objects/tls_extension
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The TLS extension type identifier. See <a target='_blank' href='https://datatracker.ietf.org/doc/html/rfc8446#page-35'>The Transport Layer Security (TLS) extension page</a>.

        OCSF Attribute: type_id
        """

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

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "server_name",
                1: "maximum_fragment_length",
                5: "status_request",
                10: "supported_groups",
                13: "signature_algorithms",
                14: "use_srtp",
                15: "heartbeat",
                16: "application_layer_protocol_negotiation",
                18: "signed_certificate_timestamp",
                19: "client_certificate_type",
                20: "server_certificate_type",
                21: "padding",
                41: "pre_shared_key",
                42: "early_data",
                43: "supported_versions",
                44: "cookie",
                45: "psk_key_exchange_modes",
                47: "certificate_authorities",
                48: "oid_filters",
                49: "post_handshake_auth",
                50: "signature_algorithms_cert",
                51: "key_share",
            }

    type_id: TypeId = Field(
        ...,
        description="The TLS extension type identifier. See <a target='_blank' href='https://datatracker.ietf.org/doc/html/rfc8446#page-35'>The Transport Layer Security (TLS) extension page</a>.",
    )
    data: dict[str, Any] | None = Field(
        default=None,
        description="The data contains information specific to the particular extension type. [Recommended]",
    )
    type_: str | None = Field(
        default=None, description="The TLS extension type. For example: <code>Server Name</code>."
    )

    @model_validator(mode="before")
    @classmethod
    def _reconcile_siblings(cls, data: Any) -> Any:
        """Reconcile sibling attribute pairs during parsing.

        For each sibling pair (e.g., activity_id/activity_name):
        - If both present: validate they match, use canonical label casing
        - If only ID: extrapolate label from enum
        - If only label: extrapolate ID from enum (unknown → OTHER=99)
        - If neither: leave for field validation to handle required/optional
        """
        if not isinstance(data, dict):
            return data

        # Sibling pairs for this object class
        siblings: list[tuple[str, str, type[SiblingEnum]]] = [
            ("type_id", "type", cls.TypeId),
        ]

        for id_field, label_field, enum_cls in siblings:
            id_val = data.get(id_field)
            label_val = data.get(label_field)

            has_id = id_val is not None
            has_label = label_val is not None

            if has_id and has_label:
                # Both present: validate consistency
                try:
                    enum_member = enum_cls(id_val)
                except (ValueError, KeyError) as e:
                    raise ValueError(f"Invalid {id_field} value: {id_val}") from e

                expected_label = enum_member.label

                # OTHER (99) allows any custom label
                if enum_member.value != 99:
                    if expected_label.lower() != str(label_val).lower():
                        raise ValueError(
                            f"{id_field}={id_val} ({expected_label}) "
                            f"does not match {label_field}={label_val!r}"
                        )
                    # Use canonical label casing
                    data[label_field] = expected_label
                # For OTHER, preserve the custom label as-is

            elif has_id:
                # Only ID provided: extrapolate label
                try:
                    enum_member = enum_cls(id_val)
                    data[label_field] = enum_member.label
                except (ValueError, KeyError) as e:
                    raise ValueError(f"Invalid {id_field} value: {id_val}") from e

            elif has_label:
                # Only label provided: extrapolate ID
                try:
                    enum_member = enum_cls(str(label_val))
                    data[id_field] = enum_member.value
                    data[label_field] = enum_member.label  # Canonical casing
                except (ValueError, KeyError):
                    # Unknown label during JSON parsing → map to OTHER (99) if available
                    # This is lenient for untrusted data, unlike direct enum construction
                    if hasattr(enum_cls, "OTHER"):
                        data[id_field] = 99
                        data[label_field] = "Other"  # Use canonical OTHER label
                    else:
                        raise ValueError(
                            f"Unknown {label_field} value: {label_val!r} "
                            f"and {enum_cls.__name__} has no OTHER member"
                        ) from None

        return data
