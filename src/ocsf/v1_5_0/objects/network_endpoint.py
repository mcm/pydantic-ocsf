"""Network Endpoint object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_5_0.objects.agent import Agent
    from ocsf.v1_5_0.objects.autonomous_system import AutonomousSystem
    from ocsf.v1_5_0.objects.device_hw_info import DeviceHwInfo
    from ocsf.v1_5_0.objects.location import Location
    from ocsf.v1_5_0.objects.network_proxy import NetworkProxy
    from ocsf.v1_5_0.objects.os import Os
    from ocsf.v1_5_0.objects.user import User


class NetworkEndpoint(OCSFBaseModel):
    """The Network Endpoint object describes characteristics of a network endpoint. These can be a source or destination of a network connection.

    See: https://schema.ocsf.io/1.5.0/objects/network_endpoint
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The network endpoint type ID.

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

    agent_list: list[Agent] | None = Field(
        default=None,
        description="A list of <code>agent</code> objects associated with a device, endpoint, or resource.",
    )
    autonomous_system: AutonomousSystem | None = Field(
        default=None, description="The Autonomous System details associated with an IP address."
    )
    domain: str | None = Field(
        default=None,
        description="The name of the domain that the endpoint belongs to or that corresponds to the endpoint.",
    )
    hostname: Any | None = Field(
        default=None, description="The fully qualified name of the endpoint. [Recommended]"
    )
    hw_info: DeviceHwInfo | None = Field(
        default=None, description="The endpoint hardware information."
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
    intermediate_ips: list[Any] | None = Field(
        default=None,
        description="The intermediate IP Addresses. For example, the IP addresses in the HTTP X-Forwarded-For header.",
    )
    ip: Any | None = Field(
        default=None,
        description="The IP address of the endpoint, in either IPv4 or IPv6 format. [Recommended]",
    )
    isp: str | None = Field(
        default=None, description="The name of the Internet Service Provider (ISP)."
    )
    isp_org: str | None = Field(
        default=None,
        description="The organization name of the Internet Service Provider (ISP). This represents the parent organization or company that owns/operates the ISP. For example, Comcast Corporation would be the ISP org for Xfinity internet service. This attribute helps identify the ultimate provider when ISPs operate under different brand names.",
    )
    location: Location | None = Field(
        default=None, description="The geographical location of the endpoint."
    )
    mac: Any | None = Field(
        default=None, description="The Media Access Control (MAC) address of the endpoint."
    )
    name: str | None = Field(default=None, description="The short name of the endpoint.")
    os: Os | None = Field(default=None, description="The endpoint operating system.")
    owner: User | None = Field(
        default=None,
        description="The identity of the service or user account that owns the endpoint or was last logged into it. [Recommended]",
    )
    port: Any | None = Field(
        default=None,
        description="The port used for communication within the network connection. [Recommended]",
    )
    proxy_endpoint: NetworkProxy | None = Field(
        default=None,
        description="The network proxy information pertaining to a specific endpoint. This can be used to describe information pertaining to network address translation (NAT).",
    )
    subnet_uid: str | None = Field(
        default=None, description="The unique identifier of a virtual subnet."
    )
    svc_name: str | None = Field(
        default=None,
        description="The service name in service-to-service connections. For example, AWS VPC logs the pkt-src-aws-service and pkt-dst-aws-service fields identify the connection is coming from or going to an AWS service. [Recommended]",
    )
    type_: str | None = Field(
        default=None,
        description="The network endpoint type. For example: <code>unknown</code>, <code>server</code>, <code>desktop</code>, <code>laptop</code>, <code>tablet</code>, <code>mobile</code>, <code>virtual</code>, <code>browser</code>, or <code>other</code>.",
    )
    type_id: TypeId | None = Field(default=None, description="The network endpoint type ID.")
    uid: str | None = Field(default=None, description="The unique identifier of the endpoint.")
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
