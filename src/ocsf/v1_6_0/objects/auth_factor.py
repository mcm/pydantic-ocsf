"""Authentication Factor object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.device import Device


class AuthFactor(OCSFBaseModel):
    """An Authentication Factor object describes a category of methods used for identity verification in an authentication attempt.

    See: https://schema.ocsf.io/1.6.0/objects/auth_factor
    """

    # Nested Enums for sibling attribute pairs
    class FactorTypeId(SiblingEnum):
        """The normalized identifier for the authentication factor.

        OCSF Attribute: factor_type_id
        """

        UNKNOWN = 0
        SMS = 1
        SECURITY_QUESTION = 2
        PHONE_CALL = 3
        BIOMETRIC = 4
        PUSH_NOTIFICATION = 5
        HARDWARE_TOKEN = 6
        OTP = 7
        EMAIL = 8
        U2F = 9
        WEBAUTHN = 10
        PASSWORD = 11
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "SMS",
                2: "Security Question",
                3: "Phone Call",
                4: "Biometric",
                5: "Push Notification",
                6: "Hardware Token",
                7: "OTP",
                8: "Email",
                9: "U2F",
                10: "WebAuthn",
                11: "Password",
                99: "Other",
            }

    factor_type_id: FactorTypeId = Field(
        ..., description="The normalized identifier for the authentication factor."
    )
    device: Device | None = Field(
        default=None, description="Device used to complete an authentication request. [Recommended]"
    )
    email_addr: Any | None = Field(
        default=None, description="The email address used in an email-based authentication factor."
    )
    factor_type: str | None = Field(
        default=None,
        description="The type of authentication factor used in an authentication attempt. [Recommended]",
    )
    is_hotp: bool | None = Field(
        default=None,
        description="Whether the authentication factor is an HMAC-based One-time Password (HOTP). [Recommended]",
    )
    is_totp: bool | None = Field(
        default=None,
        description="Whether the authentication factor is a Time-based One-time Password (TOTP). [Recommended]",
    )
    phone_number: str | None = Field(
        default=None,
        description="The phone number used for a telephony-based authentication request.",
    )
    provider: str | None = Field(
        default=None, description="The name of provider for an authentication factor. [Recommended]"
    )
    security_questions: list[str] | None = Field(
        default=None,
        description="The question(s) provided to user for a question-based authentication factor.",
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
            ("factor_type_id", "factor_type", cls.FactorTypeId),
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
