"""SCIM object."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum


class Scim(OCSFBaseModel):
    """The System for Cross-domain Identity Management (SCIM) Configuration object provides a structured set of attributes related to SCIM protocols used for identity provisioning and management across cloud-based platforms. It standardizes user and group provisioning details, enabling identity synchronization and lifecycle management with compatible Identity Providers (IdPs) and applications. SCIM is defined in <a target='_blank' href='https://datatracker.ietf.org/doc/html/rfc7643'>RFC-7634</a>

    See: https://schema.ocsf.io/1.7.0/objects/scim
    """

    # Nested Enums for sibling attribute pairs
    class AuthProtocolId(SiblingEnum):
        """The normalized identifier of the authorization protocol used by the SCIM resource.

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

    class StateId(SiblingEnum):
        """The normalized state ID of the SCIM resource to reflect its activation status.

        OCSF Attribute: state_id
        """

        UNKNOWN = 0
        PENDING = 1
        ACTIVE = 2
        FAILED = 3
        DELETED = 4
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Pending",
                2: "Active",
                3: "Failed",
                4: "Deleted",
                99: "Other",
            }

    auth_protocol: str | None = Field(
        default=None,
        description="The authorization protocol as defined by the caption of <code>auth_protocol_id</code>. In the case of <code>Other</code>, it is defined by the event source.",
    )
    auth_protocol_id: AuthProtocolId | None = Field(
        default=None,
        description="The normalized identifier of the authorization protocol used by the SCIM resource.",
    )
    created_time: int | None = Field(
        default=None, description="When the SCIM resource was added to the service provider."
    )
    error_message: str | None = Field(
        default=None, description="Message or code associated with the last encountered error."
    )
    is_group_provisioning_enabled: bool | None = Field(
        default=None,
        description="Indicates whether the SCIM resource is configured to provision groups, automatically or otherwise.",
    )
    is_user_provisioning_enabled: bool | None = Field(
        default=None,
        description="Indicates whether the SCIM resource is configured to provision users, automatically or otherwise.",
    )
    last_run_time: int | None = Field(
        default=None, description="Timestamp of the most recent successful synchronization."
    )
    modified_time: int | None = Field(
        default=None,
        description="The most recent time when the SCIM resource was updated at the service provider.",
    )
    name: str | None = Field(
        default=None, description="The name of the SCIM resource. [Recommended]"
    )
    protocol_name: str | None = Field(
        default=None,
        description="The supported protocol for the SCIM resource. E.g., <code>SAML</code>, <code>OIDC</code>, or <code>OAuth2</code>.",
    )
    rate_limit: int | None = Field(
        default=None,
        description="Maximum number of requests allowed by the SCIM resource within a specified time frame to avoid throttling.",
    )
    scim_group_schema: dict[str, Any] | None = Field(
        default=None,
        description="SCIM provides a schema for representing groups, identified using the following schema URI: <code>urn:ietf:params:scim:schemas:core:2.0:Group</code> as defined in <a target='_blank' href='https://datatracker.ietf.org/doc/html/rfc7643'>RFC-7634</a>. This attribute will capture key-value pairs for the scheme implemented in a SCIM resource. [Recommended]",
    )
    scim_user_schema: dict[str, Any] | None = Field(
        default=None,
        description="SCIM provides a resource type for user resources. The core schema for user is identified using the following schema URI: <code>urn:ietf:params:scim:schemas:core:2.0:User</code> as defined in <a target='_blank' href='https://datatracker.ietf.org/doc/html/rfc7643'>RFC-7634</a>. his attribute will capture key-value pairs for the scheme implemented in a SCIM resource. This object is inclusive of both the basic and Enterprise User Schema Extension. [Recommended]",
    )
    state: str | None = Field(
        default=None,
        description="The provisioning state of the SCIM resource, normalized to the caption of the <code>state_id</code> value. In the case of <code>Other</code>, it is defined by the event source.",
    )
    state_id: StateId | None = Field(
        default=None,
        description="The normalized state ID of the SCIM resource to reflect its activation status.",
    )
    uid: str | None = Field(
        default=None,
        description="A unique identifier for a SCIM resource as defined by the service provider. [Recommended]",
    )
    uid_alt: str | None = Field(
        default=None,
        description="A String that is an identifier for the resource as defined by the provisioning client. The <code>externalId</code> may simplify identification of a resource between the provisioning client and the service provider by allowing the client to use a filter to locate the resource with an identifier from the provisioning domain, obviating the need to store a local mapping between the provisioning domain's identifier of the resource and the identifier used by the service provider.",
    )
    url_string: Any | None = Field(
        default=None, description="The primary URL for SCIM API requests."
    )
    vendor_name: str | None = Field(
        default=None,
        description="Name of the vendor or service provider implementing SCIM. E.g., <code>Okta</code>, <code>Auth0</code>, <code>Microsoft</code>.",
    )
    version: str | None = Field(
        default=None,
        description="SCIM protocol version supported e.g., <code>SCIM 2.0</code>. [Recommended]",
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
            ("state_id", "state", cls.StateId),
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
