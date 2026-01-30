"""OCSF v1.2.0 enumerations."""

from ocsf.v1_2_0.enums.account_change_activity_id import AccountChangeActivityId
from ocsf.v1_2_0.enums.account_change_severity_id import AccountChangeSeverityId
from ocsf.v1_2_0.enums.account_change_status_id import AccountChangeStatusId
from ocsf.v1_2_0.enums.account_type_id import AccountTypeId
from ocsf.v1_2_0.enums.admin_group_query_activity_id import AdminGroupQueryActivityId
from ocsf.v1_2_0.enums.admin_group_query_query_result_id import AdminGroupQueryQueryResultId
from ocsf.v1_2_0.enums.admin_group_query_severity_id import AdminGroupQuerySeverityId
from ocsf.v1_2_0.enums.admin_group_query_status_id import AdminGroupQueryStatusId
from ocsf.v1_2_0.enums.agent_type_id import AgentTypeId
from ocsf.v1_2_0.enums.analytic_type_id import AnalyticTypeId
from ocsf.v1_2_0.enums.api_activity_activity_id import ApiActivityActivityId
from ocsf.v1_2_0.enums.api_activity_severity_id import ApiActivitySeverityId
from ocsf.v1_2_0.enums.api_activity_status_id import ApiActivityStatusId
from ocsf.v1_2_0.enums.application_lifecycle_activity_id import ApplicationLifecycleActivityId
from ocsf.v1_2_0.enums.application_lifecycle_severity_id import ApplicationLifecycleSeverityId
from ocsf.v1_2_0.enums.application_lifecycle_status_id import ApplicationLifecycleStatusId
from ocsf.v1_2_0.enums.application_severity_id import ApplicationSeverityId
from ocsf.v1_2_0.enums.application_status_id import ApplicationStatusId
from ocsf.v1_2_0.enums.auth_factor_factor_type_id import AuthFactorFactorTypeId
from ocsf.v1_2_0.enums.authentication_activity_id import AuthenticationActivityId
from ocsf.v1_2_0.enums.authentication_auth_protocol_id import AuthenticationAuthProtocolId
from ocsf.v1_2_0.enums.authentication_logon_type_id import AuthenticationLogonTypeId
from ocsf.v1_2_0.enums.authentication_severity_id import AuthenticationSeverityId
from ocsf.v1_2_0.enums.authentication_status_id import AuthenticationStatusId
from ocsf.v1_2_0.enums.authorize_session_activity_id import AuthorizeSessionActivityId
from ocsf.v1_2_0.enums.authorize_session_severity_id import AuthorizeSessionSeverityId
from ocsf.v1_2_0.enums.authorize_session_status_id import AuthorizeSessionStatusId
from ocsf.v1_2_0.enums.base_event_severity_id import BaseEventSeverityId
from ocsf.v1_2_0.enums.base_event_status_id import BaseEventStatusId
from ocsf.v1_2_0.enums.compliance_finding_activity_id import ComplianceFindingActivityId
from ocsf.v1_2_0.enums.compliance_finding_confidence_id import ComplianceFindingConfidenceId
from ocsf.v1_2_0.enums.compliance_finding_severity_id import ComplianceFindingSeverityId
from ocsf.v1_2_0.enums.compliance_finding_status_id import ComplianceFindingStatusId
from ocsf.v1_2_0.enums.compliance_status_id import ComplianceStatusId
from ocsf.v1_2_0.enums.config_state_activity_id import ConfigStateActivityId
from ocsf.v1_2_0.enums.config_state_severity_id import ConfigStateSeverityId
from ocsf.v1_2_0.enums.config_state_status_id import ConfigStateStatusId
from ocsf.v1_2_0.enums.cvss_depth import CvssDepth
from ocsf.v1_2_0.enums.data_classification_category_id import DataClassificationCategoryId
from ocsf.v1_2_0.enums.data_classification_confidentiality_id import (
    DataClassificationConfidentialityId,
)
from ocsf.v1_2_0.enums.data_security_category_id import DataSecurityCategoryId
from ocsf.v1_2_0.enums.data_security_confidentiality_id import DataSecurityConfidentialityId
from ocsf.v1_2_0.enums.data_security_data_lifecycle_state_id import DataSecurityDataLifecycleStateId
from ocsf.v1_2_0.enums.data_security_detection_system_id import DataSecurityDetectionSystemId
from ocsf.v1_2_0.enums.data_security_finding_activity_id import DataSecurityFindingActivityId
from ocsf.v1_2_0.enums.data_security_finding_confidence_id import DataSecurityFindingConfidenceId
from ocsf.v1_2_0.enums.data_security_finding_impact_id import DataSecurityFindingImpactId
from ocsf.v1_2_0.enums.data_security_finding_risk_level_id import DataSecurityFindingRiskLevelId
from ocsf.v1_2_0.enums.data_security_finding_severity_id import DataSecurityFindingSeverityId
from ocsf.v1_2_0.enums.data_security_finding_status_id import DataSecurityFindingStatusId
from ocsf.v1_2_0.enums.database_type_id import DatabaseTypeId
from ocsf.v1_2_0.enums.databucket_type_id import DatabucketTypeId
from ocsf.v1_2_0.enums.datastore_activity_activity_id import DatastoreActivityActivityId
from ocsf.v1_2_0.enums.datastore_activity_severity_id import DatastoreActivitySeverityId
from ocsf.v1_2_0.enums.datastore_activity_status_id import DatastoreActivityStatusId
from ocsf.v1_2_0.enums.datastore_activity_type_id import DatastoreActivityTypeId
from ocsf.v1_2_0.enums.detection_finding_activity_id import DetectionFindingActivityId
from ocsf.v1_2_0.enums.detection_finding_confidence_id import DetectionFindingConfidenceId
from ocsf.v1_2_0.enums.detection_finding_impact_id import DetectionFindingImpactId
from ocsf.v1_2_0.enums.detection_finding_risk_level_id import DetectionFindingRiskLevelId
from ocsf.v1_2_0.enums.detection_finding_severity_id import DetectionFindingSeverityId
from ocsf.v1_2_0.enums.detection_finding_status_id import DetectionFindingStatusId
from ocsf.v1_2_0.enums.device_config_state_change_activity_id import (
    DeviceConfigStateChangeActivityId,
)
from ocsf.v1_2_0.enums.device_config_state_change_prev_security_level_id import (
    DeviceConfigStateChangePrevSecurityLevelId,
)
from ocsf.v1_2_0.enums.device_config_state_change_security_level_id import (
    DeviceConfigStateChangeSecurityLevelId,
)
from ocsf.v1_2_0.enums.device_config_state_change_severity_id import (
    DeviceConfigStateChangeSeverityId,
)
from ocsf.v1_2_0.enums.device_config_state_change_status_id import DeviceConfigStateChangeStatusId
from ocsf.v1_2_0.enums.device_risk_level_id import DeviceRiskLevelId
from ocsf.v1_2_0.enums.device_type_id import DeviceTypeId
from ocsf.v1_2_0.enums.dhcp_activity_activity_id import DhcpActivityActivityId
from ocsf.v1_2_0.enums.dhcp_activity_severity_id import DhcpActivitySeverityId
from ocsf.v1_2_0.enums.dhcp_activity_status_id import DhcpActivityStatusId
from ocsf.v1_2_0.enums.digital_signature_algorithm_id import DigitalSignatureAlgorithmId
from ocsf.v1_2_0.enums.discovery_activity_id import DiscoveryActivityId
from ocsf.v1_2_0.enums.discovery_result_activity_id import DiscoveryResultActivityId
from ocsf.v1_2_0.enums.discovery_result_query_result_id import DiscoveryResultQueryResultId
from ocsf.v1_2_0.enums.discovery_result_severity_id import DiscoveryResultSeverityId
from ocsf.v1_2_0.enums.discovery_result_status_id import DiscoveryResultStatusId
from ocsf.v1_2_0.enums.discovery_severity_id import DiscoverySeverityId
from ocsf.v1_2_0.enums.discovery_status_id import DiscoveryStatusId
from ocsf.v1_2_0.enums.dns_activity_activity_id import DnsActivityActivityId
from ocsf.v1_2_0.enums.dns_activity_rcode_id import DnsActivityRcodeId
from ocsf.v1_2_0.enums.dns_activity_severity_id import DnsActivitySeverityId
from ocsf.v1_2_0.enums.dns_activity_status_id import DnsActivityStatusId
from ocsf.v1_2_0.enums.dns_answer_flag_ids import DnsAnswerFlagIds
from ocsf.v1_2_0.enums.dns_query_opcode_id import DnsQueryOpcodeId
from ocsf.v1_2_0.enums.email_activity_activity_id import EmailActivityActivityId
from ocsf.v1_2_0.enums.email_activity_direction_id import EmailActivityDirectionId
from ocsf.v1_2_0.enums.email_activity_severity_id import EmailActivitySeverityId
from ocsf.v1_2_0.enums.email_activity_status_id import EmailActivityStatusId
from ocsf.v1_2_0.enums.email_file_activity_activity_id import EmailFileActivityActivityId
from ocsf.v1_2_0.enums.email_file_activity_severity_id import EmailFileActivitySeverityId
from ocsf.v1_2_0.enums.email_file_activity_status_id import EmailFileActivityStatusId
from ocsf.v1_2_0.enums.email_url_activity_activity_id import EmailUrlActivityActivityId
from ocsf.v1_2_0.enums.email_url_activity_severity_id import EmailUrlActivitySeverityId
from ocsf.v1_2_0.enums.email_url_activity_status_id import EmailUrlActivityStatusId
from ocsf.v1_2_0.enums.endpoint_type_id import EndpointTypeId
from ocsf.v1_2_0.enums.entity_management_activity_id import EntityManagementActivityId
from ocsf.v1_2_0.enums.entity_management_severity_id import EntityManagementSeverityId
from ocsf.v1_2_0.enums.entity_management_status_id import EntityManagementStatusId
from ocsf.v1_2_0.enums.file_activity_activity_id import FileActivityActivityId
from ocsf.v1_2_0.enums.file_activity_severity_id import FileActivitySeverityId
from ocsf.v1_2_0.enums.file_activity_status_id import FileActivityStatusId
from ocsf.v1_2_0.enums.file_confidentiality_id import FileConfidentialityId
from ocsf.v1_2_0.enums.file_hosting_activity_id import FileHostingActivityId
from ocsf.v1_2_0.enums.file_hosting_severity_id import FileHostingSeverityId
from ocsf.v1_2_0.enums.file_hosting_status_id import FileHostingStatusId
from ocsf.v1_2_0.enums.file_query_activity_id import FileQueryActivityId
from ocsf.v1_2_0.enums.file_query_query_result_id import FileQueryQueryResultId
from ocsf.v1_2_0.enums.file_query_severity_id import FileQuerySeverityId
from ocsf.v1_2_0.enums.file_query_status_id import FileQueryStatusId
from ocsf.v1_2_0.enums.file_type_id import FileTypeId
from ocsf.v1_2_0.enums.finding_activity_id import FindingActivityId
from ocsf.v1_2_0.enums.finding_confidence_id import FindingConfidenceId
from ocsf.v1_2_0.enums.finding_severity_id import FindingSeverityId
from ocsf.v1_2_0.enums.finding_status_id import FindingStatusId
from ocsf.v1_2_0.enums.fingerprint_algorithm_id import FingerprintAlgorithmId
from ocsf.v1_2_0.enums.folder_query_activity_id import FolderQueryActivityId
from ocsf.v1_2_0.enums.folder_query_query_result_id import FolderQueryQueryResultId
from ocsf.v1_2_0.enums.folder_query_severity_id import FolderQuerySeverityId
from ocsf.v1_2_0.enums.folder_query_status_id import FolderQueryStatusId
from ocsf.v1_2_0.enums.ftp_activity_activity_id import FtpActivityActivityId
from ocsf.v1_2_0.enums.ftp_activity_severity_id import FtpActivitySeverityId
from ocsf.v1_2_0.enums.ftp_activity_status_id import FtpActivityStatusId
from ocsf.v1_2_0.enums.group_management_activity_id import GroupManagementActivityId
from ocsf.v1_2_0.enums.group_management_severity_id import GroupManagementSeverityId
from ocsf.v1_2_0.enums.group_management_status_id import GroupManagementStatusId
from ocsf.v1_2_0.enums.http_activity_activity_id import HttpActivityActivityId
from ocsf.v1_2_0.enums.http_activity_severity_id import HttpActivitySeverityId
from ocsf.v1_2_0.enums.http_activity_status_id import HttpActivityStatusId
from ocsf.v1_2_0.enums.http_request_http_method import HttpRequestHttpMethod
from ocsf.v1_2_0.enums.iam_severity_id import IamSeverityId
from ocsf.v1_2_0.enums.iam_status_id import IamStatusId
from ocsf.v1_2_0.enums.incident_finding_activity_id import IncidentFindingActivityId
from ocsf.v1_2_0.enums.incident_finding_confidence_id import IncidentFindingConfidenceId
from ocsf.v1_2_0.enums.incident_finding_impact_id import IncidentFindingImpactId
from ocsf.v1_2_0.enums.incident_finding_priority_id import IncidentFindingPriorityId
from ocsf.v1_2_0.enums.incident_finding_severity_id import IncidentFindingSeverityId
from ocsf.v1_2_0.enums.incident_finding_status_id import IncidentFindingStatusId
from ocsf.v1_2_0.enums.incident_finding_verdict_id import IncidentFindingVerdictId
from ocsf.v1_2_0.enums.inventory_info_activity_id import InventoryInfoActivityId
from ocsf.v1_2_0.enums.inventory_info_severity_id import InventoryInfoSeverityId
from ocsf.v1_2_0.enums.inventory_info_status_id import InventoryInfoStatusId
from ocsf.v1_2_0.enums.job_query_activity_id import JobQueryActivityId
from ocsf.v1_2_0.enums.job_query_query_result_id import JobQueryQueryResultId
from ocsf.v1_2_0.enums.job_query_severity_id import JobQuerySeverityId
from ocsf.v1_2_0.enums.job_query_status_id import JobQueryStatusId
from ocsf.v1_2_0.enums.job_run_state_id import JobRunStateId
from ocsf.v1_2_0.enums.kernel_activity_activity_id import KernelActivityActivityId
from ocsf.v1_2_0.enums.kernel_activity_severity_id import KernelActivitySeverityId
from ocsf.v1_2_0.enums.kernel_activity_status_id import KernelActivityStatusId
from ocsf.v1_2_0.enums.kernel_extension_activity_id import KernelExtensionActivityId
from ocsf.v1_2_0.enums.kernel_extension_severity_id import KernelExtensionSeverityId
from ocsf.v1_2_0.enums.kernel_extension_status_id import KernelExtensionStatusId
from ocsf.v1_2_0.enums.kernel_object_query_activity_id import KernelObjectQueryActivityId
from ocsf.v1_2_0.enums.kernel_object_query_query_result_id import KernelObjectQueryQueryResultId
from ocsf.v1_2_0.enums.kernel_object_query_severity_id import KernelObjectQuerySeverityId
from ocsf.v1_2_0.enums.kernel_object_query_status_id import KernelObjectQueryStatusId
from ocsf.v1_2_0.enums.kernel_type_id import KernelTypeId
from ocsf.v1_2_0.enums.kill_chain_phase_phase_id import KillChainPhasePhaseId
from ocsf.v1_2_0.enums.malware_classification_ids import MalwareClassificationIds
from ocsf.v1_2_0.enums.memory_activity_activity_id import MemoryActivityActivityId
from ocsf.v1_2_0.enums.memory_activity_severity_id import MemoryActivitySeverityId
from ocsf.v1_2_0.enums.memory_activity_status_id import MemoryActivityStatusId
from ocsf.v1_2_0.enums.module_activity_activity_id import ModuleActivityActivityId
from ocsf.v1_2_0.enums.module_activity_severity_id import ModuleActivitySeverityId
from ocsf.v1_2_0.enums.module_activity_status_id import ModuleActivityStatusId
from ocsf.v1_2_0.enums.module_load_type_id import ModuleLoadTypeId
from ocsf.v1_2_0.enums.module_query_activity_id import ModuleQueryActivityId
from ocsf.v1_2_0.enums.module_query_query_result_id import ModuleQueryQueryResultId
from ocsf.v1_2_0.enums.module_query_severity_id import ModuleQuerySeverityId
from ocsf.v1_2_0.enums.module_query_status_id import ModuleQueryStatusId
from ocsf.v1_2_0.enums.network_activity_severity_id import NetworkActivitySeverityId
from ocsf.v1_2_0.enums.network_activity_status_id import NetworkActivityStatusId
from ocsf.v1_2_0.enums.network_connection_info_boundary_id import NetworkConnectionInfoBoundaryId
from ocsf.v1_2_0.enums.network_connection_info_direction_id import NetworkConnectionInfoDirectionId
from ocsf.v1_2_0.enums.network_connection_info_protocol_ver_id import (
    NetworkConnectionInfoProtocolVerId,
)
from ocsf.v1_2_0.enums.network_connection_query_activity_id import NetworkConnectionQueryActivityId
from ocsf.v1_2_0.enums.network_connection_query_query_result_id import (
    NetworkConnectionQueryQueryResultId,
)
from ocsf.v1_2_0.enums.network_connection_query_severity_id import NetworkConnectionQuerySeverityId
from ocsf.v1_2_0.enums.network_connection_query_state_id import NetworkConnectionQueryStateId
from ocsf.v1_2_0.enums.network_connection_query_status_id import NetworkConnectionQueryStatusId
from ocsf.v1_2_0.enums.network_endpoint_type_id import NetworkEndpointTypeId
from ocsf.v1_2_0.enums.network_file_activity_activity_id import NetworkFileActivityActivityId
from ocsf.v1_2_0.enums.network_file_activity_severity_id import NetworkFileActivitySeverityId
from ocsf.v1_2_0.enums.network_file_activity_status_id import NetworkFileActivityStatusId
from ocsf.v1_2_0.enums.network_interface_type_id import NetworkInterfaceTypeId
from ocsf.v1_2_0.enums.network_proxy_type_id import NetworkProxyTypeId
from ocsf.v1_2_0.enums.network_severity_id import NetworkSeverityId
from ocsf.v1_2_0.enums.network_status_id import NetworkStatusId
from ocsf.v1_2_0.enums.networks_query_activity_id import NetworksQueryActivityId
from ocsf.v1_2_0.enums.networks_query_query_result_id import NetworksQueryQueryResultId
from ocsf.v1_2_0.enums.networks_query_severity_id import NetworksQuerySeverityId
from ocsf.v1_2_0.enums.networks_query_status_id import NetworksQueryStatusId
from ocsf.v1_2_0.enums.ntp_activity_activity_id import NtpActivityActivityId
from ocsf.v1_2_0.enums.ntp_activity_severity_id import NtpActivitySeverityId
from ocsf.v1_2_0.enums.ntp_activity_status_id import NtpActivityStatusId
from ocsf.v1_2_0.enums.ntp_activity_stratum_id import NtpActivityStratumId
from ocsf.v1_2_0.enums.observable_type_id import ObservableTypeId
from ocsf.v1_2_0.enums.os_type_id import OsTypeId
from ocsf.v1_2_0.enums.patch_state_activity_id import PatchStateActivityId
from ocsf.v1_2_0.enums.patch_state_severity_id import PatchStateSeverityId
from ocsf.v1_2_0.enums.patch_state_status_id import PatchStateStatusId
from ocsf.v1_2_0.enums.peripheral_device_query_activity_id import PeripheralDeviceQueryActivityId
from ocsf.v1_2_0.enums.peripheral_device_query_query_result_id import (
    PeripheralDeviceQueryQueryResultId,
)
from ocsf.v1_2_0.enums.peripheral_device_query_severity_id import PeripheralDeviceQuerySeverityId
from ocsf.v1_2_0.enums.peripheral_device_query_status_id import PeripheralDeviceQueryStatusId
from ocsf.v1_2_0.enums.process_activity_activity_id import ProcessActivityActivityId
from ocsf.v1_2_0.enums.process_activity_injection_type_id import ProcessActivityInjectionTypeId
from ocsf.v1_2_0.enums.process_activity_severity_id import ProcessActivitySeverityId
from ocsf.v1_2_0.enums.process_activity_status_id import ProcessActivityStatusId
from ocsf.v1_2_0.enums.process_integrity_id import ProcessIntegrityId
from ocsf.v1_2_0.enums.process_query_activity_id import ProcessQueryActivityId
from ocsf.v1_2_0.enums.process_query_query_result_id import ProcessQueryQueryResultId
from ocsf.v1_2_0.enums.process_query_severity_id import ProcessQuerySeverityId
from ocsf.v1_2_0.enums.process_query_status_id import ProcessQueryStatusId
from ocsf.v1_2_0.enums.rdp_activity_activity_id import RdpActivityActivityId
from ocsf.v1_2_0.enums.rdp_activity_severity_id import RdpActivitySeverityId
from ocsf.v1_2_0.enums.rdp_activity_status_id import RdpActivityStatusId
from ocsf.v1_2_0.enums.reputation_score_id import ReputationScoreId
from ocsf.v1_2_0.enums.scan_activity_activity_id import ScanActivityActivityId
from ocsf.v1_2_0.enums.scan_activity_severity_id import ScanActivitySeverityId
from ocsf.v1_2_0.enums.scan_activity_status_id import ScanActivityStatusId
from ocsf.v1_2_0.enums.scan_type_id import ScanTypeId
from ocsf.v1_2_0.enums.scheduled_job_activity_activity_id import ScheduledJobActivityActivityId
from ocsf.v1_2_0.enums.scheduled_job_activity_severity_id import ScheduledJobActivitySeverityId
from ocsf.v1_2_0.enums.scheduled_job_activity_status_id import ScheduledJobActivityStatusId
from ocsf.v1_2_0.enums.security_finding_activity_id import SecurityFindingActivityId
from ocsf.v1_2_0.enums.security_finding_confidence_id import SecurityFindingConfidenceId
from ocsf.v1_2_0.enums.security_finding_impact_id import SecurityFindingImpactId
from ocsf.v1_2_0.enums.security_finding_risk_level_id import SecurityFindingRiskLevelId
from ocsf.v1_2_0.enums.security_finding_severity_id import SecurityFindingSeverityId
from ocsf.v1_2_0.enums.security_finding_state_id import SecurityFindingStateId
from ocsf.v1_2_0.enums.security_finding_status_id import SecurityFindingStatusId
from ocsf.v1_2_0.enums.security_state_state_id import SecurityStateStateId
from ocsf.v1_2_0.enums.service_query_activity_id import ServiceQueryActivityId
from ocsf.v1_2_0.enums.service_query_query_result_id import ServiceQueryQueryResultId
from ocsf.v1_2_0.enums.service_query_severity_id import ServiceQuerySeverityId
from ocsf.v1_2_0.enums.service_query_status_id import ServiceQueryStatusId
from ocsf.v1_2_0.enums.session_query_activity_id import SessionQueryActivityId
from ocsf.v1_2_0.enums.session_query_query_result_id import SessionQueryQueryResultId
from ocsf.v1_2_0.enums.session_query_severity_id import SessionQuerySeverityId
from ocsf.v1_2_0.enums.session_query_status_id import SessionQueryStatusId
from ocsf.v1_2_0.enums.smb_activity_activity_id import SmbActivityActivityId
from ocsf.v1_2_0.enums.smb_activity_severity_id import SmbActivitySeverityId
from ocsf.v1_2_0.enums.smb_activity_share_type_id import SmbActivityShareTypeId
from ocsf.v1_2_0.enums.smb_activity_status_id import SmbActivityStatusId
from ocsf.v1_2_0.enums.ssh_activity_auth_type_id import SshActivityAuthTypeId
from ocsf.v1_2_0.enums.ssh_activity_severity_id import SshActivitySeverityId
from ocsf.v1_2_0.enums.ssh_activity_status_id import SshActivityStatusId
from ocsf.v1_2_0.enums.system_severity_id import SystemSeverityId
from ocsf.v1_2_0.enums.system_status_id import SystemStatusId
from ocsf.v1_2_0.enums.tls_extension_type_id import TlsExtensionTypeId
from ocsf.v1_2_0.enums.tunnel_activity_activity_id import TunnelActivityActivityId
from ocsf.v1_2_0.enums.tunnel_activity_severity_id import TunnelActivitySeverityId
from ocsf.v1_2_0.enums.tunnel_activity_status_id import TunnelActivityStatusId
from ocsf.v1_2_0.enums.tunnel_activity_tunnel_type_id import TunnelActivityTunnelTypeId
from ocsf.v1_2_0.enums.url_category_ids import UrlCategoryIds
from ocsf.v1_2_0.enums.user_access_activity_id import UserAccessActivityId
from ocsf.v1_2_0.enums.user_access_severity_id import UserAccessSeverityId
from ocsf.v1_2_0.enums.user_access_status_id import UserAccessStatusId
from ocsf.v1_2_0.enums.user_inventory_activity_id import UserInventoryActivityId
from ocsf.v1_2_0.enums.user_inventory_severity_id import UserInventorySeverityId
from ocsf.v1_2_0.enums.user_inventory_status_id import UserInventoryStatusId
from ocsf.v1_2_0.enums.user_query_activity_id import UserQueryActivityId
from ocsf.v1_2_0.enums.user_query_query_result_id import UserQueryQueryResultId
from ocsf.v1_2_0.enums.user_query_severity_id import UserQuerySeverityId
from ocsf.v1_2_0.enums.user_query_status_id import UserQueryStatusId
from ocsf.v1_2_0.enums.user_risk_level_id import UserRiskLevelId
from ocsf.v1_2_0.enums.user_type_id import UserTypeId
from ocsf.v1_2_0.enums.vulnerability_finding_activity_id import VulnerabilityFindingActivityId
from ocsf.v1_2_0.enums.vulnerability_finding_confidence_id import VulnerabilityFindingConfidenceId
from ocsf.v1_2_0.enums.vulnerability_finding_severity_id import VulnerabilityFindingSeverityId
from ocsf.v1_2_0.enums.vulnerability_finding_status_id import VulnerabilityFindingStatusId
from ocsf.v1_2_0.enums.web_resource_access_activity_activity_id import (
    WebResourceAccessActivityActivityId,
)
from ocsf.v1_2_0.enums.web_resource_access_activity_severity_id import (
    WebResourceAccessActivitySeverityId,
)
from ocsf.v1_2_0.enums.web_resource_access_activity_status_id import (
    WebResourceAccessActivityStatusId,
)
from ocsf.v1_2_0.enums.web_resources_activity_activity_id import WebResourcesActivityActivityId
from ocsf.v1_2_0.enums.web_resources_activity_severity_id import WebResourcesActivitySeverityId
from ocsf.v1_2_0.enums.web_resources_activity_status_id import WebResourcesActivityStatusId

__all__ = [
    "AccountChangeActivityId",
    "AccountChangeSeverityId",
    "AccountChangeStatusId",
    "AccountTypeId",
    "AdminGroupQueryActivityId",
    "AdminGroupQueryQueryResultId",
    "AdminGroupQuerySeverityId",
    "AdminGroupQueryStatusId",
    "AgentTypeId",
    "AnalyticTypeId",
    "ApiActivityActivityId",
    "ApiActivitySeverityId",
    "ApiActivityStatusId",
    "ApplicationLifecycleActivityId",
    "ApplicationLifecycleSeverityId",
    "ApplicationLifecycleStatusId",
    "ApplicationSeverityId",
    "ApplicationStatusId",
    "AuthFactorFactorTypeId",
    "AuthenticationActivityId",
    "AuthenticationAuthProtocolId",
    "AuthenticationLogonTypeId",
    "AuthenticationSeverityId",
    "AuthenticationStatusId",
    "AuthorizeSessionActivityId",
    "AuthorizeSessionSeverityId",
    "AuthorizeSessionStatusId",
    "BaseEventSeverityId",
    "BaseEventStatusId",
    "ComplianceFindingActivityId",
    "ComplianceFindingConfidenceId",
    "ComplianceFindingSeverityId",
    "ComplianceFindingStatusId",
    "ComplianceStatusId",
    "ConfigStateActivityId",
    "ConfigStateSeverityId",
    "ConfigStateStatusId",
    "CvssDepth",
    "DataClassificationCategoryId",
    "DataClassificationConfidentialityId",
    "DataSecurityCategoryId",
    "DataSecurityConfidentialityId",
    "DataSecurityDataLifecycleStateId",
    "DataSecurityDetectionSystemId",
    "DataSecurityFindingActivityId",
    "DataSecurityFindingConfidenceId",
    "DataSecurityFindingImpactId",
    "DataSecurityFindingRiskLevelId",
    "DataSecurityFindingSeverityId",
    "DataSecurityFindingStatusId",
    "DatabaseTypeId",
    "DatabucketTypeId",
    "DatastoreActivityActivityId",
    "DatastoreActivitySeverityId",
    "DatastoreActivityStatusId",
    "DatastoreActivityTypeId",
    "DetectionFindingActivityId",
    "DetectionFindingConfidenceId",
    "DetectionFindingImpactId",
    "DetectionFindingRiskLevelId",
    "DetectionFindingSeverityId",
    "DetectionFindingStatusId",
    "DeviceConfigStateChangeActivityId",
    "DeviceConfigStateChangePrevSecurityLevelId",
    "DeviceConfigStateChangeSecurityLevelId",
    "DeviceConfigStateChangeSeverityId",
    "DeviceConfigStateChangeStatusId",
    "DeviceRiskLevelId",
    "DeviceTypeId",
    "DhcpActivityActivityId",
    "DhcpActivitySeverityId",
    "DhcpActivityStatusId",
    "DigitalSignatureAlgorithmId",
    "DiscoveryActivityId",
    "DiscoveryResultActivityId",
    "DiscoveryResultQueryResultId",
    "DiscoveryResultSeverityId",
    "DiscoveryResultStatusId",
    "DiscoverySeverityId",
    "DiscoveryStatusId",
    "DnsActivityActivityId",
    "DnsActivityRcodeId",
    "DnsActivitySeverityId",
    "DnsActivityStatusId",
    "DnsAnswerFlagIds",
    "DnsQueryOpcodeId",
    "EmailActivityActivityId",
    "EmailActivityDirectionId",
    "EmailActivitySeverityId",
    "EmailActivityStatusId",
    "EmailFileActivityActivityId",
    "EmailFileActivitySeverityId",
    "EmailFileActivityStatusId",
    "EmailUrlActivityActivityId",
    "EmailUrlActivitySeverityId",
    "EmailUrlActivityStatusId",
    "EndpointTypeId",
    "EntityManagementActivityId",
    "EntityManagementSeverityId",
    "EntityManagementStatusId",
    "FileActivityActivityId",
    "FileActivitySeverityId",
    "FileActivityStatusId",
    "FileConfidentialityId",
    "FileHostingActivityId",
    "FileHostingSeverityId",
    "FileHostingStatusId",
    "FileQueryActivityId",
    "FileQueryQueryResultId",
    "FileQuerySeverityId",
    "FileQueryStatusId",
    "FileTypeId",
    "FindingActivityId",
    "FindingConfidenceId",
    "FindingSeverityId",
    "FindingStatusId",
    "FingerprintAlgorithmId",
    "FolderQueryActivityId",
    "FolderQueryQueryResultId",
    "FolderQuerySeverityId",
    "FolderQueryStatusId",
    "FtpActivityActivityId",
    "FtpActivitySeverityId",
    "FtpActivityStatusId",
    "GroupManagementActivityId",
    "GroupManagementSeverityId",
    "GroupManagementStatusId",
    "HttpActivityActivityId",
    "HttpActivitySeverityId",
    "HttpActivityStatusId",
    "HttpRequestHttpMethod",
    "IamSeverityId",
    "IamStatusId",
    "IncidentFindingActivityId",
    "IncidentFindingConfidenceId",
    "IncidentFindingImpactId",
    "IncidentFindingPriorityId",
    "IncidentFindingSeverityId",
    "IncidentFindingStatusId",
    "IncidentFindingVerdictId",
    "InventoryInfoActivityId",
    "InventoryInfoSeverityId",
    "InventoryInfoStatusId",
    "JobQueryActivityId",
    "JobQueryQueryResultId",
    "JobQuerySeverityId",
    "JobQueryStatusId",
    "JobRunStateId",
    "KernelActivityActivityId",
    "KernelActivitySeverityId",
    "KernelActivityStatusId",
    "KernelExtensionActivityId",
    "KernelExtensionSeverityId",
    "KernelExtensionStatusId",
    "KernelObjectQueryActivityId",
    "KernelObjectQueryQueryResultId",
    "KernelObjectQuerySeverityId",
    "KernelObjectQueryStatusId",
    "KernelTypeId",
    "KillChainPhasePhaseId",
    "MalwareClassificationIds",
    "MemoryActivityActivityId",
    "MemoryActivitySeverityId",
    "MemoryActivityStatusId",
    "ModuleActivityActivityId",
    "ModuleActivitySeverityId",
    "ModuleActivityStatusId",
    "ModuleLoadTypeId",
    "ModuleQueryActivityId",
    "ModuleQueryQueryResultId",
    "ModuleQuerySeverityId",
    "ModuleQueryStatusId",
    "NetworkActivitySeverityId",
    "NetworkActivityStatusId",
    "NetworkConnectionInfoBoundaryId",
    "NetworkConnectionInfoDirectionId",
    "NetworkConnectionInfoProtocolVerId",
    "NetworkConnectionQueryActivityId",
    "NetworkConnectionQueryQueryResultId",
    "NetworkConnectionQuerySeverityId",
    "NetworkConnectionQueryStateId",
    "NetworkConnectionQueryStatusId",
    "NetworkEndpointTypeId",
    "NetworkFileActivityActivityId",
    "NetworkFileActivitySeverityId",
    "NetworkFileActivityStatusId",
    "NetworkInterfaceTypeId",
    "NetworkProxyTypeId",
    "NetworkSeverityId",
    "NetworkStatusId",
    "NetworksQueryActivityId",
    "NetworksQueryQueryResultId",
    "NetworksQuerySeverityId",
    "NetworksQueryStatusId",
    "NtpActivityActivityId",
    "NtpActivitySeverityId",
    "NtpActivityStatusId",
    "NtpActivityStratumId",
    "ObservableTypeId",
    "OsTypeId",
    "PatchStateActivityId",
    "PatchStateSeverityId",
    "PatchStateStatusId",
    "PeripheralDeviceQueryActivityId",
    "PeripheralDeviceQueryQueryResultId",
    "PeripheralDeviceQuerySeverityId",
    "PeripheralDeviceQueryStatusId",
    "ProcessActivityActivityId",
    "ProcessActivityInjectionTypeId",
    "ProcessActivitySeverityId",
    "ProcessActivityStatusId",
    "ProcessIntegrityId",
    "ProcessQueryActivityId",
    "ProcessQueryQueryResultId",
    "ProcessQuerySeverityId",
    "ProcessQueryStatusId",
    "RdpActivityActivityId",
    "RdpActivitySeverityId",
    "RdpActivityStatusId",
    "ReputationScoreId",
    "ScanActivityActivityId",
    "ScanActivitySeverityId",
    "ScanActivityStatusId",
    "ScanTypeId",
    "ScheduledJobActivityActivityId",
    "ScheduledJobActivitySeverityId",
    "ScheduledJobActivityStatusId",
    "SecurityFindingActivityId",
    "SecurityFindingConfidenceId",
    "SecurityFindingImpactId",
    "SecurityFindingRiskLevelId",
    "SecurityFindingSeverityId",
    "SecurityFindingStateId",
    "SecurityFindingStatusId",
    "SecurityStateStateId",
    "ServiceQueryActivityId",
    "ServiceQueryQueryResultId",
    "ServiceQuerySeverityId",
    "ServiceQueryStatusId",
    "SessionQueryActivityId",
    "SessionQueryQueryResultId",
    "SessionQuerySeverityId",
    "SessionQueryStatusId",
    "SmbActivityActivityId",
    "SmbActivitySeverityId",
    "SmbActivityShareTypeId",
    "SmbActivityStatusId",
    "SshActivityAuthTypeId",
    "SshActivitySeverityId",
    "SshActivityStatusId",
    "SystemSeverityId",
    "SystemStatusId",
    "TlsExtensionTypeId",
    "TunnelActivityActivityId",
    "TunnelActivitySeverityId",
    "TunnelActivityStatusId",
    "TunnelActivityTunnelTypeId",
    "UrlCategoryIds",
    "UserAccessActivityId",
    "UserAccessSeverityId",
    "UserAccessStatusId",
    "UserInventoryActivityId",
    "UserInventorySeverityId",
    "UserInventoryStatusId",
    "UserQueryActivityId",
    "UserQueryQueryResultId",
    "UserQuerySeverityId",
    "UserQueryStatusId",
    "UserRiskLevelId",
    "UserTypeId",
    "VulnerabilityFindingActivityId",
    "VulnerabilityFindingConfidenceId",
    "VulnerabilityFindingSeverityId",
    "VulnerabilityFindingStatusId",
    "WebResourceAccessActivityActivityId",
    "WebResourceAccessActivitySeverityId",
    "WebResourceAccessActivityStatusId",
    "WebResourcesActivityActivityId",
    "WebResourcesActivitySeverityId",
    "WebResourcesActivityStatusId",
]
