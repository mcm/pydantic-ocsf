"""The security state of the managed entity. enumeration."""

from enum import IntEnum


class SecurityStateStateId(IntEnum):
    """The security state of the managed entity.

    See: https://schema.ocsf.io/1.7.0/data_types/security_state_state_id
    """

    UNKNOWN = 0  # The security state is unknown.
    MISSING_OR_OUTDATED_CONTENT = 1  # The content is missing or outdated.
    POLICY_MISMATCH = 2  # Not in compliance with the expected security policy.
    IN_NETWORK_QUARANTINE = 3  # Isolated from the network.
    PROTECTION_OFF = 4  # Not protected by a security solution.
    PROTECTION_MALFUNCTION = 5  # The security solution is not functioning properly.
    PROTECTION_NOT_LICENSED = 6  # The security solution does not have a valid license.
    UNREMEDIATED_THREAT = 7  # A detected threat has not been remediated.
    SUSPICIOUS_REPUTATION = 8  # Reputation of the entity is suspicious.
    REBOOT_PENDING = 9  # A reboot is required for one or more pending actions.
    CONTENT_IS_LOCKED = 10  # The content is locked to a specific version.
    NOT_INSTALLED = 11  # The entity is not installed.
    WRITABLE_SYSTEM_PARTITION = 12  # The system partition is writeable.
    SAFETYNET_FAILURE = 13  # The device has failed the SafetyNet check.
    FAILED_BOOT_VERIFY = 14  # The device has failed the boot verification process.
    MODIFIED_EXECUTION_ENVIRONMENT = 15  # The execution environment has been modified.
    SELINUX_DISABLED = 16  # The SELinux security feature has been disabled.
    ELEVATED_PRIVILEGE_SHELL = 17  # An elevated privilege shell has been detected.
    IOS_FILE_SYSTEM_ALTERED = 18  # The file system has been altered on an iOS device.
    OPEN_REMOTE_ACCESS = 19  # Remote access is enabled.
    OTA_UPDATES_DISABLED = 20  # Mobile OTA (Over The Air) updates have been disabled.
    ROOTED = 21  # The device has been modified to allow root access.
    ANDROID_PARTITION_MODIFIED = 22  # The Android partition has been modified.
    COMPLIANCE_FAILURE = 23  # The entity is not compliant with the associated security policy.
    OTHER = 99  # The security state is not mapped. See the <code>state</code> attribute, which contains data source specific values.
