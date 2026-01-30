"""Process object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_0_0.objects.file import File
    from ocsf.v1_0_0.objects.object import Object
    from ocsf.v1_0_0.objects.session import Session
    from ocsf.v1_0_0.objects.user import User


class Process(OCSFBaseModel):
    """The Process object describes a running instance of a launched program. Defined by D3FEND <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:Process/'>d3f:Process</a>.

    See: https://schema.ocsf.io/1.0.0/objects/process
    """

    # Nested Enums for sibling attribute pairs
    class IntegrityId(SiblingEnum):
        """The normalized identifier of the process integrity level (Windows only).

        OCSF Attribute: integrity_id
        """

        UNKNOWN = 0
        UNTRUSTED = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4
        SYSTEM = 5
        PROTECTED = 6
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Untrusted",
                2: "Low",
                3: "Medium",
                4: "High",
                5: "System",
                6: "Protected",
                99: "Other",
            }

    cmd_line: str | None = Field(
        default=None,
        description="The full command line used to launch an application, service, process, or job. For example: <code>ssh user@10.0.0.10</code>. If the command line is unavailable or missing, the empty string <code>''</code> is to be used [Recommended]",
    )
    created_time: int | None = Field(
        default=None, description="The time when the process was created/started. [Recommended]"
    )
    file: File | None = Field(default=None, description="The process file object. [Recommended]")
    include: str | None = Field(default=None, description="")
    integrity: str | None = Field(
        default=None,
        description="The process integrity level, normalized to the caption of the direction_id value. In the case of 'Other', it is defined by the event source (Windows only).",
    )
    integrity_id: IntegrityId | None = Field(
        default=None,
        description="The normalized identifier of the process integrity level (Windows only).",
    )
    lineage: list[str] | None = Field(
        default=None,
        description="The lineage of the process, represented by a list of paths for each ancestor process. For example: <code>['/usr/sbin/sshd', '/usr/bin/bash', '/usr/bin/whoami']</code>",
    )
    loaded_modules: list[str] | None = Field(
        default=None, description="The list of loaded module names."
    )
    name: Any | None = Field(
        default=None,
        description="The friendly name of the process, for example: <code>Notepad++</code>.",
    )
    parent_process: Process | None = Field(
        default=None,
        description="The parent process of this process object. It is recommended to only populate this field for the first process object, to prevent deep nesting. [Recommended]",
    )
    pid: int | None = Field(
        default=None,
        description="The process identifier, as reported by the operating system. Process ID (PID) is a number used by the operating system to uniquely identify an active process. [Recommended]",
    )
    sandbox: str | None = Field(
        default=None,
        description="The name of the containment jail (i.e., sandbox). For example, hardened_ps, high_security_ps, oracle_ps, netsvcs_ps, or default_ps.",
    )
    session: Session | None = Field(
        default=None, description="The user session under which this process is running."
    )
    terminated_time: int | None = Field(
        default=None, description="The time when the process was terminated."
    )
    tid: int | None = Field(
        default=None,
        description="The Identifier of the thread associated with the event, as returned by the operating system.",
    )
    uid: str | None = Field(
        default=None,
        description="A unique identifier for this process assigned by the producer (tool).  Facilitates correlation of a process event with other events for that process.",
    )
    user: User | None = Field(
        default=None, description="The user under which this process is running. [Recommended]"
    )
    xattributes: Object | None = Field(
        default=None,
        description="An unordered collection of zero or more name/value pairs that represent a process extended attribute.",
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
            ("integrity_id", "integrity", cls.IntegrityId),
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
