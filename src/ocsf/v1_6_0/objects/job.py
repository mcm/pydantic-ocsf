"""Job object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_6_0.objects.file import File
    from ocsf.v1_6_0.objects.user import User


class Job(OCSFBaseModel):
    """The Job object provides information about a scheduled job or task, including its name, command line, and state. It encompasses attributes that describe the properties and status of the scheduled job.

    See: https://schema.ocsf.io/1.6.0/objects/job
    """

    # Nested Enums for sibling attribute pairs
    class RunStateId(SiblingEnum):
        """The run state ID of the job.

        OCSF Attribute: run_state_id
        """

        UNKNOWN = 0
        READY = 1
        QUEUED = 2
        RUNNING = 3
        STOPPED = 4
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Ready",
                2: "Queued",
                3: "Running",
                4: "Stopped",
                99: "Other",
            }

    file: File = Field(..., description="The file that pertains to the job.")
    name: str = Field(..., description="The name of the job.")
    cmd_line: str | None = Field(default=None, description="The job command line. [Recommended]")
    created_time: int | None = Field(
        default=None, description="The time when the job was created. [Recommended]"
    )
    desc: str | None = Field(default=None, description="The description of the job. [Recommended]")
    last_run_time: int | None = Field(
        default=None, description="The time when the job was last run. [Recommended]"
    )
    next_run_time: int | None = Field(
        default=None, description="The time when the job will next be run."
    )
    run_state: str | None = Field(default=None, description="The run state of the job.")
    run_state_id: RunStateId | None = Field(
        default=None, description="The run state ID of the job. [Recommended]"
    )
    user: User | None = Field(default=None, description="The user that created the job.")

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
            ("run_state_id", "run_state", cls.RunStateId),
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
