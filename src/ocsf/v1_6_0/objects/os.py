"""Operating System (OS) object."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum


class Os(OCSFBaseModel):
    """The Operating System (OS) object describes characteristics of an OS, such as Linux or Windows.

    See: https://schema.ocsf.io/1.6.0/objects/os
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The type identifier of the operating system.

        OCSF Attribute: type_id
        """

        WINDOWS = 100
        WINDOWS_MOBILE = 101
        LINUX = 200
        ANDROID = 201
        MACOS = 300
        IOS = 301
        IPADOS = 302
        SOLARIS = 400
        AIX = 401
        HP_UX = 402

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                100: "Windows",
                101: "Windows Mobile",
                200: "Linux",
                201: "Android",
                300: "macOS",
                301: "iOS",
                302: "iPadOS",
                400: "Solaris",
                401: "AIX",
                402: "HP-UX",
            }

    name: str = Field(..., description="The operating system name.")
    type_id: TypeId = Field(..., description="The type identifier of the operating system.")
    build: str | None = Field(default=None, description="The operating system build number.")
    country: str | None = Field(
        default=None,
        description="The operating system country code, as defined by the ISO 3166-1 standard (Alpha-2 code).<p><b>Note:</b> The two letter country code should be capitalized. For example: <code>US</code> or <code>CA</code>.</p>",
    )
    cpe_name: str | None = Field(
        default=None,
        description="The Common Platform Enumeration (CPE) name as described by (<a target='_blank' href='https://nvd.nist.gov/products/cpe'>NIST</a>) For example: <code>cpe:/a:apple:safari:16.2</code>.",
    )
    cpu_bits: int | None = Field(
        default=None,
        description="The cpu architecture, the number of bits used for addressing in memory. For example: <code>32</code> or <code>64</code>.",
    )
    edition: str | None = Field(
        default=None,
        description="The operating system edition. For example: <code>Professional</code>.",
    )
    kernel_release: str | None = Field(
        default=None,
        description='The kernel release of the operating system. On Unix-based systems, this is determined from the <code>uname -r</code> command output, for example "5.15.0-122-generic".',
    )
    lang: str | None = Field(
        default=None,
        description="The two letter lower case language codes, as defined by <a target='_blank' href='https://en.wikipedia.org/wiki/ISO_639-1'>ISO 639-1</a>. For example: <code>en</code> (English), <code>de</code> (German), or <code>fr</code> (French).",
    )
    sp_name: str | None = Field(default=None, description="The name of the latest Service Pack.")
    sp_ver: int | None = Field(
        default=None, description="The version number of the latest Service Pack."
    )
    type_: str | None = Field(default=None, description="The type of the operating system.")
    version: str | None = Field(
        default=None,
        description='The version of the OS running on the device that originated the event. For example: "Windows 10", "OS X 10.7", or "iOS 9".',
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
