"""Module object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_0_0.objects.file import File


class Module(OCSFBaseModel):
    """The Module object describes the load attributes of a module.

    See: https://schema.ocsf.io/1.0.0/objects/module
    """

    # Nested Enums for sibling attribute pairs
    class LoadTypeId(SiblingEnum):
        """The normalized identifier of the load type. It identifies how the module was loaded in memory.

        OCSF Attribute: load_type_id
        """

        UNKNOWN = 0
        STANDARD = 1
        NON_STANDARD = 2
        SHELLCODE = 3
        MAPPED = 4
        NONSTANDARD_BACKED = 5
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Standard",
                2: "Non Standard",
                3: "ShellCode",
                4: "Mapped",
                5: "NonStandard Backed",
                99: "Other",
            }

    load_type_id: LoadTypeId = Field(
        ...,
        description="The normalized identifier of the load type. It identifies how the module was loaded in memory.",
    )
    base_address: str | None = Field(
        default=None, description="The memory address where the module was loaded. [Recommended]"
    )
    file: File | None = Field(default=None, description="The module file object. [Recommended]")
    function_name: str | None = Field(
        default=None,
        description="The entry-point function of the module. The system calls the entry-point function whenever a process or thread loads or unloads the module.",
    )
    load_type: str | None = Field(
        default=None,
        description="The load type, normalized to the caption of the load_type_id value. In the case of 'Other', it is defined by the event source. It describes how the module was loaded in memory.",
    )
    start_address: str | None = Field(
        default=None, description="The start address of the execution. [Recommended]"
    )
    type_: str | None = Field(default=None, description="The module type. [Recommended]")

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
            ("load_type_id", "load_type", cls.LoadTypeId),
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
