"""Application object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.graph import Graph
    from ocsf.v1_6_0.objects.group import Group
    from ocsf.v1_6_0.objects.key_value_object import KeyValueObject
    from ocsf.v1_6_0.objects.sbom import Sbom
    from ocsf.v1_6_0.objects.url import Url
    from ocsf.v1_6_0.objects.user import User


class Application(OCSFBaseModel):
    """An Application describes the details for an inventoried application as reported by an Application Security tool or other Developer-centric tooling. Applications can be defined as Kubernetes resources, Containerized resources, or application hosting-specific cloud sources such as AWS Elastic BeanStalk, AWS Lightsail, or Azure Logic Apps.

    See: https://schema.ocsf.io/1.6.0/objects/application
    """

    # Nested Enums for sibling attribute pairs
    class RiskLevelId(SiblingEnum):
        """The normalized risk level id.

        OCSF Attribute: risk_level_id
        """

        INFO = 0
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        CRITICAL = 4
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Info",
                1: "Low",
                2: "Medium",
                3: "High",
                4: "Critical",
                99: "Other",
            }

    criticality: str | None = Field(
        default=None,
        description="The criticality of the application as defined by the event source.",
    )
    data: dict[str, Any] | None = Field(
        default=None, description="Additional data describing the application."
    )
    desc: str | None = Field(
        default=None,
        description="A description or commentary for an application, usually retrieved from an upstream system.",
    )
    group: Group | None = Field(
        default=None,
        description="The name of the related application or associated resource group.",
    )
    hostname: Any | None = Field(
        default=None, description="The fully qualified name of the application."
    )
    labels: list[str] | None = Field(
        default=None, description="The list of labels associated to the application."
    )
    name: str | None = Field(default=None, description="The name of the application. [Recommended]")
    owner: User | None = Field(
        default=None,
        description="The identity of the service or user account that owns the application. [Recommended]",
    )
    region: str | None = Field(default=None, description="The cloud region of the resource.")
    resource_relationship: Graph | None = Field(
        default=None,
        description="A graph representation showing how this application relates to and interacts with other entities in the environment. This can include parent/child relationships, dependencies, or other connections.",
    )
    risk_level: str | None = Field(
        default=None,
        description="The risk level, normalized to the caption of the risk_level_id value.",
    )
    risk_level_id: RiskLevelId | None = Field(
        default=None, description="The normalized risk level id."
    )
    risk_score: int | None = Field(
        default=None, description="The risk score as reported by the event source."
    )
    sbom: Sbom | None = Field(
        default=None,
        description="The Software Bill of Materials (SBOM) associated with the application",
    )
    tags: list[KeyValueObject] | None = Field(
        default=None,
        description="The list of tags; <code>{key:value}</code> pairs associated to the application.",
    )
    type_: str | None = Field(
        default=None,
        description="The type of application as defined by the event source, e.g., <code>GitHub</code>, <code>Azure Logic App</code>, or <code>Amazon Elastic BeanStalk</code>.",
    )
    uid: str | None = Field(
        default=None, description="The unique identifier for the application. [Recommended]"
    )
    uid_alt: str | None = Field(
        default=None,
        description="An alternative or contextual identifier for the application, such as a configuration, organization, or license UID.",
    )
    url: Url | None = Field(default=None, description="The URL of the application.")
    version: str | None = Field(
        default=None,
        description="The semantic version of the application, e.g., <code>1.7.4</code>.",
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
            ("risk_level_id", "risk_level", cls.RiskLevelId),
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
