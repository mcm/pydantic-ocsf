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
        MFA_FACTOR_ENABLE = 10
        MFA_FACTOR_DISABLE = 11
        UNLOCK = 12
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    auth_factors: list[Any] | None = None
    policies: list[Any] | None = None
    policy: Any | None = None
    user: Any
    user_result: Any | None = None

class AdminGroupQuery(DiscoveryResult):
    group: Any
    users: list[Any] | None = None

class AirborneBroadcastActivity(UnmannedSystems):
    class ActivityId(SiblingEnum):
        UNKNOWN = 0
        CAPTURE = 1
        RECORD = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int
    aircraft: Any | None = None
    dst_endpoint: Any | None = None
    protocol_name: str | None = None
    rssi: int | None = None
    src_endpoint: Any | None = None
    traffic: Any | None = None
    unmanned_aerial_system: Any
    unmanned_system_operating_area: Any | None = None
    unmanned_system_operator: Any

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

    actor: Any
    api: Any
    dst_endpoint: Any | None = None
    http_request: Any | None = None
    http_response: Any | None = None
    resources: list[Any] | None = None
    src_endpoint: Any

class Application(BaseEvent):
    pass

class ApplicationError(Application):
    class ActivityId(SiblingEnum):
        GENERAL_ERROR = 1
        TRANSLATION_ERROR = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    message: str | None = None

class ApplicationLifecycle(Application):
    class ActivityId(SiblingEnum):
        INSTALL = 1
        REMOVE = 2
        START = 3
        STOP = 4
        RESTART = 5
        ENABLE = 6
        DISABLE = 7
        UPDATE = 8
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int
    app: Any

class ApplicationSecurityPostureFinding(Finding):
    application: Any | None = None
    compliance: Any | None = None
    remediation: Any | None = None
    resources: list[Any] | None = None
    vulnerabilities: list[Any] | None = None

class Authentication(Iam):
    class AccountSwitchTypeId(SiblingEnum):
        UNKNOWN = 0
        SUBSTITUTE_USER = 1
        IMPERSONATE = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class ActivityId(SiblingEnum):
        LOGON = 1
        LOGOFF = 2
        AUTHENTICATION_TICKET = 3
        SERVICE_TICKET_REQUEST = 4
        SERVICE_TICKET_RENEW = 5
        PREAUTH = 6
        ACCOUNT_SWITCH = 7
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
        BASIC_AUTHENTICATION = 11
        LDAP = 12
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class LogonTypeId(SiblingEnum):
        UNKNOWN = 0
        SYSTEM = 1
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

    account_switch_type: str | None = None
    account_switch_type_id: int | None = None
    auth_factors: list[Any] | None = None
    auth_protocol: str | None = None
    auth_protocol_id: int | None = None
    authentication_token: Any | None = None
    certificate: Any | None = None
    dst_endpoint: Any | None = None
    is_cleartext: bool | None = None
    is_mfa: bool | None = None
    is_new_logon: bool | None = None
    is_remote: bool | None = None
    logon_process: Any | None = None
    logon_type: str | None = None
    logon_type_id: int | None = None
    service: Any | None = None
    session: Any | None = None
    status_detail: str | None = None
    user: Any

class AuthorizeSession(Iam):
    class ActivityId(SiblingEnum):
        ASSIGN_PRIVILEGES = 1
        ASSIGN_GROUPS = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    dst_endpoint: Any | None = None
    group: Any | None = None
    privileges: list[str] | None = None
    session: Any | None = None
    user: Any

class BaseEvent(OCSFBaseModel):
    class ActivityId(SiblingEnum):
        UNKNOWN = 0
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

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

    activity_id: int
    activity_name: str | None = None
    category_name: str | None = None
    category_uid: int | None = None
    class_name: str | None = None
    class_uid: int | None = None
    count: int | None = None
    duration: int | None = None
    end_time: int | None = None
    enrichments: list[Any] | None = None
    message: str | None = None
    metadata: Any
    observables: list[Any] | None = None
    raw_data: str | None = None
    raw_data_hash: Any | None = None
    raw_data_size: int | None = None
    severity: str | None = None
    severity_id: int
    start_time: int | None = None
    status: str | None = None
    status_code: str | None = None
    status_detail: str | None = None
    status_id: int | None = None
    time: int
    timezone_offset: int | None = None
    type_name: str | None = None
    type_uid: int | None = None
    unmapped: Any | None = None

class CloudResourcesInventoryInfo(Discovery):
    cloud: Any | None = None
    container: Any | None = None
    database: Any | None = None
    databucket: Any | None = None
    idp: Any | None = None
    region: str | None = None
    resources: list[Any] | None = None
    table: Any | None = None

class ComplianceFinding(Finding):
    compliance: Any
    evidences: list[Any] | None = None
    remediation: Any | None = None
    resource: Any | None = None
    resources: list[Any] | None = None

class ConfigState(Discovery):
    actor: Any | None = None
    assessments: list[Any] | None = None
    cis_benchmark_result: Any | None = None
    device: Any

class DataSecurityFinding(Finding):
    class ActivityId(SiblingEnum):
        CREATE = 1
        UPDATE = 2
        CLOSE = 3
        SUPPRESSED = 4
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

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

    activity_id: int
    activity_name: str | None = None
    actor: Any | None = None
    confidence: str | None = None
    confidence_id: int | None = None
    confidence_score: int | None = None
    data_security: Any | None = None
    database: Any | None = None
    databucket: Any | None = None
    device: Any | None = None
    dst_endpoint: Any | None = None
    file: Any | None = None
    impact: str | None = None
    impact_id: int | None = None
    impact_score: int | None = None
    is_alert: bool | None = None
    resources: list[Any] | None = None
    risk_details: str | None = None
    risk_level: str | None = None
    risk_level_id: int | None = None
    risk_score: int | None = None
    src_endpoint: Any | None = None
    table: Any | None = None

class DatastoreActivity(Application):
    class ActivityId(SiblingEnum):
        READ = 1
        UPDATE = 2
        CONNECT = 3
        QUERY = 4
        WRITE = 5
        CREATE = 6
        DELETE = 7
        LIST = 8
        ENCRYPT = 9
        DECRYPT = 10
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class TypeId(SiblingEnum):
        UNKNOWN = 0
        DATABASE = 1
        DATABUCKET = 2
        TABLE = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    actor: Any
    database: Any | None = None
    databucket: Any | None = None
    dst_endpoint: Any | None = None
    http_request: Any | None = None
    http_response: Any | None = None
    query_info: Any | None = None
    src_endpoint: Any
    table: Any | None = None
    type_id: int | None = None

class DetectionFinding(Finding):
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

    anomaly_analyses: list[Any] | None = None
    confidence: str | None = None
    confidence_id: int | None = None
    confidence_score: int | None = None
    evidences: list[Any] | None = None
    impact: str | None = None
    impact_id: int | None = None
    impact_score: int | None = None
    is_alert: bool | None = None
    malware: list[Any] | None = None
    malware_scan_info: Any | None = None
    remediation: Any | None = None
    resources: list[Any] | None = None
    risk_details: str | None = None
    risk_level: str | None = None
    risk_level_id: int | None = None
    risk_score: int | None = None
    vulnerabilities: list[Any] | None = None

class DeviceConfigStateChange(Discovery):
    class PrevSecurityLevelId(SiblingEnum):
        UNKNOWN = 0
        SECURE = 1
        AT_RISK = 2
        COMPROMISED = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class SecurityLevelId(SiblingEnum):
        UNKNOWN = 0
        SECURE = 1
        AT_RISK = 2
        COMPROMISED = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class StateId(SiblingEnum):
        UNKNOWN = 0
        DISABLED = 1
        ENABLED = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    actor: Any | None = None
    device: Any
    prev_security_level: str | None = None
    prev_security_level_id: int | None = None
    prev_security_states: list[Any] | None = None
    security_level: str | None = None
    security_level_id: int | None = None
    security_states: list[Any] | None = None
    state: str | None = None
    state_id: int | None = None

class DhcpActivity(Network):
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


class DiscoveryResult(BaseEvent):
    class ActivityId(SiblingEnum):
        QUERY = 1
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class QueryResultId(SiblingEnum):
        UNKNOWN = 0
        EXISTS = 1
        PARTIAL = 2
        DOES_NOT_EXIST = 3
        ERROR = 4
        UNSUPPORTED = 5
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    query_info: Any | None = None
    query_result: str | None = None
    query_result_id: int

class DnsActivity(Network):
    class ActivityId(SiblingEnum):
        QUERY = 1
        RESPONSE = 2
        TRAFFIC = 6
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

    answers: list[Any] | None = None
    connection_info: Any | None = None
    dst_endpoint: Any | None = None
    query: Any | None = None
    query_time: int | None = None
    rcode: str | None = None
    rcode_id: int | None = None
    response_time: int | None = None
    traffic: Any | None = None

class DroneFlightsActivity(UnmannedSystems):
    class ActivityId(SiblingEnum):
        UNKNOWN = 0
        CAPTURE = 1
        RECORD = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class AuthProtocolId(SiblingEnum):
        UNKNOWN = 0
        NONE = 1
        UAS_ID_SIGNATURE = 2
        OPERATOR_ID_SIGNATURE = 3
        MESSAGE_SET_SIGNATURE = 4
        AUTHENTICATION_PROVIDED_BY_NETWORK_REMOTE_ID = 5
        SPECIFIC_AUTHENTICATION_METHOD = 6
        RESERVED = 7
        PRIVATE_USER = 8
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class StatusId(SiblingEnum):
        UNDECLARED = 1
        GROUND = 2
        AIRBORNE = 3
        EMERGENCY = 4
        REMOTE_ID_SYSTEM_FAILURE = 5
        RESERVED = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int
    auth_protocol: str | None = None
    auth_protocol_id: int | None = None
    classification: str | None = None
    comment: str | None = None
    protocol_name: str | None = None
    src_endpoint: Any | None = None
    status: str | None = None
    status_id: int | None = None
    traffic: Any | None = None
    unmanned_aerial_system: Any
    unmanned_system_operating_area: Any | None = None
    unmanned_system_operator: Any

class EmailActivity(BaseEvent):
    class ActivityId(SiblingEnum):
        SEND = 1
        RECEIVE = 2
        SCAN = 3
        TRACE = 4
        MTA_RELAY = 5
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

    activity_id: int
    attempt: int | None = None
    banner: str | None = None
    command: str | None = None
    direction: str | None = None
    direction_id: int
    dst_endpoint: Any | None = None
    email: Any
    email_auth: Any | None = None
    message_trace_uid: str | None = None
    protocol_name: str | None = None
    smtp_hello: str | None = None
    src_endpoint: Any | None = None
    to: list[Any] | None = None

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

    activity_id: int
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

    activity_id: int
    email_uid: str
    url: Any

class EntityManagement(Iam):
    class ActivityId(SiblingEnum):
        CREATE = 1
        READ = 2
        UPDATE = 3
        DELETE = 4
        MOVE = 5
        ENROLL = 6
        UNENROLL = 7
        ENABLE = 8
        DISABLE = 9
        ACTIVATE = 10
        DEACTIVATE = 11
        SUSPEND = 12
        RESUME = 13
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    access_list: list[str] | None = None
    access_mask: int | None = None
    comment: str | None = None
    entity: Any
    entity_result: Any | None = None

class EventLogActvity(System):
    class ActivityId(SiblingEnum):
        CLEAR = 1
        DELETE = 2
        EXPORT = 3
        ARCHIVE = 4
        ROTATE = 5
        START = 6
        STOP = 7
        RESTART = 8
        ENABLE = 9
        DISABLE = 10
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class LogTypeId(SiblingEnum):
        UNKNOWN = 0
        OS = 1
        APPLICATION = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    actor: Any | None = None
    device: Any | None = None
    dst_endpoint: Any | None = None
    file: Any | None = None
    log_name: str | None = None
    log_provider: str | None = None
    log_type: str | None = None
    log_type_id: int | None = None
    src_endpoint: Any | None = None
    status_code: str | None = None
    status_detail: str | None = None

class EvidenceInfo(DiscoveryResult):
    device: Any
    query_evidence: Any

class FileActivity(System):
    class ActivityId(SiblingEnum):
        CREATE = 1
        READ = 2
        UPDATE = 3
        DELETE = 4
        RENAME = 5
        SET_ATTRIBUTES = 6
        SET_SECURITY = 7
        GET_ATTRIBUTES = 8
        GET_SECURITY = 9
        ENCRYPT = 10
        DECRYPT = 11
        MOUNT = 12
        UNMOUNT = 13
        OPEN = 14
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    access_mask: int | None = None
    actor: Any
    component: str | None = None
    connection_uid: str | None = None
    create_mask: str | None = None
    file: Any
    file_diff: str | None = None
    file_result: Any | None = None

class FileHosting(Application):
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
        SYNC = 15
        UNSYNC = 16
        ACCESS_CHECK = 17
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

    access_list: list[str] | None = None
    access_mask: int | None = None
    access_result: dict[str, Any] | None = None
    actor: Any
    connection_info: Any | None = None
    dst_endpoint: Any | None = None
    expiration_time: int | None = None
    file: Any
    file_result: Any | None = None
    http_request: Any | None = None
    http_response: Any | None = None
    share: str | None = None
    share_type: str | None = None
    share_type_id: int | None = None
    src_endpoint: Any

class FileQuery(DiscoveryResult):
    file: Any

class FileRemediationActivity(RemediationActivity):
    file: Any

class Finding(BaseEvent):
    class ActivityId(SiblingEnum):
        CREATE = 1
        UPDATE = 2
        CLOSE = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

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

    class StatusId(SiblingEnum):
        NEW = 1
        IN_PROGRESS = 2
        SUPPRESSED = 3
        RESOLVED = 4
        ARCHIVED = 5
        DELETED = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_name: str | None = None
    comment: str | None = None
    confidence: str | None = None
    confidence_id: int | None = None
    confidence_score: int | None = None
    device: Any | None = None
    end_time: int | None = None
    finding_info: Any
    start_time: int | None = None
    status: str | None = None
    status_id: int | None = None
    vendor_attributes: Any | None = None

class FolderQuery(DiscoveryResult):
    folder: Any

class FtpActivity(Network):
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

    codes: list[int] | None = None
    command: str | None = None
    command_responses: list[str] | None = None
    file: Any | None = None
    name: str | None = None
    port: Any | None = None

class GroupManagement(Iam):
    class ActivityId(SiblingEnum):
        ASSIGN_PRIVILEGES = 1
        REVOKE_PRIVILEGES = 2
        ADD_USER = 3
        REMOVE_USER = 4
        DELETE = 5
        CREATE = 6
        ADD_SUBGROUP = 7
        REMOVE_SUBGROUP = 8
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    group: Any
    privileges: list[str] | None = None
    resource: Any | None = None
    subgroup: Any | None = None
    user: Any | None = None

class HttpActivity(Network):
    class ActivityId(SiblingEnum):
        CONNECT = 1
        DELETE = 2
        GET = 3
        HEAD = 4
        OPTIONS = 5
        POST = 6
        PUT = 7
        TRACE = 8
        PATCH = 9
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    file: Any | None = None
    http_cookies: list[Any] | None = None
    http_request: Any | None = None
    http_response: Any | None = None
    http_status: int | None = None

class Iam(BaseEvent):
    actor: Any | None = None
    http_request: Any | None = None
    http_response: Any | None = None
    src_endpoint: Any | None = None

class IamAnalysisFinding(Finding):
    access_analysis_result: Any | None = None
    applications: list[Any] | None = None
    identity_activity_metrics: Any | None = None
    permission_analysis_results: list[Any] | None = None
    remediation: Any | None = None
    resources: list[Any] | None = None
    user: Any | None = None

class IncidentFinding(BaseEvent):
    class ActivityId(SiblingEnum):
        CREATE = 1
        UPDATE = 2
        CLOSE = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

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

    class PriorityId(SiblingEnum):
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

    class StatusId(SiblingEnum):
        NEW = 1
        IN_PROGRESS = 2
        ON_HOLD = 3
        RESOLVED = 4
        CLOSED = 5
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class VerdictId(SiblingEnum):
        UNKNOWN = 0
        FALSE_POSITIVE = 1
        TRUE_POSITIVE = 2
        DISREGARD = 3
        SUSPICIOUS = 4
        BENIGN = 5
        TEST = 6
        INSUFFICIENT_DATA = 7
        SECURITY_RISK = 8
        MANAGED_EXTERNALLY = 9
        DUPLICATE = 10
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int
    activity_name: str | None = None
    assignee: Any | None = None
    assignee_group: Any | None = None
    attacks: list[Any] | None = None
    comment: str | None = None
    confidence: str | None = None
    confidence_id: int | None = None
    confidence_score: int | None = None
    desc: str | None = None
    end_time: int | None = None
    finding_info_list: list[Any]
    impact: str | None = None
    impact_id: int | None = None
    impact_score: int | None = None
    is_suspected_breach: bool | None = None
    priority: str | None = None
    priority_id: int | None = None
    src_url: Any | None = None
    start_time: int | None = None
    status: str | None = None
    status_id: int
    ticket: Any | None = None
    tickets: list[Any] | None = None
    vendor_attributes: Any | None = None
    verdict: str | None = None
    verdict_id: int | None = None

class InventoryInfo(Discovery):
    actor: Any | None = None
    device: Any

class JobQuery(DiscoveryResult):
    job: Any

class KernelActivity(System):
    class ActivityId(SiblingEnum):
        CREATE = 1
        READ = 2
        DELETE = 3
        INVOKE = 4
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    kernel: Any

class KernelExtensionActivity(System):
    class ActivityId(SiblingEnum):
        LOAD = 1
        UNLOAD = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    actor: Any
    driver: Any

class KernelObjectQuery(DiscoveryResult):
    kernel: Any

class MemoryActivity(System):
    class ActivityId(SiblingEnum):
        ALLOCATE_PAGE = 1
        MODIFY_PAGE = 2
        DELETE_PAGE = 3
        BUFFER_OVERFLOW = 4
        DISABLE_DEP = 5
        ENABLE_DEP = 6
        READ = 7
        WRITE = 8
        MAP_VIEW = 9
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    actual_permissions: int | None = None
    base_address: str | None = None
    process: Any
    requested_permissions: int | None = None
    size: int | None = None

class ModuleActivity(System):
    class ActivityId(SiblingEnum):
        LOAD = 1
        UNLOAD = 2
        INVOKE = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    actor: Any
    module: Any

class ModuleQuery(DiscoveryResult):
    module: Any
    process: Any

class Network(BaseEvent):
    class ObservationPointId(SiblingEnum):
        UNKNOWN = 0
        SOURCE = 1
        DESTINATION = 2
        NEITHER = 3
        BOTH = 4
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    app_name: str | None = None
    connection_info: Any | None = None
    cumulative_traffic: Any | None = None
    dst_endpoint: Any | None = None
    ja4_fingerprint_list: list[Any] | None = None
    observation_point: str | None = None
    observation_point_id: int | None = None
    proxy: Any | None = None
    src_endpoint: Any | None = None
    tls: Any | None = None
    traffic: Any | None = None

class NetworkActivity(Network):
    class ActivityId(SiblingEnum):
        OPEN = 1
        CLOSE = 2
        RESET = 3
        FAIL = 4
        REFUSE = 5
        TRAFFIC = 6
        LISTEN = 7
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    dst_endpoint: Any | None = None
    is_src_dst_assignment_known: bool | None = None
    src_endpoint: Any | None = None
    url: Any | None = None

class NetworkConnectionQuery(DiscoveryResult):
    class StateId(SiblingEnum):
        UNKNOWN = 0
        ESTABLISHED = 1
        SYN_SENT = 2
        SYN_RECV = 3
        FIN_WAIT1 = 4
        FIN_WAIT2 = 5
        TIME_WAIT = 6
        CLOSED = 7
        CLOSE_WAIT = 8
        LAST_ACK = 9
        LISTEN = 10
        CLOSING = 11
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    connection_info: Any
    process: Any
    state: str | None = None
    state_id: int

class NetworkFileActivity(Network):
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
        SYNC = 15
        UNSYNC = 16
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    actor: Any
    connection_info: Any | None = None
    dst_endpoint: Any | None = None
    expiration_time: int | None = None
    file: Any
    src_endpoint: Any

class NetworkRemediationActivity(RemediationActivity):
    connection_info: Any

class NetworksQuery(DiscoveryResult):
    network_interfaces: list[Any]

class NtpActivity(Network):
    class ActivityId(SiblingEnum):
        UNKNOWN = 0
        SYMMETRIC_ACTIVE_EXCHANGE = 1
        SYMMETRIC_PASSIVE_RESPONSE = 2
        CLIENT_SYNCHRONIZATION = 3
        SERVER_RESPONSE = 4
        BROADCAST = 5
        CONTROL = 6
        PRIVATE_USE_CASE = 7
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class StratumId(SiblingEnum):
        UNKNOWN = 0
        PRIMARY_SERVER = 1
        SECONDARY_SERVER = 2
        UNSYNCHRONIZED = 16
        RESERVED = 17
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    delay: int | None = None
    dispersion: int | None = None
    precision: int | None = None
    stratum: str | None = None
    stratum_id: int | None = None
    version: str

class OsintInventoryInfo(Discovery):
    actor: Any | None = None
    osint: list[Any]

class PatchState(Discovery):
    device: Any
    kb_article_list: list[Any] | None = None

class PeripheralActivity(System):
    class ActivityId(SiblingEnum):
        CONNECT = 1
        DISCONNECT = 2
        ENABLE = 3
        DISABLE = 4
        EJECT = 5
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    peripheral_device: Any

class PeripheralDeviceQuery(DiscoveryResult):
    peripheral_device: Any

class ProcessActivity(System):
    class ActivityId(SiblingEnum):
        LAUNCH = 1
        TERMINATE = 2
        OPEN = 3
        INJECT = 4
        SET_USER_ID = 5
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class InjectionTypeId(SiblingEnum):
        UNKNOWN = 0
        REMOTE_THREAD = 1
        LOAD_LIBRARY = 2
        QUEUE_APC = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class LaunchTypeId(SiblingEnum):
        UNKNOWN = 0
        SPAWN = 1
        FORK = 2
        EXEC = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    actor: Any | None = None
    actual_permissions: int | None = None
    exit_code: int | None = None
    injection_type: str | None = None
    injection_type_id: int | None = None
    launch_type: str | None = None
    launch_type_id: int | None = None
    module: Any | None = None
    process: Any
    requested_permissions: int | None = None

class ProcessQuery(DiscoveryResult):
    process: Any

class ProcessRemediationActivity(RemediationActivity):
    process: Any

class RdpActivity(Network):
    class ActivityId(SiblingEnum):
        INITIAL_REQUEST = 1
        INITIAL_RESPONSE = 2
        CONNECT_REQUEST = 3
        CONNECT_RESPONSE = 4
        TLS_HANDSHAKE = 5
        TRAFFIC = 6
        DISCONNECT = 7
        RECONNECT = 8
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    capabilities: list[str] | None = None
    certificate_chain: list[str] | None = None
    connection_info: Any | None = None
    device: Any | None = None
    file: Any | None = None
    identifier_cookie: str | None = None
    keyboard_info: Any | None = None
    protocol_ver: str | None = None
    remote_display: Any | None = None
    request: Any | None = None
    response: Any | None = None
    user: Any | None = None

class RemediationActivity(BaseEvent):
    class ActivityId(SiblingEnum):
        ISOLATE = 1
        EVICT = 2
        RESTORE = 3
        HARDEN = 4
        DETECT = 5
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class StatusId(SiblingEnum):
        DOES_NOT_EXIST = 3
        PARTIAL = 4
        UNSUPPORTED = 5
        ERROR = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    command_uid: str
    countermeasures: list[Any] | None = None
    remediation: Any | None = None
    scan: Any | None = None

class ScanActivity(Application):
    class ActivityId(SiblingEnum):
        STARTED = 1
        COMPLETED = 2
        CANCELLED = 3
        DURATION_VIOLATION = 4
        PAUSE_VIOLATION = 5
        ERROR = 6
        PAUSED = 7
        RESUMED = 8
        RESTARTED = 9
        DELAYED = 10
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    command_uid: str | None = None
    duration: int | None = None
    end_time: int | None = None
    num_detections: int | None = None
    num_files: int | None = None
    num_folders: int | None = None
    num_network_items: int | None = None
    num_processes: int | None = None
    num_registry_items: int | None = None
    num_resolutions: int | None = None
    num_skipped_items: int | None = None
    num_trusted_items: int | None = None
    policy: Any | None = None
    scan: Any
    schedule_uid: str | None = None
    start_time: int | None = None
    total: int | None = None

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

    actor: Any | None = None
    job: Any

class ScriptActivity(System):
    class ActivityId(SiblingEnum):
        EXECUTE = 1
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    script: Any

class SecurityFinding(BaseEvent):
    class ActivityId(SiblingEnum):
        CREATE = 1
        UPDATE = 2
        CLOSE = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

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

class ServiceQuery(DiscoveryResult):
    service: Any

class SessionQuery(DiscoveryResult):
    session: Any

class SmbActivity(Network):
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

class SoftwareInfo(Discovery):
    actor: Any | None = None
    device: Any
    package: Any | None = None
    product: Any | None = None
    sbom: Any | None = None

class SshActivity(Network):
    class ActivityId(SiblingEnum):
        OPEN = 1
        CLOSE = 2
        RESET = 3
        FAIL = 4
        REFUSE = 5
        TRAFFIC = 6
        LISTEN = 7
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class AuthTypeId(SiblingEnum):
        UNKNOWN = 0
        CERTIFICATE_BASED = 1
        GSSAPI = 2
        HOST_BASED = 3
        KEYBOARD_INTERACTIVE = 4
        PASSWORD = 5
        PUBLIC_KEY = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    auth_type: str | None = None
    auth_type_id: int | None = None
    client_hassh: Any | None = None
    file: Any | None = None
    protocol_ver: str | None = None
    server_hassh: Any | None = None

class StartupItemQuery(DiscoveryResult):
    startup_item: Any

class System(BaseEvent):
    actor: Any
    device: Any

class TunnelActivity(Network):
    class ActivityId(SiblingEnum):
        UNKNOWN = 0
        OPEN = 1
        CLOSE = 2
        RENEW = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class TunnelTypeId(SiblingEnum):
        UNKNOWN = 0
        SPLIT_TUNNEL = 1
        FULL_TUNNEL = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    activity_id: int
    connection_info: Any | None = None
    device: Any | None = None
    dst_endpoint: Any | None = None
    protocol_name: str | None = None
    session: Any | None = None
    src_endpoint: Any | None = None
    traffic: Any | None = None
    tunnel_interface: Any | None = None
    tunnel_type: str | None = None
    tunnel_type_id: int | None = None
    user: Any | None = None

class UnmannedSystems(BaseEvent):
    connection_info: Any | None = None
    dst_endpoint: Any
    proxy_endpoint: Any | None = None
    src_endpoint: Any | None = None
    tls: Any | None = None
    traffic: Any | None = None

class UserAccess(Iam):
    class ActivityId(SiblingEnum):
        ASSIGN_PRIVILEGES = 1
        REVOKE_PRIVILEGES = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    privileges: list[str]
    resource: Any | None = None
    resources: list[Any] | None = None
    user: Any

class UserInventory(Discovery):
    actor: Any | None = None
    user: Any

class UserQuery(DiscoveryResult):
    user: Any

class VulnerabilityFinding(Finding):
    resource: Any | None = None
    resources: list[Any] | None = None
    vulnerabilities: list[Any]

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

    http_request: Any
    http_response: Any | None = None
    proxy: Any | None = None
    src_endpoint: Any | None = None
    tls: Any | None = None
    web_resources: list[Any]

class WebResourcesActivity(Application):
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

    dst_endpoint: Any | None = None
    http_request: Any | None = None
    http_response: Any | None = None
    src_endpoint: Any | None = None
    tls: Any | None = None
    web_resources: list[Any]
    web_resources_result: list[Any] | None = None
