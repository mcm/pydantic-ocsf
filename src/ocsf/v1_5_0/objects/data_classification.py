"""Data Classification object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_5_0.objects.classifier_details import ClassifierDetails
    from ocsf.v1_5_0.objects.discovery_details import DiscoveryDetails
    from ocsf.v1_5_0.objects.policy import Policy


class DataClassification(OCSFBaseModel):
    """The Data Classification object includes information about data classification levels and data category types.

    See: https://schema.ocsf.io/1.5.0/objects/data_classification
    """

    # Nested Enums for sibling attribute pairs
    class CategoryId(SiblingEnum):
        """The normalized identifier of the data classification category.

        OCSF Attribute: category_id
        """

        UNKNOWN = 0
        PERSONAL = 1
        GOVERNMENTAL = 2
        FINANCIAL = 3
        BUSINESS = 4
        MILITARY_AND_LAW_ENFORCEMENT = 5
        SECURITY = 6
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Personal",
                2: "Governmental",
                3: "Financial",
                4: "Business",
                5: "Military and Law Enforcement",
                6: "Security",
                99: "Other",
            }

    class ConfidentialityId(SiblingEnum):
        """The normalized identifier of the file content confidentiality indicator.

        OCSF Attribute: confidentiality_id
        """

        UNKNOWN = 0
        NOT_CONFIDENTIAL = 1
        CONFIDENTIAL = 2
        SECRET = 3
        TOP_SECRET = 4
        PRIVATE = 5
        RESTRICTED = 6
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Not Confidential",
                2: "Confidential",
                3: "Secret",
                4: "Top Secret",
                5: "Private",
                6: "Restricted",
                99: "Other",
            }

    class StatusId(SiblingEnum):
        """The normalized status identifier of the classification job.

        OCSF Attribute: status_id
        """

        UNKNOWN = 0
        COMPLETE = 1
        PARTIAL = 2
        FAIL = 3
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Complete",
                2: "Partial",
                3: "Fail",
                99: "Other",
            }

    category: str | None = Field(
        default=None,
        description="The name of the data classification category that data matched into, e.g. Financial, Personal, Governmental, etc.",
    )
    category_id: CategoryId | None = Field(
        default=None,
        description="The normalized identifier of the data classification category. [Recommended]",
    )
    classifier_details: ClassifierDetails | None = Field(
        default=None,
        description="Describes details about the classifier used for data classification. [Recommended]",
    )
    confidentiality: str | None = Field(
        default=None,
        description="The file content confidentiality, normalized to the confidentiality_id value. In the case of 'Other', it is defined by the event source.",
    )
    confidentiality_id: ConfidentialityId | None = Field(
        default=None,
        description="The normalized identifier of the file content confidentiality indicator. [Recommended]",
    )
    discovery_details: list[DiscoveryDetails] | None = Field(
        default=None, description="Details about the data discovered by classification job."
    )
    policy: Policy | None = Field(
        default=None,
        description="Details about the data policy that governs data handling and security measures related to classification.",
    )
    size: int | None = Field(default=None, description="Size of the data classified.")
    src_url: Any | None = Field(
        default=None,
        description="The source URL pointing towards the full classifcation job details.",
    )
    status: str | None = Field(
        default=None,
        description="The resultant status of the classification job normalized to the caption of the <code>status_id</code> value. In the case of 'Other', it is defined by the event source. [Recommended]",
    )
    status_details: list[str] | None = Field(
        default=None,
        description="The contextual description of the <code>status, status_id</code> value.",
    )
    status_id: StatusId | None = Field(
        default=None,
        description="The normalized status identifier of the classification job. [Recommended]",
    )
    total: int | None = Field(
        default=None,
        description="The total count of discovered entities, by the classification job.",
    )
    uid: str | None = Field(
        default=None, description="The unique identifier of the classification job."
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
            ("category_id", "category", cls.CategoryId),
            ("confidentiality_id", "confidentiality", cls.ConfidentialityId),
            ("status_id", "status", cls.StatusId),
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
