"""Device Hardware Info object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.display import Display
    from ocsf.v1_6_0.objects.keyboard_info import KeyboardInfo


class DeviceHwInfo(OCSFBaseModel):
    """The Device Hardware Information object contains details and specifications of the physical components that make up a device. This information provides an overview of the hardware capabilities, configuration, and characteristics of the device.

    See: https://schema.ocsf.io/1.6.0/objects/device_hw_info
    """

    # Nested Enums for sibling attribute pairs
    class CpuArchitectureId(SiblingEnum):
        """The normalized identifier of the CPU architecture.

        OCSF Attribute: cpu_architecture_id
        """

        UNKNOWN = 0
        X86 = 1
        ARM = 2
        RISC_V = 3
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "x86",
                2: "ARM",
                3: "RISC-V",
                99: "Other",
            }

    bios_date: str | None = Field(
        default=None, description="The BIOS date. For example: <code>03/31/16</code>."
    )
    bios_manufacturer: str | None = Field(
        default=None, description="The BIOS manufacturer. For example: <code>LENOVO</code>."
    )
    bios_ver: str | None = Field(
        default=None,
        description="The BIOS version. For example: <code>LENOVO G5ETA2WW (2.62)</code>.",
    )
    chassis: str | None = Field(
        default=None,
        description="The chassis type describes the system enclosure or physical form factor. Such as the following examples for Windows <a target='_blank' href='https://docs.microsoft.com/en-us/windows/win32/cimwin32prov/win32-systemenclosure'>Windows Chassis Types</a>",
    )
    cpu_architecture: str | None = Field(
        default=None,
        description="The CPU architecture, normalized to the caption of the <code>cpu_architecture_id</code> value. In the case of <code>Other</code>, it is defined by the source.",
    )
    cpu_architecture_id: CpuArchitectureId | None = Field(
        default=None, description="The normalized identifier of the CPU architecture."
    )
    cpu_bits: int | None = Field(
        default=None,
        description="The cpu architecture, the number of bits used for addressing in memory. For example: <code>32</code> or <code>64</code>.",
    )
    cpu_cores: int | None = Field(
        default=None,
        description="The number of processor cores in all installed processors. For Example: <code>42</code>.",
    )
    cpu_count: int | None = Field(
        default=None,
        description="The number of physical processors on a system. For example: <code>1</code>.",
    )
    cpu_speed: int | None = Field(
        default=None,
        description="The speed of the processor in Mhz. For Example: <code>4200</code>.",
    )
    cpu_type: str | None = Field(
        default=None,
        description="The processor type. For example: <code>x86 Family 6 Model 37 Stepping 5</code>.",
    )
    desktop_display: Display | None = Field(
        default=None, description="The desktop display affiliated with the event"
    )
    keyboard_info: KeyboardInfo | None = Field(
        default=None, description="The keyboard detailed information."
    )
    ram_size: int | None = Field(
        default=None,
        description="The total amount of installed RAM, in Megabytes. For example: <code>2048</code>.",
    )
    serial_number: str | None = Field(
        default=None, description="The device manufacturer serial number."
    )
    uuid: Any | None = Field(
        default=None,
        description="The device manufacturer assigned universally unique hardware identifier. For SMBIOS compatible devices such as those running Linux and Windows, it is the UUID member of the System Information structure in the SMBIOS information. For macOS devices, it is the Hardware UUID (also known as IOPlatformUUID in the I/O Registry).",
    )
    vendor_name: str | None = Field(default=None, description="The device manufacturer.")

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
            ("cpu_architecture_id", "cpu_architecture", cls.CpuArchitectureId),
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
