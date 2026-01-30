"""Related Event/Finding object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.attack import Attack
    from ocsf.v1_6_0.objects.key_value_object import KeyValueObject
    from ocsf.v1_6_0.objects.kill_chain_phase import KillChainPhase
    from ocsf.v1_6_0.objects.observable import Observable
    from ocsf.v1_6_0.objects.product import Product
    from ocsf.v1_6_0.objects.trait import Trait


class RelatedEvent(OCSFBaseModel):
    """The Related Event object describes an event or another finding related to a finding. It may or may not be an OCSF event.

    See: https://schema.ocsf.io/1.6.0/objects/related_event
    """

    # Nested Enums for sibling attribute pairs
    class SeverityId(SiblingEnum):
        """<p>The normalized identifier of the event/finding severity.</p>The normalized severity is a measurement the effort and expense required to manage and resolve an event or incident. Smaller numerical values represent lower impact events, and larger numerical values represent higher impact events.

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

    uid: str = Field(
        ...,
        description="The unique identifier of the related event/finding.</p> If the related event/finding is in OCSF, then this value must be equal to <code>metadata.uid</code> in the corresponding event.",
    )
    attacks: list[Attack] | None = Field(
        default=None,
        description="An array of MITRE ATT&CK® objects describing identified tactics, techniques & sub-techniques. The objects are compatible with MITRE ATLAS™ tactics, techniques & sub-techniques.",
    )
    count: int | None = Field(
        default=None,
        description="The number of times that activity in the same logical group occurred, as reported by the related Finding.",
    )
    created_time: int | None = Field(
        default=None, description="The time when the related event/finding was created."
    )
    desc: str | None = Field(
        default=None, description="A description of the related event/finding."
    )
    first_seen_time: int | None = Field(
        default=None,
        description="The time when the finding was first observed. e.g. The time when a vulnerability was first observed.<br>It can differ from the <code>created_time</code> timestamp, which reflects the time this finding was created.",
    )
    kill_chain: list[KillChainPhase] | None = Field(
        default=None,
        description="The <a target='_blank' href='https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html'>Cyber Kill Chain®</a> provides a detailed description of each phase and its associated activities within the broader context of a cyber attack.",
    )
    last_seen_time: int | None = Field(
        default=None,
        description="The time when the finding was most recently observed. e.g. The time when a vulnerability was most recently observed.<br>It can differ from the <code>modified_time</code> timestamp, which reflects the time this finding was last modified.",
    )
    modified_time: int | None = Field(
        default=None, description="The time when the related event/finding was last modified."
    )
    observables: list[Observable] | None = Field(
        default=None, description="The observables associated with the event or a finding."
    )
    product: Product | None = Field(
        default=None,
        description="Details about the product that reported the related event/finding.",
    )
    product_uid: str | None = Field(
        default=None,
        description="The unique identifier of the product that reported the related event.",
    )
    severity: str | None = Field(
        default=None,
        description="The event/finding severity, normalized to the caption of the <code>severity_id</code> value. In the case of 'Other', it is defined by the source.",
    )
    severity_id: SeverityId | None = Field(
        default=None,
        description="<p>The normalized identifier of the event/finding severity.</p>The normalized severity is a measurement the effort and expense required to manage and resolve an event or incident. Smaller numerical values represent lower impact events, and larger numerical values represent higher impact events. [Recommended]",
    )
    status: str | None = Field(
        default=None,
        description="The related event status. Should correspond to the label of the status_id (or 'Other' status value for status_id = 99) of the related event.",
    )
    tags: list[KeyValueObject] | None = Field(
        default=None,
        description="The list of tags; <code>{key:value}</code> pairs associated with the related event/finding.",
    )
    title: str | None = Field(
        default=None, description="A title or a brief phrase summarizing the related event/finding."
    )
    traits: list[Trait] | None = Field(
        default=None,
        description="The list of key traits or characteristics extracted from the related event/finding that influenced or contributed to the overall finding's outcome.",
    )
    type_: str | None = Field(
        default=None,
        description="The type of the related event/finding.</p>Populate if the related event/finding is <code>NOT</code> in OCSF. If it is in OCSF, then utilize <code>type_name, type_uid</code> instead.",
    )
    type_name: str | None = Field(
        default=None,
        description="The type of the related OCSF event, as defined by <code>type_uid</code>.<p>For example: <code>Process Activity: Launch.</code></p>Populate if the related event/finding is in OCSF.",
    )
    type_uid: int | None = Field(
        default=None,
        description="The unique identifier of the related OCSF event type. <p>For example: <code>100701.</code></p>Populate if the related event/finding is in OCSF. [Recommended]",
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
            ("severity_id", "severity", cls.SeverityId),
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
