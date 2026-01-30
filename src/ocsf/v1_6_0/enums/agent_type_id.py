"""The normalized representation of an agent or sensor. E.g., EDR, vulnerability management, APM, backup & recovery, etc. enumeration."""

from enum import IntEnum


class AgentTypeId(IntEnum):
    """The normalized representation of an agent or sensor. E.g., EDR, vulnerability management, APM, backup & recovery, etc.

    See: https://schema.ocsf.io/1.6.0/data_types/agent_type_id
    """

    ENDPOINT_DETECTION_AND_RESPONSE = 1  # Any EDR sensor or agent. Or any tool that provides similar threat detection, anti-malware, anti-ransomware, or similar capabilities. E.g., Crowdstrike Falcon, Microsoft Defender for Endpoint, Wazuh.
    DATA_LOSS_PREVENTION = 2  # Any DLP sensor or agent. Or any tool that provides similar data classification, data loss detection, and/or data loss prevention capabilities. E.g., Forcepoint DLP, Microsoft Purview, Symantec DLP.
    BACKUP___RECOVERY = 3  # Any agent or sensor that provides backups, archival, or recovery capabilities. E.g., Azure Backup, AWS Backint Agent.
    PERFORMANCE_MONITORING___OBSERVABILITY = 4  # Any agent or sensor that provides Application Performance Monitoring (APM), active tracing, profiling, or other observability use cases and optionally forwards the logs. E.g., New Relic Agent, Datadog Agent, Azure Monitor Agent.
    VULNERABILITY_MANAGEMENT = 5  # Any agent or sensor that provides vulnerability management or scanning capabilities. E.g., Qualys VMDR, Microsoft Defender for Endpoint, Crowdstrike Spotlight, Amazon Inspector Agent.
    LOG_FORWARDING = 6  # Any agent or sensor that forwards logs to a 3rd party storage system such as a data lake or SIEM. E.g., Splunk Universal Forwarder, Tenzir, FluentBit, Amazon CloudWatch Agent, Amazon Kinesis Agent.
    MOBILE_DEVICE_MANAGEMENT = 7  # Any agent or sensor responsible for providing Mobile Device Management (MDM) or Mobile Enterprise Management (MEM) capabilities. E.g., JumpCloud Agent, Esper Agent, Jamf Pro binary.
    CONFIGURATION_MANAGEMENT = 8  # Any agent or sensor that provides configuration management of a device, such as scanning for software, license management, or applying configurations. E.g., AWS Systems Manager Agent, Flexera, ServiceNow MID Server.
    REMOTE_ACCESS = 9  # Any agent or sensor that provides remote access capabilities to a device. E.g., BeyondTrust, Amazon Systems Manager Agent, Verkada Agent.
