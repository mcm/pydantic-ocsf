from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.objects.object import Object


class StateId(Enum):
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
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return StateId[obj]
        else:
            return StateId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "MISSING_OR_OUTDATED_CONTENT": "Missing or outdated content",
            "POLICY_MISMATCH": "Policy mismatch",
            "IN_NETWORK_QUARANTINE": "In network quarantine",
            "PROTECTION_OFF": "Protection off",
            "PROTECTION_MALFUNCTION": "Protection malfunction",
            "PROTECTION_NOT_LICENSED": "Protection not licensed",
            "UNREMEDIATED_THREAT": "Unremediated threat",
            "SUSPICIOUS_REPUTATION": "Suspicious reputation",
            "REBOOT_PENDING": "Reboot pending",
            "CONTENT_IS_LOCKED": "Content is locked",
            "NOT_INSTALLED": "Not installed",
            "WRITABLE_SYSTEM_PARTITION": "Writable system partition",
            "SAFETYNET_FAILURE": "SafetyNet failure",
            "FAILED_BOOT_VERIFY": "Failed boot verify",
            "MODIFIED_EXECUTION_ENVIRONMENT": "Modified execution environment",
            "SELINUX_DISABLED": "SELinux disabled",
            "ELEVATED_PRIVILEGE_SHELL": "Elevated privilege shell",
            "IOS_FILE_SYSTEM_ALTERED": "iOS file system altered",
            "OPEN_REMOTE_ACCESS": "Open remote access",
            "OTA_UPDATES_DISABLED": "OTA updates disabled",
            "ROOTED": "Rooted",
            "ANDROID_PARTITION_MODIFIED": "Android partition modified",
            "COMPLIANCE_FAILURE": "Compliance failure",
            "OTHER": "Other",
        }
        return name_map[super().name]


class SecurityState(Object):
    schema_name: ClassVar[str] = "security_state"

    # Recommended
    state_id: StateId | None = None

    # Optional
    state: str | None = None
