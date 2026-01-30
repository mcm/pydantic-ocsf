"""Device object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_1_0.objects.device_hw_info import DeviceHwInfo
    from ocsf.v1_1_0.objects.group import Group
    from ocsf.v1_1_0.objects.image import Image
    from ocsf.v1_1_0.objects.location import Location
    from ocsf.v1_1_0.objects.network_interface import NetworkInterface
    from ocsf.v1_1_0.objects.organization import Organization
    from ocsf.v1_1_0.objects.os import Os


class Device(OCSFBaseModel):
    """The Device object represents an addressable computer system or host, which is typically connected to a computer network and participates in the transmission or processing of data within the computer network. Defined by D3FEND <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:Host/'>d3f:Host</a>.

    See: https://schema.ocsf.io/1.1.0/objects/device
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The device type ID.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                99: "Other",
            }

    class RiskLevelId(SiblingEnum):
        """The normalized risk level id.

        OCSF Attribute: risk_level_id
        """

        INFO = 0
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        CRITICAL = 4

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Info",
                1: "Low",
                2: "Medium",
                3: "High",
                4: "Critical",
            }

    type_id: TypeId = Field(..., description="The device type ID.")
    autoscale_uid: str | None = Field(
        default=None, description="The unique identifier of the cloud autoscale configuration."
    )
    created_time: int | None = Field(
        default=None, description="The time when the device was known to have been created."
    )
    desc: str | None = Field(
        default=None,
        description="The description of the device, ordinarily as reported by the operating system.",
    )
    domain: str | None = Field(
        default=None,
        description="The network domain where the device resides. For example: <code>work.example.com</code>.",
    )
    first_seen_time: int | None = Field(
        default=None, description="The initial discovery time of the device."
    )
    groups: list[Group] | None = Field(
        default=None,
        description='The group names to which the device belongs. For example: <code>["Windows Laptops", "Engineering"]<code/>.',
    )
    hostname: Any | None = Field(default=None, description="The device hostname.")
    hw_info: DeviceHwInfo | None = Field(
        default=None, description="The endpoint hardware information."
    )
    hypervisor: str | None = Field(
        default=None,
        description="The name of the hypervisor running on the device. For example, <code>Xen</code>, <code>VMware</code>, <code>Hyper-V</code>, <code>VirtualBox</code>, etc.",
    )
    image: Image | None = Field(
        default=None, description="The image used as a template to run the virtual machine."
    )
    imei: str | None = Field(
        default=None,
        description="The International Mobile Station Equipment Identifier that is associated with the device.",
    )
    include: str | None = Field(default=None, description="")
    instance_uid: str | None = Field(
        default=None, description="The unique identifier of a VM instance. [Recommended]"
    )
    interface_name: str | None = Field(
        default=None, description="The name of the network interface (e.g. eth2). [Recommended]"
    )
    interface_uid: str | None = Field(
        default=None, description="The unique identifier of the network interface. [Recommended]"
    )
    ip: Any | None = Field(
        default=None, description="The device IP address, in either IPv4 or IPv6 format."
    )
    is_compliant: bool | None = Field(
        default=None, description="The event occurred on a compliant device."
    )
    is_managed: bool | None = Field(
        default=None, description="The event occurred on a managed device."
    )
    is_personal: bool | None = Field(
        default=None, description="The event occurred on a personal device."
    )
    is_trusted: bool | None = Field(
        default=None, description="The event occurred on a trusted device."
    )
    last_seen_time: int | None = Field(
        default=None, description="The most recent discovery time of the device."
    )
    location: Location | None = Field(
        default=None, description="The geographical location of the device."
    )
    mac: Any | None = Field(
        default=None, description="The Media Access Control (MAC) address of the endpoint."
    )
    modified_time: int | None = Field(
        default=None, description="The time when the device was last known to have been modified."
    )
    name: str | None = Field(
        default=None,
        description="The alternate device name, ordinarily as assigned by an administrator. <p><b>Note:</b> The <b>Name</b> could be any other string that helps to identify the device, such as a phone number; for example <code>310-555-1234</code>.</p>",
    )
    network_interfaces: list[NetworkInterface] | None = Field(
        default=None,
        description="The network interfaces that are associated with the device, one for each unique MAC address/IP address/hostname/name combination.<p><b>Note:</b> The first element of the array is the network information that pertains to the event.</p>",
    )
    org: Organization | None = Field(
        default=None, description="Organization and org unit related to the device."
    )
    os: Os | None = Field(default=None, description="The endpoint operating system.")
    region: str | None = Field(
        default=None,
        description="The region where the virtual machine is located. For example, an AWS Region. [Recommended]",
    )
    risk_level: str | None = Field(
        default=None,
        description="The risk level, normalized to the caption of the risk_level_id value. In the case of 'Other', it is defined by the event source.",
    )
    risk_level_id: RiskLevelId | None = Field(
        default=None, description="The normalized risk level id."
    )
    risk_score: int | None = Field(
        default=None, description="The risk score as reported by the event source."
    )
    subnet: Any | None = Field(default=None, description="The subnet mask.")
    subnet_uid: str | None = Field(
        default=None, description="The unique identifier of a virtual subnet."
    )
    type_: str | None = Field(
        default=None,
        description="The device type. For example: <code>unknown</code>, <code>server</code>, <code>desktop</code>, <code>laptop</code>, <code>tablet</code>, <code>mobile</code>, <code>virtual</code>, <code>browser</code>, or <code>other</code>.",
    )
    uid: str | None = Field(
        default=None,
        description="The unique identifier of the device. For example the Windows TargetSID or AWS EC2 ARN.",
    )
    uid_alt: str | None = Field(
        default=None,
        description="An alternate unique identifier of the device if any. For example the ActiveDirectory DN.",
    )
    vlan_uid: str | None = Field(default=None, description="The Virtual LAN identifier.")
    vpc_uid: str | None = Field(
        default=None, description="The unique identifier of the Virtual Private Cloud (VPC)."
    )
    zone: str | None = Field(default=None, description="The network zone or LAN segment.")

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
            ("risk_level_id", "risk_level", cls.RiskLevelId),
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
