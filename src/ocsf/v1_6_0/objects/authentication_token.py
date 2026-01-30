"""Authentication Token object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.encryption_details import EncryptionDetails


class AuthenticationToken(OCSFBaseModel):
    """The Authentication Token object represents standardized authentication tokens, tickets, or assertions that conform to established authentication protocols such as Kerberos, OIDC, and SAML. These tokens are issued by authentication servers and identity providers and carry protocol-specific metadata, lifecycle information, and security attributes defined by their respective specifications.

    See: https://schema.ocsf.io/1.6.0/objects/authentication_token
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The normalized authentication token type identifier.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        TICKET_GRANTING_TICKET = 1
        SERVICE_TICKET = 2
        IDENTITY_TOKEN = 3
        REFRESH_TOKEN = 4
        SAML_ASSERTION = 5
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Ticket Granting Ticket",
                2: "Service Ticket",
                3: "Identity Token",
                4: "Refresh Token",
                5: "SAML Assertion",
                99: "Other",
            }

    created_time: int | None = Field(
        default=None,
        description="The time that the authentication token was created. [Recommended]",
    )
    encryption_details: EncryptionDetails | None = Field(
        default=None,
        description="The encryption details of the authentication token. [Recommended]",
    )
    expiration_time: int | None = Field(
        default=None, description="The expiration time of the authentication token."
    )
    is_renewable: bool | None = Field(
        default=None, description="Indicates whether the authentication token is renewable."
    )
    kerberos_flags: str | None = Field(
        default=None,
        description="A bitmask, either in hexadecimal or decimal form, which encodes various attributes or permissions associated with a Kerberos ticket. These flags delineate specific characteristics of the ticket, such as its renewability or forwardability. [Recommended]",
    )
    type_: str | None = Field(
        default=None, description="The type of the authentication token. [Recommended]"
    )
    type_id: TypeId | None = Field(
        default=None,
        description="The normalized authentication token type identifier. [Recommended]",
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
