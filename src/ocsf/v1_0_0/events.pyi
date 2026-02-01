"""OCSF Events - Type stubs (auto-generated)."""

from __future__ import annotations

from typing import Any

from typing_extensions import Self

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

class AccountChange(Iam):
    class ActivityId(SiblingEnum):
        CREATE = 1
        ENABLE = 2
        PASSWORD_CHANGE = 3
        PASSWORD_RESET = 4
        DISABLE = 5
        DELETE = 6
        ATTACH_POLICY = 7
        DETACH_POLICY = 8
        LOCK = 9
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    actor: Any | None = None
    http_request: Any | None = None
    src_endpoint: Any | None = None
    user: Any
    user_result: Any | None = None

class ApiActivity(Application):
    class ActivityId(SiblingEnum):
        CREATE = 1
        READ = 2
        UPDATE = 3
        DELETE = 4
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    actor: Any
    api: Any
    dst_endpoint: Any | None = None
    http_request: Any | None = None
    resources: list[Any] | None = None
    src_endpoint: Any

class Application(BaseEvent):
    pass

class ApplicationLifecycle(Application):
    class ActivityId(SiblingEnum):
        INSTALL = 1
        REMOVE = 2
        START = 3
        STOP = 4
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int
    app: Any

class Authentication(Iam):
    class ActivityId(SiblingEnum):
        LOGON = 1
        LOGOFF = 2
        AUTHENTICATION_TICKET = 3
        SERVICE_TICKET = 4
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class AuthProtocolId(SiblingEnum):
        UNKNOWN = 0
        NTLM = 1
        KERBEROS = 2
        DIGEST = 3
        OPENID = 4
        SAML = 5
        OAUTH_20 = 6
        PAP = 7
        CHAP = 8
        EAP = 9
        RADIUS = 10
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class LogonTypeId(SiblingEnum):
        SYSTEM = 0
        INTERACTIVE = 2
        NETWORK = 3
        BATCH = 4
        OS_SERVICE = 5
        UNLOCK = 7
        NETWORK_CLEARTEXT = 8
        NEW_CREDENTIALS = 9
        REMOTE_INTERACTIVE = 10
        CACHED_INTERACTIVE = 11
        CACHED_REMOTE_INTERACTIVE = 12
        CACHED_UNLOCK = 13
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    actor: Any | None = None
    auth_protocol: str | None = None
    auth_protocol_id: int | None = None
    certificate: Any | None = None
    dst_endpoint: Any | None = None
    http_request: Any | None = None
    is_cleartext: bool | None = None
    is_mfa: bool | None = None
    is_new_logon: bool | None = None
    is_remote: bool | None = None
    logon_process: Any | None = None
    logon_type: str | None = None
    logon_type_id: int | None = None
    service: Any | None = None
    session: Any | None = None
    src_endpoint: Any | None = None
    status_detail: str | None = None
    user: Any

class AuthorizeSession(Iam):
    class ActivityId(SiblingEnum):
        UNKNOWN = 0
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    dst_endpoint: Any | None = None
    group: Any | None = None
    privileges: list[str] | None = None
    session: Any | None = None
    user: Any

class BaseEvent(OCSFBaseModel):
    class SeverityId(SiblingEnum):
        UNKNOWN = 0
        INFORMATIONAL = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4
        CRITICAL = 5
        FATAL = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class StatusId(SiblingEnum):
        UNKNOWN = 0
        SUCCESS = 1
        FAILURE = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    enrichments: list[Any] | None = None
    message: str | None = None
    metadata: Any
    observables: list[Any] | None = None
    raw_data: str | None = None
    severity: str | None = None
    severity_id: int
    status: str | None = None
    status_code: str | None = None
    status_detail: str | None = None
    status_id: int | None = None
    unmapped: Any | None = None

class ConfigState(Discovery):
    actor: Any | None = None
    cis_benchmark_result: Any | None = None
    device: Any

class DhcpActivity(BaseEvent):
    class ActivityId(SiblingEnum):
        DISCOVER = 1
        OFFER = 2
        REQUEST = 3
        DECLINE = 4
        ACK = 5
        NAK = 6
        RELEASE = 7
        INFORM = 8
        EXPIRE = 9
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int
    dst_endpoint: Any | None = None
    is_renewal: bool | None = None
    lease_dur: int | None = None
    relay: Any | None = None
    src_endpoint: Any | None = None
    transaction_uid: str | None = None

class Discovery(BaseEvent):
    class ActivityId(SiblingEnum):
        LOG = 1
        COLLECT = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None

class DnsActivity(NetworkActivity):
    class ActivityId(SiblingEnum):
        UNKNOWN = 0
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class RcodeId(SiblingEnum):
        NOERROR = 0
        FORMERROR = 1
        SERVERROR = 2
        NXDOMAIN = 3
        NOTIMP = 4
        REFUSED = 5
        YXDOMAIN = 6
        YXRRSET = 7
        NXRRSET = 8
        NOTAUTH = 9
        NOTZONE = 10
        DSOTYPENI = 11
        BADSIG_VERS = 16
        BADKEY = 17
        BADTIME = 18
        BADMODE = 19
        BADNAME = 20
        BADALG = 21
        BADTRUNC = 22
        BADCOOKIE = 23
        UNASSIGNED = 24
        RESERVED = 25
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    answers: list[Any] | None = None
    connection_info: Any | None = None
    proxy: Any | None = None
    query: Any | None = None
    query_time: int | None = None
    rcode: str | None = None
    rcode_id: int | None = None
    response_time: int | None = None
    traffic: Any | None = None

class EmailActivity(BaseEvent):
    class ActivityId(SiblingEnum):
        SEND = 1
        RECEIVE = 2
        SCAN = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class DirectionId(SiblingEnum):
        UNKNOWN = 0
        INBOUND = 1
        OUTBOUND = 2
        INTERNAL = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    attempt: int | None = None
    banner: str | None = None
    direction: str | None = None
    direction_id: int
    dst_endpoint: Any | None = None
    email: Any
    email_auth: Any | None = None
    smtp_hello: str | None = None
    src_endpoint: Any | None = None

class EmailFileActivity(BaseEvent):
    class ActivityId(SiblingEnum):
        SEND = 1
        RECEIVE = 2
        SCAN = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    email_uid: str
    file: Any

class EmailUrlActivity(BaseEvent):
    class ActivityId(SiblingEnum):
        SEND = 1
        RECEIVE = 2
        SCAN = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    email_uid: str
    url: Any

class EntityManagement(Iam):
    class ActivityId(SiblingEnum):
        CREATE = 1
        READ = 2
        UPDATE = 3
        DELETE = 4
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    actor: Any | None = None
    comment: str | None = None
    entity: Any
    entity_result: Any | None = None

class FileActivity(System):
    class ActivityId(SiblingEnum):
        UNKNOWN = 0
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    access_mask: int | None = None
    activity_id: int | None = None
    actor: Any
    component: str | None = None
    connection_uid: str | None = None
    create_mask: str | None = None
    file: Any
    file_diff: str | None = None
    file_result: Any | None = None

class Findings(BaseEvent):
    class ActivityId(SiblingEnum):
        CREATE = 1
        UPDATE = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None

class FtpActivity(NetworkActivity):
    class ActivityId(SiblingEnum):
        PUT = 1
        GET = 2
        POLL = 3
        DELETE = 4
        RENAME = 5
        LIST = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    codes: list[int] | None = None
    command: str | None = None
    command_responses: list[str] | None = None
    name: str | None = None
    port: Any | None = None

class GroupManagement(Iam):
    class ActivityId(SiblingEnum):
        ASSIGN_PRIVILEGES = 1
        REVOKE_PRIVILEGES = 2
        ADD_USER = 3
        REMOVE_USER = 4
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    group: Any
    privileges: list[str] | None = None
    resource: Any | None = None
    user: Any | None = None

class HttpActivity(NetworkActivity):
    class ActivityId(SiblingEnum):
        UNKNOWN = 0
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    http_request: Any
    http_response: Any
    http_status: int | None = None

class Iam(BaseEvent):
    pass

class InventoryInfo(Discovery):
    actor: Any | None = None
    device: Any

class KernelActivity(System):
    class ActivityId(SiblingEnum):
        UNKNOWN = 0
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    kernel: Any

class KernelExtension(System):
    class ActivityId(SiblingEnum):
        UNKNOWN = 0
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    actor: Any
    driver: Any

class MemoryActivity(System):
    class ActivityId(SiblingEnum):
        UNKNOWN = 0
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    actual_permissions: int | None = None
    base_address: str | None = None
    process: Any
    requested_permissions: int | None = None
    size: int | None = None

class ModuleActivity(System):
    class ActivityId(SiblingEnum):
        UNKNOWN = 0
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    actor: Any
    module: Any

class NetworkActivity(BaseEvent):
    class ActivityId(SiblingEnum):
        UNKNOWN = 0
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None

class NetworkFileActivity(BaseEvent):
    class ActivityId(SiblingEnum):
        UPLOAD = 1
        DOWNLOAD = 2
        UPDATE = 3
        DELETE = 4
        RENAME = 5
        COPY = 6
        MOVE = 7
        RESTORE = 8
        PREVIEW = 9
        LOCK = 10
        UNLOCK = 11
        SHARE = 12
        UNSHARE = 13
        OPEN = 14
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    actor: Any
    expiration_time: int | None = None
    file: Any
    src_endpoint: Any

class ProcessActivity(System):
    class ActivityId(SiblingEnum):
        UNKNOWN = 0
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class InjectionTypeId(SiblingEnum):
        UNKNOWN = 0
        REMOTE_THREAD = 1
        LOAD_LIBRARY = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    actor: Any | None = None
    actual_permissions: int | None = None
    exit_code: int | None = None
    injection_type: str | None = None
    injection_type_id: int | None = None
    module: Any | None = None
    process: Any
    requested_permissions: int | None = None

class RdpActivity(NetworkActivity):
    class ActivityId(SiblingEnum):
        INITIAL_REQUEST = 1
        INITIAL_RESPONSE = 2
        CONNECT_REQUEST = 3
        CONNECT_RESPONSE = 4
        TLS_HANDSHAKE = 5
        TRAFFIC = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    capabilities: list[str] | None = None
    certificate_chain: list[str] | None = None
    device: Any | None = None
    identifier_cookie: str | None = None
    protocol_ver: str | None = None
    remote_display: Any | None = None
    request: Any | None = None
    response: Any | None = None

class ScheduledJobActivity(System):
    class ActivityId(SiblingEnum):
        CREATE = 1
        UPDATE = 2
        DELETE = 3
        ENABLE = 4
        DISABLE = 5
        START = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    actor: Any | None = None
    job: Any

class SecurityFinding(Findings):
    class ConfidenceId(SiblingEnum):
        UNKNOWN = 0
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class ImpactId(SiblingEnum):
        UNKNOWN = 0
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        CRITICAL = 4
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class RiskLevelId(SiblingEnum):
        INFO = 0
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        CRITICAL = 4
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class StateId(SiblingEnum):
        NEW = 1
        IN_PROGRESS = 2
        SUPPRESSED = 3
        RESOLVED = 4
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    analytic: Any | None = None
    attacks: list[Any] | None = None
    cis_csc: list[Any] | None = None
    compliance: Any | None = None
    confidence: str | None = None
    confidence_id: int | None = None
    confidence_score: int | None = None
    data_sources: list[str] | None = None
    evidence: dict[str, Any] | None = None
    finding: Any
    impact: str | None = None
    impact_id: int | None = None
    impact_score: int | None = None
    kill_chain: list[Any] | None = None
    malware: list[Any] | None = None
    nist: list[str] | None = None
    process: Any | None = None
    resources: list[Any] | None = None
    risk_level: str | None = None
    risk_level_id: int | None = None
    risk_score: int | None = None
    state: str | None = None
    state_id: int
    vulnerabilities: list[Any] | None = None

class SmbActivity(NetworkActivity):
    class ActivityId(SiblingEnum):
        FILE_SUPERSEDE = 1
        FILE_OPEN = 2
        FILE_CREATE = 3
        FILE_OPEN_IF = 4
        FILE_OVERWRITE = 5
        FILE_OVERWRITE_IF = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class ShareTypeId(SiblingEnum):
        UNKNOWN = 0
        FILE = 1
        PIPE = 2
        PRINT = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    client_dialects: list[str] | None = None
    command: str | None = None
    dce_rpc: Any | None = None
    dialect: str | None = None
    file: Any | None = None
    open_type: str | None = None
    response: Any | None = None
    share: str | None = None
    share_type: str | None = None
    share_type_id: int | None = None
    tree_uid: str | None = None

class SshActivity(NetworkActivity):
    client_hassh: Any | None = None
    protocol_ver: str | None = None
    server_hassh: Any | None = None

class System(BaseEvent):
    actor: Any
    device: Any

class UserAccess(Iam):
    class ActivityId(SiblingEnum):
        ASSIGN_PRIVILEGES = 1
        REVOKE_PRIVILEGES = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    privileges: list[str]
    resource: Any | None = None
    user: Any

class WebResourceAccessActivity(Application):
    class ActivityId(SiblingEnum):
        ACCESS_GRANT = 1
        ACCESS_DENY = 2
        ACCESS_REVOKE = 3
        ACCESS_ERROR = 4
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    http_request: Any
    http_response: Any | None = None
    proxy: Any | None = None
    src_endpoint: Any | None = None
    tls: Any | None = None
    web_resources: list[Any]

class WebResourcesActivity(BaseEvent):
    class ActivityId(SiblingEnum):
        CREATE = 1
        READ = 2
        UPDATE = 3
        DELETE = 4
        SEARCH = 5
        IMPORT = 6
        EXPORT = 7
        SHARE = 8
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int | None = None
    dst_endpoint: Any | None = None
    src_endpoint: Any | None = None
    web_resources: list[Any]
    web_resources_result: list[Any] | None = None
