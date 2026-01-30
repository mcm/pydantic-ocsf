"""Identity Provider object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.auth_factor import AuthFactor
    from ocsf.v1_6_0.objects.fingerprint import Fingerprint
    from ocsf.v1_6_0.objects.scim import Scim
    from ocsf.v1_6_0.objects.sso import Sso


class Idp(OCSFBaseModel):
    """The Identity Provider object contains detailed information about a provider responsible for creating, maintaining, and managing identity information while offering authentication services to applications. An Identity Provider (IdP) serves as a trusted authority that verifies the identity of users and issues authentication tokens or assertions to enable secure access to applications or services.

    See: https://schema.ocsf.io/1.6.0/objects/idp
    """

    # Nested Enums for sibling attribute pairs
    class StateId(SiblingEnum):
        """The normalized state ID of the Identity Provider to reflect its configuration or activation status.

        OCSF Attribute: state_id
        """

        UNKNOWN = 0
        ACTIVE = 1
        SUSPENDED = 2
        DEPRECATED = 3
        DELETED = 4
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Active",
                2: "Suspended",
                3: "Deprecated",
                4: "Deleted",
                99: "Other",
            }

    auth_factors: list[AuthFactor] | None = Field(
        default=None,
        description="The Authentication Factors object describes the different types of Multi-Factor Authentication (MFA) methods and/or devices supported by the Identity Provider.",
    )
    domain: str | None = Field(
        default=None, description="The primary domain associated with the Identity Provider."
    )
    fingerprint: Fingerprint | None = Field(
        default=None,
        description="The fingerprint of the X.509 certificate used by the Identity Provider.",
    )
    has_mfa: bool | None = Field(
        default=None,
        description="The Identity Provider enforces Multi Factor Authentication (MFA).",
    )
    issuer: str | None = Field(
        default=None,
        description="The unique identifier (often a URL) used by the Identity Provider as its issuer.",
    )
    name: str | None = Field(
        default=None, description="The name of the Identity Provider. [Recommended]"
    )
    protocol_name: str | None = Field(
        default=None,
        description="The supported protocol of the Identity Provider. E.g., <code>SAML</code>, <code>OIDC</code>, or <code>OAuth2</code>.",
    )
    scim: Scim | None = Field(
        default=None,
        description="The System for Cross-domain Identity Management (SCIM) resource object provides a structured set of attributes related to SCIM protocols used for identity provisioning and management across cloud-based platforms. It standardizes user and group provisioning details, enabling identity synchronization and lifecycle management with compatible Identity Providers (IdPs) and applications. SCIM is defined in <a target='_blank' href='https://datatracker.ietf.org/doc/html/rfc7643'>RFC-7634</a>",
    )
    sso: Sso | None = Field(
        default=None,
        description="The Single Sign-On (SSO) object provides a structure for normalizing SSO attributes, configuration, and/or settings from Identity Providers.",
    )
    state: str | None = Field(
        default=None,
        description="The configuration state of the Identity Provider, normalized to the caption of the <code>state_id</code> value. In the case of <code>Other</code>, it is defined by the event source.",
    )
    state_id: StateId | None = Field(
        default=None,
        description="The normalized state ID of the Identity Provider to reflect its configuration or activation status.",
    )
    tenant_uid: str | None = Field(
        default=None, description="The tenant ID associated with the Identity Provider."
    )
    uid: str | None = Field(
        default=None, description="The unique identifier of the Identity Provider. [Recommended]"
    )
    url_string: Any | None = Field(
        default=None,
        description="The URL for accessing the configuration or metadata of the Identity Provider.",
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
            ("state_id", "state", cls.StateId),
        ]

        for id_field, label_field, enum_cls in siblings:
            id_val = data.get(id_field)
            label_val = data.get(label_field)

            has_id = id_val is not None
            has_label = label_val is not None

            if has_id and has_label:
                # Both present: validate consistency
                assert id_val is not None  # Type narrowing for mypy
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
                assert id_val is not None  # Type narrowing for mypy
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
