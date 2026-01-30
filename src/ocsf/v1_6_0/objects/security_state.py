"""Security State object."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum


class SecurityState(OCSFBaseModel):
    """The Security State object describes the security related state of a managed entity.

    See: https://schema.ocsf.io/1.6.0/objects/security_state
    """

    # Nested Enums for sibling attribute pairs
    class StateId(SiblingEnum):
        """The security state of the managed entity.

        OCSF Attribute: state_id
        """

        UNKNOWN = 0
        MISSING_OR_OUTDATED_CONTENT = 1
        POLICY_MISMATCH = 2
        IN_NETWORK_QUARANTINE = 3
        PROTECTION_OFF = 4
        PROTECTION_MALFUNCTION = 5
        PROTECTION_NOT_LICENSED = 6
        UNREMEDIATED_THREAT = 7
        SUSPICIOUS_REPUTATION = 8
        REBOOT_PENDING = 9
        CONTENT_IS_LOCKED = 10
        NOT_INSTALLED = 11
        WRITABLE_SYSTEM_PARTITION = 12
        SAFETYNET_FAILURE = 13
        FAILED_BOOT_VERIFY = 14
        MODIFIED_EXECUTION_ENVIRONMENT = 15
        SELINUX_DISABLED = 16
        ELEVATED_PRIVILEGE_SHELL = 17
        IOS_FILE_SYSTEM_ALTERED = 18
        OPEN_REMOTE_ACCESS = 19
        OTA_UPDATES_DISABLED = 20
        ROOTED = 21
        ANDROID_PARTITION_MODIFIED = 22
        COMPLIANCE_FAILURE = 23
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Missing or outdated content",
                2: "Policy mismatch",
                3: "In network quarantine",
                4: "Protection off",
                5: "Protection malfunction",
                6: "Protection not licensed",
                7: "Unremediated threat",
                8: "Suspicious reputation",
                9: "Reboot pending",
                10: "Content is locked",
                11: "Not installed",
                12: "Writable system partition",
                13: "SafetyNet failure",
                14: "Failed boot verify",
                15: "Modified execution environment",
                16: "SELinux disabled",
                17: "Elevated privilege shell",
                18: "iOS file system altered",
                19: "Open remote access",
                20: "OTA updates disabled",
                21: "Rooted",
                22: "Android partition modified",
                23: "Compliance failure",
                99: "Other",
            }

    state: str | None = Field(
        default=None,
        description="The security state, normalized to the caption of the state_id value. In the case of 'Other', it is defined by the source.",
    )
    state_id: StateId | None = Field(
        default=None, description="The security state of the managed entity. [Recommended]"
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
            ("state_id", "state", cls.StateId),
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
