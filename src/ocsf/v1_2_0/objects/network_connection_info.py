"""Network Connection Information object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_2_0.objects.session import Session


class NetworkConnectionInfo(OCSFBaseModel):
    """The Network Connection Information object describes characteristics of a network connection. Defined by D3FEND <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:NetworkSession/'>d3f:NetworkSession</a>.

    See: https://schema.ocsf.io/1.2.0/objects/network_connection_info
    """

    # Nested Enums for sibling attribute pairs
    class BoundaryId(SiblingEnum):
        """<p>The normalized identifier of the boundary of the connection. </p><p> For cloud connections, this translates to the traffic-boundary (same VPC, through IGW, etc.). For traditional networks, this is described as Local, Internal, or External.</p>

        OCSF Attribute: boundary_id
        """

        UNKNOWN = 0
        LOCALHOST = 1
        INTERNAL = 2
        EXTERNAL = 3
        SAME_VPC = 4
        INTERNETVPC_GATEWAY = 5
        VIRTUAL_PRIVATE_GATEWAY = 6
        INTRA_REGION_VPC = 7
        INTER_REGION_VPC = 8
        LOCAL_GATEWAY = 9
        GATEWAY_VPC = 10
        INTERNET_GATEWAY = 11
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Localhost",
                2: "Internal",
                3: "External",
                4: "Same VPC",
                5: "Internet/VPC Gateway",
                6: "Virtual Private Gateway",
                7: "Intra-region VPC",
                8: "Inter-region VPC",
                9: "Local Gateway",
                10: "Gateway VPC",
                11: "Internet Gateway",
                99: "Other",
            }

    class DirectionId(SiblingEnum):
        """The normalized identifier of the direction of the initiated connection, traffic, or email.

        OCSF Attribute: direction_id
        """

        UNKNOWN = 0
        INBOUND = 1
        OUTBOUND = 2
        LATERAL = 3
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Inbound",
                2: "Outbound",
                3: "Lateral",
                99: "Other",
            }

    class ProtocolVerId(SiblingEnum):
        """The Internet Protocol version identifier.

        OCSF Attribute: protocol_ver_id
        """

        UNKNOWN = 0
        INTERNET_PROTOCOL_VERSION_4_IPV4 = 4
        INTERNET_PROTOCOL_VERSION_6_IPV6 = 6
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                4: "Internet Protocol version 4 (IPv4)",
                6: "Internet Protocol version 6 (IPv6)",
                99: "Other",
            }

    direction_id: DirectionId = Field(
        ...,
        description="The normalized identifier of the direction of the initiated connection, traffic, or email.",
    )
    boundary: str | None = Field(
        default=None,
        description="The boundary of the connection, normalized to the caption of 'boundary_id'. In the case of 'Other', it is defined by the event source. <p> For cloud connections, this translates to the traffic-boundary(same VPC, through IGW, etc.). For traditional networks, this is described as Local, Internal, or External.</p>",
    )
    boundary_id: BoundaryId | None = Field(
        default=None,
        description="<p>The normalized identifier of the boundary of the connection. </p><p> For cloud connections, this translates to the traffic-boundary (same VPC, through IGW, etc.). For traditional networks, this is described as Local, Internal, or External.</p>",
    )
    direction: str | None = Field(
        default=None,
        description="The direction of the initiated connection, traffic, or email, normalized to the caption of the direction_id value. In the case of 'Other', it is defined by the event source.",
    )
    protocol_name: str | None = Field(
        default=None,
        description="The TCP/IP protocol name in lowercase, as defined by the Internet Assigned Numbers Authority (IANA). See <a target='_blank' href='https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml'>Protocol Numbers</a>. For example: <code>tcp</code> or <code>udp</code>.",
    )
    protocol_num: int | None = Field(
        default=None,
        description="The TCP/IP protocol number, as defined by the Internet Assigned Numbers Authority (IANA). Use -1 if the protocol is not defined by IANA. See <a target='_blank' href='https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml'>Protocol Numbers</a>. For example: <code>6</code> for TCP and <code>17</code> for UDP. [Recommended]",
    )
    protocol_ver: str | None = Field(default=None, description="The Internet Protocol version.")
    protocol_ver_id: ProtocolVerId | None = Field(
        default=None, description="The Internet Protocol version identifier."
    )
    session: Session | None = Field(
        default=None, description="The authenticated user or service session."
    )
    tcp_flags: int | None = Field(
        default=None, description="The network connection TCP header flags (i.e., control bits)."
    )
    uid: str | None = Field(default=None, description="The unique identifier of the connection.")

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
            ("boundary_id", "boundary", cls.BoundaryId),
            ("direction_id", "direction", cls.DirectionId),
            ("protocol_ver_id", "protocol_ver", cls.ProtocolVerId),
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
