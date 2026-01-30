"""Software Package object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.fingerprint import Fingerprint


class Package(OCSFBaseModel):
    """The Software Package object describes details about a software package.

    See: https://schema.ocsf.io/1.6.0/objects/package
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The type of software package.

        OCSF Attribute: type_id
        """

        APPLICATION = 1
        OPERATING_SYSTEM = 2

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "Application",
                2: "Operating System",
            }

    name: str = Field(..., description="The software package name.")
    version: str = Field(..., description="The software package version.")
    architecture: str | None = Field(
        default=None,
        description="Architecture is a shorthand name describing the type of computer hardware the packaged software is meant to run on. [Recommended]",
    )
    cpe_name: str | None = Field(
        default=None,
        description="The Common Platform Enumeration (CPE) name as described by (<a target='_blank' href='https://nvd.nist.gov/products/cpe'>NIST</a>) For example: <code>cpe:/a:apple:safari:16.2</code>.",
    )
    epoch: int | None = Field(
        default=None,
        description="The software package epoch. Epoch is a way to define weighted dependencies based on version numbers.",
    )
    hash: Fingerprint | None = Field(
        default=None,
        description="Cryptographic hash to identify the binary instance of a software component. This can include any component such file, package, or library.",
    )
    license: str | None = Field(
        default=None, description="The software license applied to this package."
    )
    license_url: Any | None = Field(
        default=None,
        description="The URL pointing to the license applied on package or software. This is typically a <code>LICENSE.md</code> file within a repository.",
    )
    package_manager: str | None = Field(
        default=None,
        description="The software packager manager utilized to manage a package on a system, e.g. npm, yum, dpkg etc.",
    )
    package_manager_url: Any | None = Field(
        default=None,
        description="The URL of the package or library at the package manager, or the specific URL or URI of an internal package manager link such as <code>AWS CodeArtifact</code> or <code>Artifactory</code>.",
    )
    purl: str | None = Field(
        default=None,
        description="A purl is a URL string used to identify and locate a software package in a mostly universal and uniform way across programming languages, package managers, packaging conventions, tools, APIs and databases.",
    )
    release: str | None = Field(
        default=None,
        description="Release is the number of times a version of the software has been packaged.",
    )
    src_url: Any | None = Field(
        default=None,
        description="The link to the specific library or package such as within <code>GitHub</code>, this is different from the link to the package manager where the library or package is hosted.",
    )
    type_: str | None = Field(
        default=None,
        description="The type of software package, normalized to the caption of the <code>type_id</code> value. In the case of 'Other', it is defined by the source.",
    )
    type_id: TypeId | None = Field(
        default=None, description="The type of software package. [Recommended]"
    )
    uid: str | None = Field(
        default=None,
        description="A unique identifier for the package or library reported by the source tool. E.g., the <code>libId</code> within the <code>sbom</code> field of an OX Security Issue or the SPDX <code>components.*.bom-ref</code>.",
    )
    vendor_name: str | None = Field(
        default=None, description="The name of the vendor who published the software package."
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
