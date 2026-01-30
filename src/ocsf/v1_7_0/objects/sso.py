"""SSO object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_7_0.objects.certificate import Certificate


class Sso(OCSFBaseModel):
    """The Single Sign-On (SSO) object provides a structure for normalizing SSO attributes, configuration, and/or settings from Identity Providers.

    See: https://schema.ocsf.io/1.7.0/objects/sso
    """

    # Nested Enums for sibling attribute pairs
    class AuthProtocolId(SiblingEnum):
        """The normalized identifier of the authentication protocol used by the SSO resource.

        OCSF Attribute: auth_protocol_id
        """

        UNKNOWN = 0
        NTLM = 1
        KERBEROS = 2
        DIGEST = 3
        OPENID = 4
        SAML = 5
        OAUTH_20 = 6
        PAP = 7
        CHAP = 8
        EAP = 9
        RADIUS = 10
        BASIC_AUTHENTICATION = 11
        LDAP = 12
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "NTLM",
                2: "Kerberos",
                3: "Digest",
                4: "OpenID",
                5: "SAML",
                6: "OAUTH 2.0",
                7: "PAP",
                8: "CHAP",
                9: "EAP",
                10: "RADIUS",
                11: "Basic Authentication",
                12: "LDAP",
                99: "Other",
            }

    auth_protocol: str | None = Field(
        default=None,
        description="The authorization protocol as defined by the caption of <code>auth_protocol_id</code>. In the case of <code>Other</code>, it is defined by the event source.",
    )
    auth_protocol_id: AuthProtocolId | None = Field(
        default=None,
        description="The normalized identifier of the authentication protocol used by the SSO resource.",
    )
    certificate: Certificate | None = Field(
        default=None,
        description="Digital Signature associated with the SSO resource, e.g., SAML X.509 certificate details. [Recommended]",
    )
    created_time: int | None = Field(default=None, description="When the SSO resource was created.")
    duration_mins: int | None = Field(
        default=None,
        description="The duration (in minutes) for an SSO session, after which re-authentication is required.",
    )
    idle_timeout: int | None = Field(
        default=None,
        description="Duration (in minutes) of allowed inactivity before Single Sign-On (SSO) session expiration.",
    )
    login_endpoint: Any | None = Field(
        default=None, description="URL for initiating an SSO login request."
    )
    logout_endpoint: Any | None = Field(
        default=None,
        description="URL for initiating an SSO logout request, allowing sessions to be terminated across applications.",
    )
    metadata_endpoint: Any | None = Field(
        default=None,
        description="URL where metadata about the SSO configuration is available (e.g., for SAML configurations).",
    )
    modified_time: int | None = Field(
        default=None, description="The most recent time when the SSO resource was updated."
    )
    name: str | None = Field(
        default=None, description="The name of the SSO resource. [Recommended]"
    )
    protocol_name: str | None = Field(
        default=None,
        description="The supported protocol for the SSO resource. E.g., <code>SAML</code> or <code>OIDC</code>.",
    )
    scopes: list[str] | None = Field(
        default=None,
        description="Scopes define the specific permissions or actions that the client is allowed to perform on behalf of the user. Each scope represents a different set of permissions, and the user can selectively grant or deny access to specific scopes during the authorization process.",
    )
    uid: str | None = Field(
        default=None, description="A unique identifier for a SSO resource. [Recommended]"
    )
    vendor_name: str | None = Field(
        default=None,
        description="Name of the vendor or service provider implementing SSO. E.g., <code>Okta</code>, <code>Auth0</code>, <code>Microsoft</code>.",
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
            ("auth_protocol_id", "auth_protocol", cls.AuthProtocolId),
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
