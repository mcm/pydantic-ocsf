"""OCSF v1.2.0 objects."""

from __future__ import annotations

import sys
from typing import Any

__all__ = [
    "Account",
    "Actor",
    "AffectedCode",
    "AffectedPackage",
    "Agent",
    "Analytic",
    "Api",
    "Attack",
    "AuthFactor",
    "Authorization",
    "AutonomousSystem",
    "Certificate",
    "CisBenchmark",
    "CisBenchmarkResult",
    "CisControl",
    "CisCsc",
    "Cloud",
    "Compliance",
    "Container",
    "Cve",
    "Cvss",
    "Cwe",
    "DataClassification",
    "DataSecurity",
    "Database",
    "Databucket",
    "DceRpc",
    "Device",
    "DeviceHwInfo",
    "DigitalSignature",
    "Display",
    "Dns",
    "DnsAnswer",
    "DnsQuery",
    "Email",
    "EmailAuth",
    "Endpoint",
    "EndpointConnection",
    "Enrichment",
    "Entity",
    "Epss",
    "Evidences",
    "Extension",
    "Feature",
    "File",
    "Finding",
    "FindingInfo",
    "Fingerprint",
    "FirewallRule",
    "Group",
    "Hassh",
    "HttpCookie",
    "HttpHeader",
    "HttpRequest",
    "HttpResponse",
    "Idp",
    "Image",
    "Job",
    "KbArticle",
    "Kernel",
    "KernelDriver",
    "KeyboardInfo",
    "KillChainPhase",
    "LdapPerson",
    "LoadBalancer",
    "Location",
    "Logger",
    "Malware",
    "ManagedEntity",
    "Metadata",
    "Metric",
    "Module",
    "NetworkConnectionInfo",
    "NetworkEndpoint",
    "NetworkInterface",
    "NetworkProxy",
    "NetworkTraffic",
    "Object",
    "Observable",
    "Organization",
    "Os",
    "Package",
    "PeripheralDevice",
    "Policy",
    "Process",
    "Product",
    "QueryInfo",
    "RelatedEvent",
    "Remediation",
    "Reputation",
    "Request",
    "Resource",
    "ResourceDetails",
    "Response",
    "RpcInterface",
    "Rule",
    "San",
    "Scan",
    "SecurityState",
    "Service",
    "Session",
    "SubTechnique",
    "Table",
    "Tactic",
    "Technique",
    "Tls",
    "TlsExtension",
    "Url",
    "User",
    "Vulnerability",
    "WebResource",
]

# Mapping of class names to their module file names
_MODULE_MAP = {
    "Account": "account",
    "Actor": "actor",
    "AffectedCode": "affected_code",
    "AffectedPackage": "affected_package",
    "Agent": "agent",
    "Analytic": "analytic",
    "Api": "api",
    "Attack": "attack",
    "AuthFactor": "auth_factor",
    "Authorization": "authorization",
    "AutonomousSystem": "autonomous_system",
    "Certificate": "certificate",
    "CisBenchmark": "cis_benchmark",
    "CisBenchmarkResult": "cis_benchmark_result",
    "CisControl": "cis_control",
    "CisCsc": "cis_csc",
    "Cloud": "cloud",
    "Compliance": "compliance",
    "Container": "container",
    "Cve": "cve",
    "Cvss": "cvss",
    "Cwe": "cwe",
    "DataClassification": "data_classification",
    "DataSecurity": "data_security",
    "Database": "database",
    "Databucket": "databucket",
    "DceRpc": "dce_rpc",
    "Device": "device",
    "DeviceHwInfo": "device_hw_info",
    "DigitalSignature": "digital_signature",
    "Display": "display",
    "Dns": "_dns",
    "DnsAnswer": "dns_answer",
    "DnsQuery": "dns_query",
    "Email": "email",
    "EmailAuth": "email_auth",
    "Endpoint": "endpoint",
    "EndpointConnection": "endpoint_connection",
    "Enrichment": "enrichment",
    "Entity": "_entity",
    "Epss": "epss",
    "Evidences": "evidences",
    "Extension": "extension",
    "Feature": "feature",
    "File": "file",
    "Finding": "finding",
    "FindingInfo": "finding_info",
    "Fingerprint": "fingerprint",
    "FirewallRule": "firewall_rule",
    "Group": "group",
    "Hassh": "hassh",
    "HttpCookie": "http_cookie",
    "HttpHeader": "http_header",
    "HttpRequest": "http_request",
    "HttpResponse": "http_response",
    "Idp": "idp",
    "Image": "image",
    "Job": "job",
    "KbArticle": "kb_article",
    "Kernel": "kernel",
    "KernelDriver": "kernel_driver",
    "KeyboardInfo": "keyboard_info",
    "KillChainPhase": "kill_chain_phase",
    "LdapPerson": "ldap_person",
    "LoadBalancer": "load_balancer",
    "Location": "location",
    "Logger": "logger",
    "Malware": "malware",
    "ManagedEntity": "managed_entity",
    "Metadata": "metadata",
    "Metric": "metric",
    "Module": "module",
    "NetworkConnectionInfo": "network_connection_info",
    "NetworkEndpoint": "network_endpoint",
    "NetworkInterface": "network_interface",
    "NetworkProxy": "network_proxy",
    "NetworkTraffic": "network_traffic",
    "Object": "object",
    "Observable": "observable",
    "Organization": "organization",
    "Os": "os",
    "Package": "package",
    "PeripheralDevice": "peripheral_device",
    "Policy": "policy",
    "Process": "process",
    "Product": "product",
    "QueryInfo": "query_info",
    "RelatedEvent": "related_event",
    "Remediation": "remediation",
    "Reputation": "reputation",
    "Request": "request",
    "Resource": "_resource",
    "ResourceDetails": "resource_details",
    "Response": "response",
    "RpcInterface": "rpc_interface",
    "Rule": "rule",
    "San": "san",
    "Scan": "scan",
    "SecurityState": "security_state",
    "Service": "service",
    "Session": "session",
    "SubTechnique": "sub_technique",
    "Table": "table",
    "Tactic": "tactic",
    "Technique": "technique",
    "Tls": "tls",
    "TlsExtension": "tls_extension",
    "Url": "url",
    "User": "user",
    "Vulnerability": "vulnerability",
    "WebResource": "web_resource",
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
