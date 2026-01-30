"""OCSF v1.0.0 event classes."""

from __future__ import annotations

import sys
from typing import Any

__all__ = [
    "AccountChange",
    "ApiActivity",
    "ApplicationLifecycle",
    "Authentication",
    "AuthorizeSession",
    "ConfigState",
    "DhcpActivity",
    "DnsActivity",
    "EmailActivity",
    "EmailFileActivity",
    "EmailUrlActivity",
    "EntityManagement",
    "FileActivity",
    "FtpActivity",
    "GroupManagement",
    "HttpActivity",
    "InventoryInfo",
    "KernelActivity",
    "KernelExtension",
    "MemoryActivity",
    "ModuleActivity",
    "NetworkActivity",
    "NetworkFileActivity",
    "ProcessActivity",
    "RdpActivity",
    "ScheduledJobActivity",
    "SecurityFinding",
    "SmbActivity",
    "SshActivity",
    "UserAccess",
    "WebResourceAccessActivity",
    "WebResourcesActivity",
]

# Mapping of class names to their module file names
_MODULE_MAP = {
    "AccountChange": "account_change",
    "ApiActivity": "api_activity",
    "ApplicationLifecycle": "application_lifecycle",
    "Authentication": "authentication",
    "AuthorizeSession": "authorize_session",
    "ConfigState": "config_state",
    "DhcpActivity": "dhcp_activity",
    "DnsActivity": "dns_activity",
    "EmailActivity": "email_activity",
    "EmailFileActivity": "email_file_activity",
    "EmailUrlActivity": "email_url_activity",
    "EntityManagement": "entity_management",
    "FileActivity": "file_activity",
    "FtpActivity": "ftp_activity",
    "GroupManagement": "group_management",
    "HttpActivity": "http_activity",
    "InventoryInfo": "inventory_info",
    "KernelActivity": "kernel_activity",
    "KernelExtension": "kernel_extension",
    "MemoryActivity": "memory_activity",
    "ModuleActivity": "module_activity",
    "NetworkActivity": "network_activity",
    "NetworkFileActivity": "network_file_activity",
    "ProcessActivity": "process_activity",
    "RdpActivity": "rdp_activity",
    "ScheduledJobActivity": "scheduled_job_activity",
    "SecurityFinding": "security_finding",
    "SmbActivity": "smb_activity",
    "SshActivity": "ssh_activity",
    "UserAccess": "user_access",
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
