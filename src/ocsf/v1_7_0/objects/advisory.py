"""Advisory object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_7_0.objects.cve import Cve
    from ocsf.v1_7_0.objects.cwe import Cwe
    from ocsf.v1_7_0.objects.os import Os
    from ocsf.v1_7_0.objects.product import Product
    from ocsf.v1_7_0.objects.timespan import Timespan


class Advisory(OCSFBaseModel):
    """The Advisory object represents publicly disclosed cybersecurity vulnerabilities defined in a Security advisory. e.g. <code> Microsoft KB Article</code>, <code>Apple Security Advisory</code>, or a <code>GitHub Security Advisory (GHSA)</code>

    See: https://schema.ocsf.io/1.7.0/objects/advisory
    """

    # Nested Enums for sibling attribute pairs
    class InstallStateId(SiblingEnum):
        """The normalized install state ID of the Advisory.

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

    uid: str = Field(
        ...,
        description="The unique identifier assigned to the advisory or disclosed vulnerability, e.g, <code>GHSA-5mrr-rgp6-x4gr</code>.",
    )
    avg_timespan: Timespan | None = Field(default=None, description="The average time to patch.")
    bulletin: str | None = Field(default=None, description="The Advisory bulletin identifier.")
    classification: str | None = Field(
        default=None, description="The vendors classification of the Advisory."
    )
    created_time: int | None = Field(
        default=None, description="The time when the Advisory record was created. [Recommended]"
    )
    desc: str | None = Field(
        default=None, description="A brief description of the Advisory Record."
    )
    install_state: str | None = Field(
        default=None, description="The install state of the Advisory. [Recommended]"
    )
    install_state_id: InstallStateId | None = Field(
        default=None, description="The normalized install state ID of the Advisory. [Recommended]"
    )
    is_superseded: bool | None = Field(
        default=None, description="The Advisory has been replaced by another."
    )
    modified_time: int | None = Field(
        default=None, description="The time when the Advisory record was last updated."
    )
    os: Os | None = Field(
        default=None, description="The operating system the Advisory applies to. [Recommended]"
    )
    product: Product | None = Field(
        default=None, description="The product where the vulnerability was discovered."
    )
    references: list[str] | None = Field(
        default=None,
        description="A list of reference URLs with additional information about the vulnerabilities disclosed in the Advisory. [Recommended]",
    )
    related_cves: list[Cve] | None = Field(
        default=None,
        description="A list of Common Vulnerabilities and Exposures <a target='_blank' href='https://cve.mitre.org/'>(CVE)</a> identifiers related to the vulnerabilities disclosed in the Advisory.",
    )
    related_cwes: list[Cwe] | None = Field(
        default=None,
        description="A list of Common Weakness Enumeration <a target='_blank' href='https://cwe.mitre.org/'>(CWE)</a> identifiers related to the vulnerabilities disclosed in the Advisory.",
    )
    size: int | None = Field(
        default=None,
        description="The size in bytes for the Advisory. Usually populated for a KB Article patch.",
    )
    src_url: Any | None = Field(
        default=None, description="The Advisory link from the source vendor."
    )
    title: str | None = Field(
        default=None,
        description="A title or a brief phrase summarizing the Advisory. [Recommended]",
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
