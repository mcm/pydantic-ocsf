"""Databucket object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_5_0.objects.agent import Agent
    from ocsf.v1_5_0.objects.encryption_details import EncryptionDetails
    from ocsf.v1_5_0.objects.file import File
    from ocsf.v1_5_0.objects.graph import Graph
    from ocsf.v1_5_0.objects.group import Group
    from ocsf.v1_5_0.objects.key_value_object import KeyValueObject
    from ocsf.v1_5_0.objects.user import User


class Databucket(OCSFBaseModel):
    """The databucket object is a basic container that holds data, typically organized through the use of data partitions.

    See: https://schema.ocsf.io/1.5.0/objects/databucket
    """

    # Nested Enums for sibling attribute pairs
    class TypeId(SiblingEnum):
        """The normalized identifier of the databucket type.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        S3 = 1
        AZURE_BLOB = 2
        GCP_BUCKET = 3
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "S3",
                2: "Azure Blob",
                3: "GCP Bucket",
                99: "Other",
            }

    type_id: TypeId = Field(..., description="The normalized identifier of the databucket type.")
    agent_list: list[Agent] | None = Field(
        default=None,
        description="A list of <code>agent</code> objects associated with a device, endpoint, or resource.",
    )
    cloud_partition: str | None = Field(
        default=None,
        description="The canonical cloud partition name to which the region is assigned (e.g. AWS Partitions: aws, aws-cn, aws-us-gov).",
    )
    created_time: int | None = Field(
        default=None, description="The time when the databucket was known to have been created."
    )
    criticality: str | None = Field(
        default=None, description="The criticality of the resource as defined by the event source."
    )
    data: dict[str, Any] | None = Field(
        default=None, description="Additional data describing the resource."
    )
    desc: str | None = Field(default=None, description="The description of the databucket.")
    encryption_details: EncryptionDetails | None = Field(
        default=None,
        description="The encryption details of the databucket. Should be populated if the databucket is encrypted.",
    )
    file: File | None = Field(
        default=None, description="Details about the file/object within a databucket."
    )
    group: Group | None = Field(default=None, description="The name of the related resource group.")
    groups: list[Group] | None = Field(
        default=None, description="The group names to which the databucket belongs."
    )
    hostname: Any | None = Field(
        default=None, description="The fully qualified name of the resource. [Recommended]"
    )
    include: str | None = Field(default=None, description="")
    ip: Any | None = Field(
        default=None,
        description="The IP address of the resource, in either IPv4 or IPv6 format. [Recommended]",
    )
    is_backed_up: bool | None = Field(
        default=None,
        description="Indicates whether the device or resource has a backup enabled, such as an automated snapshot or a cloud backup. For example, this is indicated by the <code>cloudBackupEnabled</code> value within JAMF Pro mobile devices or the registration of an AWS ARN with the AWS Backup service.",
    )
    is_encrypted: bool | None = Field(
        default=None, description="Indicates if the databucket is encrypted."
    )
    is_public: bool | None = Field(
        default=None,
        description="Indicates if the databucket is publicly accessible. [Recommended]",
    )
    labels: list[str] | None = Field(
        default=None, description="The list of labels associated to the resource."
    )
    modified_time: int | None = Field(
        default=None,
        description="The most recent time when any changes, updates, or modifications were made within the databucket.",
    )
    name: str | None = Field(default=None, description="The databucket name.")
    namespace: str | None = Field(
        default=None,
        description="The namespace is useful when similar entities exist that you need to keep separate.",
    )
    owner: User | None = Field(
        default=None,
        description="The identity of the service or user account that owns the resource. [Recommended]",
    )
    region: str | None = Field(default=None, description="The cloud region of the resource.")
    resource_relationship: Graph | None = Field(
        default=None,
        description="A graph representation showing how this resource relates to and interacts with other entities in the environment. This can include parent/child relationships, dependencies, or other connections.",
    )
    size: int | None = Field(default=None, description="The size of the databucket in bytes.")
    tags: list[KeyValueObject] | None = Field(
        default=None,
        description="The list of tags; <code>{key:value}</code> pairs associated to the resource.",
    )
    type_: str | None = Field(default=None, description="The databucket type. [Recommended]")
    uid: str | None = Field(default=None, description="The unique identifier of the databucket.")
    uid_alt: Any | None = Field(
        default=None, description="The alternative unique identifier of the resource."
    )
    version: str | None = Field(
        default=None, description="The version of the resource. For example <code>1.2.3</code>."
    )
    zone: str | None = Field(
        default=None,
        description="The specific availability zone within a cloud region where the resource is located.",
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
