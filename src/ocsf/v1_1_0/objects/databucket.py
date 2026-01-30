"""Databucket object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_1_0.objects.file import File
    from ocsf.v1_1_0.objects.group import Group


class Databucket(OCSFBaseModel):
    """The databucket object is a basic container that holds data, typically organized through the use of data partitions.

    See: https://schema.ocsf.io/1.1.0/objects/databucket
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The normalized identifier of the databucket type.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        S3 = 1
        AZURE_BLOB = 2
        GCP_BUCKET = 3
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "S3",
                2: "Azure Blob",
                3: "GCP Bucket",
                99: "Other",
            }

    type_id: TypeId = Field(..., description="The normalized identifier of the databucket type.")
    created_time: int | None = Field(
        default=None, description="The time when the databucket was known to have been created."
    )
    desc: str | None = Field(default=None, description="The description of the databucket.")
    file: File | None = Field(default=None, description="A file within a databucket.")
    groups: list[Group] | None = Field(
        default=None, description="The group names to which the databucket belongs."
    )
    modified_time: int | None = Field(
        default=None,
        description="The most recent time when any changes, updates, or modifications were made within the databucket.",
    )
    name: str | None = Field(default=None, description="The databucket name.")
    size: int | None = Field(default=None, description="The size of the databucket in bytes.")
    type_: str | None = Field(default=None, description="The databucket type. [Recommended]")
    uid: str | None = Field(default=None, description="The unique identifier of the databucket.")

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
