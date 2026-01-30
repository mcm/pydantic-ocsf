"""Startup Item object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_7_0.enums.startup_item_run_mode_ids import StartupItemRunModeIds
    from ocsf.v1_7_0.objects.job import Job
    from ocsf.v1_7_0.objects.kernel_driver import KernelDriver
    from ocsf.v1_7_0.objects.process import Process


class StartupItem(OCSFBaseModel):
    """The startup item object describes an application component that has associated startup criteria and configurations.

    See: https://schema.ocsf.io/1.7.0/objects/startup_item
    """

    # Nested Enums for sibling attribute pairs
    class RunStateId(SiblingEnum):
        """The run state ID of the startup item.

        OCSF Attribute: run_state_id
        """

        STOPPED = 1
        START_PENDING = 2
        STOP_PENDING = 3
        RUNNING = 4
        CONTINUE_PENDING = 5
        PAUSE_PENDING = 6
        PAUSED = 7
        RESTART_PENDING = 8

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "Stopped",
                2: "Start Pending",
                3: "Stop Pending",
                4: "Running",
                5: "Continue Pending",
                6: "Pause Pending",
                7: "Paused",
                8: "Restart Pending",
            }

    class StartTypeId(SiblingEnum):
        """The start type ID of the startup item.

        OCSF Attribute: start_type_id
        """

        UNKNOWN = 0
        AUTO = 1
        BOOT = 2
        ON_DEMAND = 3
        DISABLED = 4
        ALL_LOGINS = 5
        SPECIFIC_USER_LOGIN = 6
        SCHEDULED = 7
        SYSTEM_CHANGED = 8
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Auto",
                2: "Boot",
                3: "On Demand",
                4: "Disabled",
                5: "All Logins",
                6: "Specific User Login",
                7: "Scheduled",
                8: "System Changed",
                99: "Other",
            }

    class TypeId(SiblingEnum):
        """The startup item type identifier.

        OCSF Attribute: type_id
        """

        UNKNOWN = 0
        KERNEL_MODE_DRIVER = 1
        USER_MODE_DRIVER = 2
        SERVICE = 3
        USER_MODE_APPLICATION = 4
        AUTOLOAD = 5
        SYSTEM_EXTENSION = 6
        KERNEL_EXTENSION = 7
        SCHEDULED_JOB_TASK = 8
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Kernel Mode Driver",
                2: "User Mode Driver",
                3: "Service",
                4: "User Mode Application",
                5: "Autoload",
                6: "System Extension",
                7: "Kernel Extension",
                8: "Scheduled Job, Task",
                99: "Other",
            }

    name: str = Field(..., description="The unique name of the startup item.")
    start_type_id: StartTypeId = Field(..., description="The start type ID of the startup item.")
    driver: KernelDriver | None = Field(
        default=None, description="The startup item kernel driver resource."
    )
    job: Job | None = Field(default=None, description="The startup item job resource.")
    process: Process | None = Field(default=None, description="The startup item process resource.")
    run_mode_ids: list[StartupItemRunModeIds] | None = Field(
        default=None,
        description="The list of normalized identifiers that describe the startup items' properties when it is running.  Use this field to capture extended information about the process, which may depend on the type of startup item.  E.g., A Windows service that interacts with the desktop.",
    )
    run_modes: list[str] | None = Field(
        default=None,
        description="The list of run_modes, normalized to the captions of the run_mode_id values.  In the case of 'Other', they are defined by the event source.",
    )
    run_state: str | None = Field(default=None, description="The run state of the startup item.")
    run_state_id: RunStateId | None = Field(
        default=None, description="The run state ID of the startup item. [Recommended]"
    )
    start_type: str | None = Field(default=None, description="The start type of the startup item.")
    type_: str | None = Field(default=None, description="The startup item type.")
    type_id: TypeId | None = Field(
        default=None, description="The startup item type identifier. [Recommended]"
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
            ("run_state_id", "run_state", cls.RunStateId),
            ("start_type_id", "start_type", cls.StartTypeId),
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
