"""Managed Entity object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.device import Device
    from ocsf.v1_6_0.objects.email import Email
    from ocsf.v1_6_0.objects.group import Group
    from ocsf.v1_6_0.objects.location import Location
    from ocsf.v1_6_0.objects.organization import Organization
    from ocsf.v1_6_0.objects.policy import Policy
    from ocsf.v1_6_0.objects.user import User


class ManagedEntity(OCSFBaseModel):
    """The Managed Entity object describes the type and version of an entity, such as a user, device, or policy.  For types in the <code>type_id</code> enum list, an associated attribute should be populated.  If the type of entity is not in the <code>type_id</code> list, information can be put into the <code>data</code> attribute, <code>type_id</code> should be 'Other' and the <code>type</code> attribute should label the entity type.

    See: https://schema.ocsf.io/1.6.0/objects/managed_entity
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The type of the Managed Entity. It is recommended to also populate the <code>type</code> attribute with the associated label, or the source specific name if <code>Other</code>.

        OCSF Attribute: type_id
        """

        DEVICE = 1
        USER = 2
        GROUP = 3
        ORGANIZATION = 4
        POLICY = 5
        EMAIL = 6
        NETWORK_ZONE = 7

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "Device",
                2: "User",
                3: "Group",
                4: "Organization",
                5: "Policy",
                6: "Email",
                7: "Network Zone",
            }

    data: dict[str, Any] | None = Field(
        default=None, description="The managed entity content as a JSON object."
    )
    device: Device | None = Field(
        default=None, description="An addressable device, computer system or host. [Recommended]"
    )
    email: Email | None = Field(default=None, description="The email object. [Recommended]")
    group: Group | None = Field(
        default=None,
        description="The group object associated with an entity such as user, policy, or rule. [Recommended]",
    )
    location: Location | None = Field(
        default=None,
        description="The detailed geographical location usually associated with an IP address.",
    )
    name: str | None = Field(
        default=None,
        description="The name of the managed entity. It should match the name of the specific entity object's name if populated, or the name of the managed entity if the <code>type_id</code> is 'Other'.",
    )
    org: Organization | None = Field(
        default=None,
        description="Organization and org unit relevant to the event or object. [Recommended]",
    )
    policy: Policy | None = Field(
        default=None, description="Describes details of a managed policy. [Recommended]"
    )
    type_: str | None = Field(
        default=None,
        description="The managed entity type. For example: <code>Policy</code>, <code>User</code>, <code>Organization</code>, <code>Device</code>. [Recommended]",
    )
    type_id: TypeId | None = Field(
        default=None,
        description="The type of the Managed Entity. It is recommended to also populate the <code>type</code> attribute with the associated label, or the source specific name if <code>Other</code>. [Recommended]",
    )
    uid: str | None = Field(
        default=None,
        description="The identifier of the managed entity. It should match the <code>uid</code> of the specific entity's object UID if populated, or the source specific ID if the <code>type_id</code> is 'Other'.",
    )
    user: User | None = Field(
        default=None, description="The user that pertains to the event or object. [Recommended]"
    )
    version: str | None = Field(
        default=None,
        description="The version of the managed entity. For example: <code>1.2.3</code>. [Recommended]",
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
