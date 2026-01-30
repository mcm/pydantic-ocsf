"""KB Article object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_5_0.objects.os import Os
    from ocsf.v1_5_0.objects.product import Product
    from ocsf.v1_5_0.objects.timespan import Timespan


class KbArticle(OCSFBaseModel):
    """The KB Article object contains metadata that describes the patch or update.

    See: https://schema.ocsf.io/1.5.0/objects/kb_article
    """

    # Nested Enums for sibling attribute pairs
    class InstallStateId(SiblingEnum):
        """The normalized install state ID of the kb article.

        OCSF Attribute: install_state_id
        """

        UNKNOWN = 0
        INSTALLED = 1
        NOT_INSTALLED = 2
        INSTALLED_PENDING_REBOOT = 3
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Installed",
                2: "Not Installed",
                3: "Installed Pending Reboot",
                99: "Other",
            }

    uid: str = Field(..., description="The unique identifier for the kb article.")
    avg_timespan: Timespan | None = Field(default=None, description="The average time to patch.")
    bulletin: str | None = Field(default=None, description="The kb article bulletin identifier.")
    classification: str | None = Field(
        default=None, description="The vendors classification of the kb article."
    )
    created_time: int | None = Field(
        default=None, description="The date the kb article was released by the vendor."
    )
    install_state: str | None = Field(
        default=None, description="The install state of the kb article. [Recommended]"
    )
    install_state_id: InstallStateId | None = Field(
        default=None, description="The normalized install state ID of the kb article. [Recommended]"
    )
    is_superseded: bool | None = Field(
        default=None, description="The kb article has been replaced by another."
    )
    os: Os | None = Field(
        default=None, description="The operating system the kb article applies. [Recommended]"
    )
    product: Product | None = Field(
        default=None, description="The product details the kb article applies."
    )
    severity: str | None = Field(
        default=None, description="The severity of the kb article. [Recommended]"
    )
    size: int | None = Field(default=None, description="The size in bytes for the kb article.")
    src_url: Any | None = Field(
        default=None, description="The kb article link from the source vendor."
    )
    title: str | None = Field(
        default=None, description="The title of the kb article. [Recommended]"
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
            ("install_state_id", "install_state", cls.InstallStateId),
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
