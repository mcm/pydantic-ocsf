"""Domain Contact object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.location import Location


class DomainContact(OCSFBaseModel):
    """The contact information related to a domain registration, e.g., registrant, administrator, abuse, billing, or technical contact.

    See: https://schema.ocsf.io/1.6.0/objects/domain_contact
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The normalized domain contact type ID.

        OCSF Attribute: type_id
        """

        REGISTRANT = 1
        ADMINISTRATIVE = 2
        TECHNICAL = 3
        BILLING = 4
        ABUSE = 5

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "Registrant",
                2: "Administrative",
                3: "Technical",
                4: "Billing",
                5: "Abuse",
            }

    type_id: TypeId = Field(..., description="The normalized domain contact type ID.")
    email_addr: Any | None = Field(
        default=None, description="The user's primary email address. [Recommended]"
    )
    location: Location | None = Field(
        default=None,
        description="Location details for the contract such as the city, state/province, country, etc. [Recommended]",
    )
    name: str | None = Field(
        default=None, description="The individual or organization name for the contact."
    )
    phone_number: str | None = Field(
        default=None, description="The number associated with the phone."
    )
    type_: str | None = Field(
        default=None,
        description="The Domain Contact type, normalized to the caption of the <code>type_id</code> value. In the case of 'Other', it is defined by the source",
    )
    uid: str | None = Field(
        default=None,
        description="The unique identifier of the contact information, typically provided in WHOIS information.",
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
