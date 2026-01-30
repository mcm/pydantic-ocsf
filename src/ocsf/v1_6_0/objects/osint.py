"""OSINT object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.enums.osint_tlp import OsintTlp
    from ocsf.v1_6_0.objects.analytic import Analytic
    from ocsf.v1_6_0.objects.attack import Attack
    from ocsf.v1_6_0.objects.autonomous_system import AutonomousSystem
    from ocsf.v1_6_0.objects.campaign import Campaign
    from ocsf.v1_6_0.objects.digital_signature import DigitalSignature
    from ocsf.v1_6_0.objects.dns_answer import DnsAnswer
    from ocsf.v1_6_0.objects.email import Email
    from ocsf.v1_6_0.objects.email_auth import EmailAuth
    from ocsf.v1_6_0.objects.file import File
    from ocsf.v1_6_0.objects.kill_chain_phase import KillChainPhase
    from ocsf.v1_6_0.objects.location import Location
    from ocsf.v1_6_0.objects.malware import Malware
    from ocsf.v1_6_0.objects.reputation import Reputation
    from ocsf.v1_6_0.objects.script import Script
    from ocsf.v1_6_0.objects.threat_actor import ThreatActor
    from ocsf.v1_6_0.objects.user import User
    from ocsf.v1_6_0.objects.vulnerability import Vulnerability
    from ocsf.v1_6_0.objects.whois import Whois


class Osint(OCSFBaseModel):
    """The OSINT (Open Source Intelligence) object contains details related to an indicator such as the indicator itself, related indicators, geolocation, registrar information, subdomains, analyst commentary, and other contextual information. This information can be used to further enrich a detection or finding by providing decisioning support to other analysts and engineers.

    See: https://schema.ocsf.io/1.6.0/objects/osint
    """

    # Nested Enums for sibling attribute pairs
    class ConfidenceId(SiblingEnum):
        """The normalized confidence refers to the accuracy of collected information related to the OSINT or how pertinent an indicator or analysis is to a specific event or finding. A low confidence means that the information collected or analysis conducted lacked detail or is not accurate enough to qualify an indicator as fully malicious.

        OCSF Attribute: confidence_id
        """

        UNKNOWN = 0
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Low",
                2: "Medium",
                3: "High",
                99: "Other",
            }

    class DetectionPatternTypeId(SiblingEnum):
        """Specifies the type of detection pattern used to identify the associated threat indicator.

        OCSF Attribute: detection_pattern_type_id
        """

        UNKNOWN = 0
        STIX = 1
        PCRE = 2
        SIGMA = 3
        SNORT = 4
        SURICATA = 5
        YARA = 6
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "STIX",
                2: "PCRE",
                3: "SIGMA",
                4: "Snort",
                5: "Suricata",
                6: "YARA",
                99: "Other",
            }

    class SeverityId(SiblingEnum):
        """The normalized severity level of the threat indicator, typically reflecting its potential impact or damage.

        OCSF Attribute: severity_id
        """

        UNKNOWN = 0
        INFORMATIONAL = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4
        CRITICAL = 5
        FATAL = 6
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Informational",
                2: "Low",
                3: "Medium",
                4: "High",
                5: "Critical",
                6: "Fatal",
                99: "Other",
            }

    class TypeId(SiblingEnum):
        """The OSINT indicator type ID.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        IP_ADDRESS = 1
        DOMAIN = 2
        HOSTNAME = 3
        HASH = 4
        URL = 5
        USER_AGENT = 6
        DIGITAL_CERTIFICATE = 7
        EMAIL = 8
        EMAIL_ADDRESS = 9
        VULNERABILITY = 10
        FILE = 11
        REGISTRY_KEY = 12
        REGISTRY_VALUE = 13
        COMMAND_LINE = 14
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "IP Address",
                2: "Domain",
                3: "Hostname",
                4: "Hash",
                5: "URL",
                6: "User Agent",
                7: "Digital Certificate",
                8: "Email",
                9: "Email Address",
                10: "Vulnerability",
                11: "File",
                12: "Registry Key",
                13: "Registry Value",
                14: "Command Line",
                99: "Other",
            }

    type_id: TypeId = Field(..., description="The OSINT indicator type ID.")
    value: str = Field(
        ...,
        description="The actual indicator value in scope, e.g., a SHA-256 hash hexdigest or a domain name.",
    )
    answers: list[DnsAnswer] | None = Field(
        default=None,
        description="Any pertinent DNS answers information related to an indicator or OSINT analysis.",
    )
    attacks: list[Attack] | None = Field(
        default=None,
        description="MITRE ATT&CK Tactics, Techniques, and/or Procedures (TTPs) pertinent to an indicator or OSINT analysis.",
    )
    autonomous_system: AutonomousSystem | None = Field(
        default=None,
        description="Any pertinent autonomous system information related to an indicator or OSINT analysis.",
    )
    campaign: Campaign | None = Field(
        default=None,
        description="The campaign object describes details about the campaign that was the source of the activity.",
    )
    category: str | None = Field(
        default=None,
        description="Categorizes the threat indicator based on its functional or operational role.",
    )
    comment: str | None = Field(
        default=None,
        description="Analyst commentary or source commentary about an indicator or OSINT analysis.",
    )
    confidence: str | None = Field(
        default=None,
        description="The confidence of an indicator being malicious and/or pertinent, normalized to the caption of the confidence_id value. In the case of 'Other', it is defined by the event source or analyst.",
    )
    confidence_id: ConfidenceId | None = Field(
        default=None,
        description="The normalized confidence refers to the accuracy of collected information related to the OSINT or how pertinent an indicator or analysis is to a specific event or finding. A low confidence means that the information collected or analysis conducted lacked detail or is not accurate enough to qualify an indicator as fully malicious. [Recommended]",
    )
    created_time: int | None = Field(
        default=None,
        description="The timestamp when the indicator was initially created or identified.",
    )
    creator: User | None = Field(
        default=None,
        description="The identifier of the user, system, or organization that contributed the indicator.",
    )
    desc: str | None = Field(
        default=None,
        description="A detailed explanation of the indicator, including its context, purpose, and relevance.",
    )
    detection_pattern: str | None = Field(
        default=None,
        description="The specific detection pattern or signature associated with the indicator.",
    )
    detection_pattern_type: str | None = Field(
        default=None,
        description="The detection pattern type, normalized to the caption of the detection_pattern_type_id value. In the case of 'Other', it is defined by the event source.",
    )
    detection_pattern_type_id: DetectionPatternTypeId | None = Field(
        default=None,
        description="Specifies the type of detection pattern used to identify the associated threat indicator.",
    )
    email: Email | None = Field(
        default=None,
        description="Any email information pertinent to an indicator or OSINT analysis.",
    )
    email_auth: EmailAuth | None = Field(
        default=None,
        description="Any email authentication information pertinent to an indicator or OSINT analysis.",
    )
    expiration_time: int | None = Field(
        default=None,
        description="The expiration date of the indicator, after which it is no longer considered reliable.",
    )
    external_uid: str | None = Field(
        default=None,
        description="A unique identifier assigned by an external system for cross-referencing.",
    )
    file: File | None = Field(
        default=None,
        description="Any pertinent file information related to an indicator or OSINT analysis.",
    )
    intrusion_sets: list[str] | None = Field(
        default=None,
        description="A grouping of adversarial behaviors and resources believed to be associated with specific threat actors or campaigns. Intrusion sets often encompass multiple campaigns and are used to organize related activities under a common label.",
    )
    kill_chain: list[KillChainPhase] | None = Field(
        default=None,
        description="Lockheed Martin Kill Chain Phases pertinent to an indicator or OSINT analysis.",
    )
    labels: list[str] | None = Field(
        default=None,
        description="Tags or keywords associated with the indicator to enhance searchability.",
    )
    location: Location | None = Field(
        default=None,
        description="Any pertinent geolocation information related to an indicator or OSINT analysis.",
    )
    malware: list[Malware] | None = Field(
        default=None,
        description="A list of Malware objects, describing details about the identified malware.",
    )
    modified_time: int | None = Field(
        default=None,
        description="The timestamp of the last modification or update to the indicator.",
    )
    name: str | None = Field(
        default=None,
        description="The <code>name</code> is a pointer/reference to an attribute within the OCSF event data. For example: file.name.",
    )
    references: list[str] | None = Field(
        default=None,
        description="Provides a reference to an external source of information related to the CTI being represented. This may include a URL, a document, or some other type of reference that provides additional context or information about the CTI.",
    )
    related_analytics: list[Analytic] | None = Field(
        default=None, description="Any analytics related to an indicator or OSINT analysis."
    )
    reputation: Reputation | None = Field(
        default=None,
        description="Related reputational analysis from third-party engines and analysts for a given indicator or OSINT analysis.",
    )
    risk_score: int | None = Field(
        default=None, description="A numerical representation of the threat indicator’s risk level."
    )
    script: Script | None = Field(
        default=None,
        description="Any pertinent script information related to an indicator or OSINT analysis.",
    )
    severity: str | None = Field(
        default=None,
        description="Represents the severity level of the threat indicator, typically reflecting its potential impact or damage.",
    )
    severity_id: SeverityId | None = Field(
        default=None,
        description="The normalized severity level of the threat indicator, typically reflecting its potential impact or damage.",
    )
    signatures: list[DigitalSignature] | None = Field(
        default=None,
        description="Any digital signatures or hashes related to an indicator or OSINT analysis.",
    )
    src_url: Any | None = Field(
        default=None,
        description="The source URL of an indicator or OSINT analysis, e.g., a URL back to a TIP, report, or otherwise.",
    )
    subdomains: list[str] | None = Field(
        default=None,
        description="Any pertinent subdomain information - such as those generated by a Domain Generation Algorithm - related to an indicator or OSINT analysis.",
    )
    subnet: Any | None = Field(
        default=None,
        description="A CIDR or network block related to an indicator or OSINT analysis.",
    )
    threat_actor: ThreatActor | None = Field(
        default=None,
        description="A threat actor is an individual or group that conducts malicious cyber activities, often with financial, political, or ideological motives.",
    )
    tlp: OsintTlp | None = Field(
        default=None,
        description="The <a target='_blank' href='https://www.first.org/tlp/'>Traffic Light Protocol</a> was created to facilitate greater sharing of potentially sensitive information and more effective collaboration. TLP provides a simple and intuitive schema for indicating with whom potentially sensitive information can be shared. [Recommended]",
    )
    type_: str | None = Field(default=None, description="The OSINT indicator type.")
    uid: str | None = Field(default=None, description="The unique identifier for the OSINT object.")
    uploaded_time: int | None = Field(
        default=None,
        description="The timestamp indicating when the associated indicator or intelligence was added to the system or repository.",
    )
    vendor_name: str | None = Field(
        default=None,
        description="The vendor name of a tool which generates intelligence or provides indicators.",
    )
    vulnerabilities: list[Vulnerability] | None = Field(
        default=None, description="Any vulnerabilities related to an indicator or OSINT analysis."
    )
    whois: Whois | None = Field(
        default=None,
        description="Any pertinent WHOIS information related to an indicator or OSINT analysis.",
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
            ("confidence_id", "confidence", cls.ConfidenceId),
            ("detection_pattern_type_id", "detection_pattern_type", cls.DetectionPatternTypeId),
            ("severity_id", "severity", cls.SeverityId),
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
