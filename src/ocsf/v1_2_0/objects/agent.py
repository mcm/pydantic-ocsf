"""Agent object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_2_0.objects.policy import Policy


class Agent(OCSFBaseModel):
    """An Agent (also known as a Sensor) is typically installed on an Operating System (OS) and serves as a specialized software component that can be designed to monitor, detect, collect, archive, or take action. These activities and possible actions are defined by the upstream system controlling the Agent and its intended purpose. For instance, an Agent can include Endpoint Detection & Response (EDR) agents, backup/disaster recovery sensors, Application Performance Monitoring or profiling sensors, and similar software.

    See: https://schema.ocsf.io/1.2.0/objects/agent
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The normalized representation of an agent or sensor. E.g., EDR, vulnerability management, APM, backup & recovery, etc.

        OCSF Attribute: type_id
        """

        ENDPOINT_DETECTION_AND_RESPONSE = 1
        DATA_LOSS_PREVENTION = 2
        BACKUP_RECOVERY = 3
        PERFORMANCE_MONITORING_OBSERVABILITY = 4
        VULNERABILITY_MANAGEMENT = 5
        LOG_FORWARDING = 6
        MOBILE_DEVICE_MANAGEMENT = 7
        CONFIGURATION_MANAGEMENT = 8
        REMOTE_ACCESS = 9

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "Endpoint Detection and Response",
                2: "Data Loss Prevention",
                3: "Backup & Recovery",
                4: "Performance Monitoring & Observability",
                5: "Vulnerability Management",
                6: "Log Forwarding",
                7: "Mobile Device Management",
                8: "Configuration Management",
                9: "Remote Access",
            }

    name: str | None = Field(
        default=None,
        description="The name of the agent or sensor. For example: <code>AWS SSM Agent</code>. [Recommended]",
    )
    policies: list[Policy] | None = Field(
        default=None,
        description="Describes the various policies that may be applied or enforced by an agent or sensor. E.g., Conditional Access, prevention, auto-update, tamper protection, destination configuration, etc.",
    )
    type_: str | None = Field(
        default=None,
        description="The normalized caption of the type_id value for the agent or sensor. In the case of 'Other' or 'Unknown', it is defined by the event source.",
    )
    type_id: TypeId | None = Field(
        default=None,
        description="The normalized representation of an agent or sensor. E.g., EDR, vulnerability management, APM, backup & recovery, etc. [Recommended]",
    )
    uid: str | None = Field(
        default=None,
        description="The UID of the agent or sensor, sometimes known as a Sensor ID or <code>aid</code>. [Recommended]",
    )
    uid_alt: str | None = Field(
        default=None,
        description="An alternative or contextual identifier for the agent or sensor, such as a configuration, organization, or license UID.",
    )
    vendor_name: str | None = Field(
        default=None,
        description="The company or author who created the agent or sensor. For example: <code>Crowdstrike</code>.",
    )
    version: str | None = Field(
        default=None,
        description="The semantic version of the agent or sensor, e.g., <code>7.101.50.0</code>.",
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
