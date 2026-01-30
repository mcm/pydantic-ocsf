"""WHOIS object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.autonomous_system import AutonomousSystem
    from ocsf.v1_6_0.objects.domain_contact import DomainContact


class Whois(OCSFBaseModel):
    """The resources of a WHOIS record for a given domain. This can include domain names, IP address blocks, autonomous system information, and/or contact and registration information for a domain.

    See: https://schema.ocsf.io/1.6.0/objects/whois
    """

    # Nested Enums for sibling attribute pairs
    class DnssecStatusId(SiblingEnum):
        """Describes the normalized status of DNS Security Extensions (DNSSEC) for a domain.

        OCSF Attribute: dnssec_status_id
        """

        UNKNOWN = 0
        SIGNED = 1
        UNSIGNED = 2
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Signed",
                2: "Unsigned",
                99: "Other",
            }

    autonomous_system: AutonomousSystem | None = Field(
        default=None, description="The autonomous system information associated with a domain."
    )
    created_time: int | None = Field(
        default=None,
        description="When the domain was registered or WHOIS entry was created. [Recommended]",
    )
    dnssec_status: str | None = Field(
        default=None, description="The normalized value of dnssec_status_id."
    )
    dnssec_status_id: DnssecStatusId | None = Field(
        default=None,
        description="Describes the normalized status of DNS Security Extensions (DNSSEC) for a domain. [Recommended]",
    )
    domain: str | None = Field(
        default=None, description="The domain name corresponding to the WHOIS record. [Recommended]"
    )
    domain_contacts: list[DomainContact] | None = Field(
        default=None, description="An array of <code>Domain Contact</code> objects. [Recommended]"
    )
    email_addr: Any | None = Field(
        default=None, description="The email address for the registrar's abuse contact"
    )
    isp: str | None = Field(
        default=None, description="The name of the Internet Service Provider (ISP)."
    )
    isp_org: str | None = Field(
        default=None,
        description="The organization name of the Internet Service Provider (ISP). This represents the parent organization or company that owns/operates the ISP. For example, Comcast Corporation would be the ISP org for Xfinity internet service. This attribute helps identify the ultimate provider when ISPs operate under different brand names.",
    )
    last_seen_time: int | None = Field(
        default=None, description="When the WHOIS record was last updated or seen at. [Recommended]"
    )
    name_servers: list[str] | None = Field(
        default=None,
        description="A collection of name servers related to a domain registration or other record. [Recommended]",
    )
    phone_number: str | None = Field(
        default=None, description="The phone number for the registrar's abuse contact"
    )
    registrar: str | None = Field(default=None, description="The domain registrar. [Recommended]")
    status: str | None = Field(
        default=None,
        description="The status of a domain and its ability to be transferred, e.g., <code>clientTransferProhibited</code>. [Recommended]",
    )
    subdomains: list[str] | None = Field(
        default=None,
        description="An array of subdomain strings. Can be used to collect several subdomains such as those from Domain Generation Algorithms (DGAs).",
    )
    subnet: Any | None = Field(
        default=None, description="The IP address block (CIDR) associated with a domain."
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
            ("dnssec_status_id", "dnssec_status", cls.DnssecStatusId),
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
