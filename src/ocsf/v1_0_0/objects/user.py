"""User object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_0_0.objects.account import Account
    from ocsf.v1_0_0.objects.group import Group
    from ocsf.v1_0_0.objects.organization import Organization


class User(OCSFBaseModel):
    """The User object describes the characteristics of a user/person or a security principal. Defined by D3FEND <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:UserAccount/'>d3f:UserAccount</a>.

    See: https://schema.ocsf.io/1.0.0/objects/user
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The account type identifier.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        USER = 1
        ADMIN = 2
        SYSTEM = 3
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "User",
                2: "Admin",
                3: "System",
                99: "Other",
            }

    type_id: TypeId = Field(..., description="The account type identifier.")
    account: Account | None = Field(
        default=None, description="The user's account or the account associated with the user."
    )
    credential_uid: str | None = Field(
        default=None,
        description="The unique identifier of the user's credential. For example, AWS Access Key ID.",
    )
    domain: str | None = Field(
        default=None,
        description="The domain where the user is defined. For example: the LDAP or Active Directory domain.",
    )
    email_addr: Any | None = Field(default=None, description="The user's email address.")
    full_name: str | None = Field(
        default=None,
        description="The full name of the person, as per the LDAP Common Name attribute (cn).",
    )
    groups: list[Group] | None = Field(
        default=None, description="The administrative groups to which the user belongs."
    )
    name: Any | None = Field(
        default=None, description="The username. For example, <code>janedoe1</code>."
    )
    org: Organization | None = Field(
        default=None, description="Organization and org unit related to the user."
    )
    type_: str | None = Field(
        default=None, description="The type of the user. For example, System, AWS IAM User, etc."
    )
    uid: str | None = Field(
        default=None,
        description="The unique user identifier. For example, the Windows user SID, ActiveDirectory DN or AWS user ARN.",
    )
    uid_alt: str | None = Field(
        default=None,
        description="The alternate user identifier. For example, the Active Directory user GUID or AWS user Principal ID.",
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
