"""Software Component object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_5_0.objects.fingerprint import Fingerprint


class SoftwareComponent(OCSFBaseModel):
    """The Software Component object describes characteristics of a software component within a software package.

    See: https://schema.ocsf.io/1.5.0/objects/software_component
    """

    # Nested Enums for sibling attribute pairs
    class RelationshipId(SiblingEnum):
        """The normalized identifier of the relationship between two software components.

        OCSF Attribute: relationship_id
        """

        UNKNOWN = 0
        DEPENDS_ON = 1
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Depends On",
                99: "Other",
            }

    class TypeId(SiblingEnum):
        """The type of software component.

        OCSF Attribute: type_id
        """

        FRAMEWORK = 1
        LIBRARY = 2
        OPERATING_SYSTEM = 3

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "Framework",
                2: "Library",
                3: "Operating System",
            }

    name: str = Field(..., description="The software component name.")
    version: str = Field(..., description="The software component version.")
    author: str | None = Field(
        default=None,
        description="The author(s) who published the software component. [Recommended]",
    )
    hash: Fingerprint | None = Field(
        default=None,
        description="Cryptographic hash to identify the binary instance of a software component.",
    )
    license: str | None = Field(
        default=None, description="The software license applied to this component."
    )
    purl: str | None = Field(
        default=None,
        description="The Package URL (PURL) to identify the software component. This is a URL that uniquely identifies the component, including the component's name, version, and type. The URL is used to locate and retrieve the component's metadata and content. [Recommended]",
    )
    related_component: str | None = Field(
        default=None,
        description="The package URL (PURL) of the component that this software component has a relationship with. [Recommended]",
    )
    relationship: str | None = Field(
        default=None,
        description="The relationship between two software components, normalized to the caption of the <code>relationship_id</code> value. In the case of 'Other', it is defined by the source.",
    )
    relationship_id: RelationshipId | None = Field(
        default=None,
        description="The normalized identifier of the relationship between two software components. [Recommended]",
    )
    type_: str | None = Field(
        default=None,
        description="The type of software component, normalized to the caption of the <code>type_id</code> value. In the case of 'Other', it is defined by the source.",
    )
    type_id: TypeId | None = Field(
        default=None, description="The type of software component. [Recommended]"
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
            ("relationship_id", "relationship", cls.RelationshipId),
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
