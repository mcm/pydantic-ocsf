"""OCSF v1.2.0 event classes."""

from __future__ import annotations

import sys
from typing import Any

__all__ = [
    "AccountChange",
    "AdminGroupQuery",
    "ApiActivity",
    "ApplicationLifecycle",
    "Authentication",
    "AuthorizeSession",
    "ComplianceFinding",
    "ConfigState",
    "DataSecurityFinding",
    "DatastoreActivity",
    "DetectionFinding",
    "DeviceConfigStateChange",
    "DhcpActivity",
    "DnsActivity",
    "EmailActivity",
    "EmailFileActivity",
    "EmailUrlActivity",
    "EntityManagement",
    "FileActivity",
    "FileHosting",
    "FileQuery",
    "FolderQuery",
    "FtpActivity",
    "GroupManagement",
    "HttpActivity",
    "IncidentFinding",
    "InventoryInfo",
    "JobQuery",
    "KernelActivity",
    "KernelExtension",
    "KernelObjectQuery",
    "MemoryActivity",
    "ModuleActivity",
    "ModuleQuery",
    "NetworkActivity",
    "NetworkConnectionQuery",
    "NetworkFileActivity",
    "NetworksQuery",
    "NtpActivity",
    "PatchState",
    "PeripheralDeviceQuery",
    "ProcessActivity",
    "ProcessQuery",
    "RdpActivity",
    "ScanActivity",
    "ScheduledJobActivity",
    "SecurityFinding",
    "ServiceQuery",
    "SessionQuery",
    "SmbActivity",
    "SshActivity",
    "TunnelActivity",
    "UserAccess",
    "UserInventory",
    "UserQuery",
    "VulnerabilityFinding",
    "WebResourceAccessActivity",
    "WebResourcesActivity",
]

# Mapping of class names to their module file names
_MODULE_MAP = {
    "AccountChange": "account_change",
    "AdminGroupQuery": "admin_group_query",
    "ApiActivity": "api_activity",
    "ApplicationLifecycle": "application_lifecycle",
    "Authentication": "authentication",
    "AuthorizeSession": "authorize_session",
    "ComplianceFinding": "compliance_finding",
    "ConfigState": "config_state",
    "DataSecurityFinding": "data_security_finding",
    "DatastoreActivity": "datastore_activity",
    "DetectionFinding": "detection_finding",
    "DeviceConfigStateChange": "device_config_state_change",
    "DhcpActivity": "dhcp_activity",
    "DnsActivity": "dns_activity",
    "EmailActivity": "email_activity",
    "EmailFileActivity": "email_file_activity",
    "EmailUrlActivity": "email_url_activity",
    "EntityManagement": "entity_management",
    "FileActivity": "file_activity",
    "FileHosting": "file_hosting",
    "FileQuery": "file_query",
    "FolderQuery": "folder_query",
    "FtpActivity": "ftp_activity",
    "GroupManagement": "group_management",
    "HttpActivity": "http_activity",
    "IncidentFinding": "incident_finding",
    "InventoryInfo": "inventory_info",
    "JobQuery": "job_query",
    "KernelActivity": "kernel_activity",
    "KernelExtension": "kernel_extension",
    "KernelObjectQuery": "kernel_object_query",
    "MemoryActivity": "memory_activity",
    "ModuleActivity": "module_activity",
    "ModuleQuery": "module_query",
    "NetworkActivity": "network_activity",
    "NetworkConnectionQuery": "network_connection_query",
    "NetworkFileActivity": "network_file_activity",
    "NetworksQuery": "networks_query",
    "NtpActivity": "ntp_activity",
    "PatchState": "patch_state",
    "PeripheralDeviceQuery": "peripheral_device_query",
    "ProcessActivity": "process_activity",
    "ProcessQuery": "process_query",
    "RdpActivity": "rdp_activity",
    "ScanActivity": "scan_activity",
    "ScheduledJobActivity": "scheduled_job_activity",
    "SecurityFinding": "security_finding",
    "ServiceQuery": "service_query",
    "SessionQuery": "session_query",
    "SmbActivity": "smb_activity",
    "SshActivity": "ssh_activity",
    "TunnelActivity": "tunnel_activity",
    "UserAccess": "user_access",
    "UserInventory": "user_inventory",
    "UserQuery": "user_query",
    "VulnerabilityFinding": "vulnerability_finding",
    "WebResourceAccessActivity": "web_resource_access_activity",
    "WebResourcesActivity": "web_resources_activity",
}

_imported: set[str] = set()
_rebuild_triggered = False


def __getattr__(name: str) -> Any:
    """Lazily import symbols and trigger model rebuilding if needed."""
    global _rebuild_triggered

    if name not in __all__:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    # Check if already imported and cached
    if name in _imported:
        return globals()[name]

    # Import from individual module file
    module_file = _MODULE_MAP[name]
    module_path = f"{__name__}.{module_file}"
    module = __import__(module_path, fromlist=[name])
    symbol = getattr(module, name)

    # Cache in globals
    globals()[name] = symbol
    _imported.add(name)

    # For models (objects/events), ensure they're rebuilt via version module
    # Only trigger once to avoid recursion
    if True:
        if not _rebuild_triggered:
            _rebuild_triggered = True
            # Trigger version-level batch rebuild
            version_module_name = ".".join(__name__.split(".")[:-1])
            version_module = sys.modules.get(version_module_name)
            if version_module and hasattr(version_module, "_rebuild_all_models"):
                # Call rebuild function directly to avoid recursion through __getattr__
                version_module._rebuild_all_models()

    return symbol


def __dir__() -> list[str]:
    """Support for dir() and autocomplete."""
    return sorted(__all__)
