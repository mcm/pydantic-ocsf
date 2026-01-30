"""Software Bill of Materials object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.package import Package
    from ocsf.v1_6_0.objects.product import Product
    from ocsf.v1_6_0.objects.software_component import SoftwareComponent


class Sbom(OCSFBaseModel):
    """The Software Bill of Materials object describes characteristics of a generated SBOM.

    See: https://schema.ocsf.io/1.6.0/objects/sbom
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The type of SBOM.

        OCSF Attribute: type_id
        """

        SPDX = 1
        CYCLONEDX = 2
        SWID = 3

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "SPDX",
                2: "CycloneDX",
                3: "SWID",
            }

    package: Package = Field(
        ...,
        description="The software package or library that is being discovered or inventoried by an SBOM.",
    )
    software_components: list[SoftwareComponent] = Field(
        ..., description="The list of software components used in the software package."
    )
    created_time: int | None = Field(
        default=None, description="The time when the SBOM was created. [Recommended]"
    )
    product: Product | None = Field(
        default=None,
        description="Details about the upstream product that generated the SBOM e.g. <code>cdxgen</code> or <code>Syft</code>. [Recommended]",
    )
    type_: str | None = Field(
        default=None,
        description="The type of SBOM, normalized to the caption of the <code>type_id</code> value. In the case of 'Other', it is defined by the source.",
    )
    type_id: TypeId | None = Field(default=None, description="The type of SBOM. [Recommended]")
    uid: str | None = Field(
        default=None,
        description="A unique identifier for the SBOM or the SBOM generation by a source tool, such as the SPDX <code>metadata.component.bom-ref</code>.",
    )
    version: str | None = Field(
        default=None,
        description="The specification (spec) version of the particular SBOM, e.g., <code>1.6</code>.",
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
