"""OCSF Objects - Type stubs (auto-generated)."""

from __future__ import annotations

from typing import Any

from typing_extensions import Self

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

class Dns(Object):
    packet_uid: int | None = None

class Entity(Object):
    name: str | None = None
    uid: str | None = None

class Resource(Entity):
    data: dict[str, Any] | None = None
    labels: list[str] | None = None
    name: str | None = None
    uid: str | None = None

class Account(Entity):
    class TypeId(SiblingEnum):
        UNKNOWN = 0
        LDAP_ACCOUNT = 1
        WINDOWS_ACCOUNT = 2
        AWS_IAM_USER = 3
        AWS_IAM_ROLE = 4
        GCP_ACCOUNT = 5
        AZURE_AD_ACCOUNT = 6
        MAC_OS_ACCOUNT = 7
        APPLE_ACCOUNT = 8
        LINUX_ACCOUNT = 9
        AWS_ACCOUNT = 10
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    labels: list[str] | None = None
    name: str | None = None
    type_id: int | None = None
    uid: str | None = None

class Actor(Object):
    app_name: str | None = None
    app_uid: str | None = None
    authorizations: list[Any] | None = None
    idp: Any | None = None
    invoked_by: str | None = None
    process: Any | None = None
    session: Any | None = None
    user: Any | None = None

class AffectedCode(Object):
    end_line: int | None = None
    file: Any
    owner: Any | None = None
    remediation: Any | None = None
    start_line: int | None = None

class AffectedPackage(Package):
    fixed_in_version: str | None = None
    package_manager: str | None = None
    path: str | None = None
    remediation: Any | None = None

class Agent(Object):
    class TypeId(SiblingEnum):
        ENDPOINT_DETECTION_AND_RESPONSE = 1
        DATA_LOSS_PREVENTION = 2
        BACKUP_RECOVERY = 3
        PERFORMANCE_MONITORING_OBSERVABILITY = 4
        VULNERABILITY_MANAGEMENT = 5
        LOG_FORWARDING = 6
        MOBILE_DEVICE_MANAGEMENT = 7
        CONFIGURATION_MANAGEMENT = 8
        REMOTE_ACCESS = 9
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    name: str | None = None
    policies: list[Any] | None = None
    type_id: int | None = None
    uid: str | None = None
    uid_alt: str | None = None
    vendor_name: str | None = None
    version: str | None = None

class Analytic(Entity):
    class TypeId(SiblingEnum):
        UNKNOWN = 0
        RULE = 1
        BEHAVIORAL = 2
        STATISTICAL = 3
        LEARNING_MLDL = 4
        FINGERPRINTING = 5
        TAGGING = 6
        KEYWORD_MATCH = 7
        REGULAR_EXPRESSIONS = 8
        EXACT_DATA_MATCH = 9
        PARTIAL_DATA_MATCH = 10
        INDEXED_DATA_MATCH = 11
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    category: str | None = None
    desc: str | None = None
    name: str | None = None
    related_analytics: list[Any] | None = None
    type_id: int
    uid: str | None = None
    version: str | None = None

class Api(Object):
    group: Any | None = None
    operation: str
    request: Any | None = None
    response: Any | None = None
    service: Any | None = None
    version: str | None = None

class Attack(Object):
    sub_technique: Any | None = None
    tactic: Any | None = None
    tactics: list[Any] | None = None
    technique: Any | None = None
    version: str | None = None

class AuthFactor(Object):
    class FactorTypeId(SiblingEnum):
        UNKNOWN = 0
        SMS = 1
        SECURITY_QUESTION = 2
        PHONE_CALL = 3
        BIOMETRIC = 4
        PUSH_NOTIFICATION = 5
        HARDWARE_TOKEN = 6
        OTP = 7
        EMAIL = 8
        U2F = 9
        WEBAUTHN = 10
        PASSWORD = 11
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    device: Any | None = None
    email_addr: Any | None = None
    factor_type: str | None = None
    factor_type_id: int
    is_hotp: bool | None = None
    is_totp: bool | None = None
    phone_number: str | None = None
    provider: str | None = None
    security_questions: list[str] | None = None

class Authorization(Object):
    decision: str | None = None
    policy: Any | None = None

class AutonomousSystem(Object):
    name: str | None = None
    number: int | None = None

class Certificate(Object):
    created_time: int | None = None
    expiration_time: int | None = None
    fingerprints: list[Any]
    is_self_signed: bool | None = None
    issuer: str
    serial_number: str
    subject: str | None = None
    uid: str | None = None
    version: str | None = None

class CisBenchmark(Object):
    cis_controls: list[Any] | None = None
    desc: str | None = None
    name: str

class CisBenchmarkResult(Object):
    desc: str | None = None
    name: str
    remediation: Any | None = None
    rule: Any | None = None

class CisControl(Object):
    desc: str | None = None
    name: str
    version: str | None = None

class CisCsc(Object):
    control: str
    version: str | None = None

class Cloud(Object):
    account: Any | None = None
    org: Any | None = None
    project_uid: str | None = None
    provider: str
    region: str | None = None
    zone: str | None = None

class Compliance(Object):
    class StatusId(SiblingEnum):
        PASS = 1
        WARNING = 2
        FAIL = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    compliance_references: list[Any] | None = None
    compliance_standards: list[Any] | None = None
    control: str | None = None
    requirements: list[str] | None = None
    standards: list[str]
    status: str | None = None
    status_code: str | None = None
    status_detail: str | None = None
    status_id: int | None = None

class Container(Object):
    hash: Any | None = None
    image: Any | None = None
    name: str | None = None
    network_driver: str | None = None
    orchestrator: str | None = None
    pod_uuid: Any | None = None
    runtime: str | None = None
    size: int | None = None
    tag: str | None = None
    uid: str | None = None

class Cve(Object):
    created_time: int | None = None
    cvss: list[Any] | None = None
    cwe: Any | None = None
    cwe_uid: str | None = None
    cwe_url: Any | None = None
    desc: str | None = None
    epss: Any | None = None
    modified_time: int | None = None
    product: Any | None = None
    references: list[str] | None = None
    title: str | None = None
    uid: str

class Cvss(Object):
    base_score: float
    depth: str | None = None
    metrics: list[Any] | None = None
    overall_score: float | None = None
    severity: str | None = None
    vector_string: str | None = None
    version: str

class Cwe(Object):
    caption: str | None = None
    src_url: Any | None = None
    uid: str

class D3fTactic(Entity):
    name: str | None = None
    src_url: Any | None = None

class D3fTechnique(Entity):
    name: str | None = None
    src_url: Any | None = None
    uid: str | None = None

class D3fend(Object):
    d3f_tactic: Any | None = None
    d3f_technique: Any | None = None
    version: str | None = None

class DataClassification(Object):
    class CategoryId(SiblingEnum):
        UNKNOWN = 0
        PERSONAL = 1
        GOVERNMENTAL = 2
        FINANCIAL = 3
        BUSINESS = 4
        MILITARY_AND_LAW_ENFORCEMENT = 5
        SECURITY = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class ConfidentialityId(SiblingEnum):
        UNKNOWN = 0
        NOT_CONFIDENTIAL = 1
        CONFIDENTIAL = 2
        SECRET = 3
        TOP_SECRET = 4
        PRIVATE = 5
        RESTRICTED = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    category: str | None = None
    category_id: int | None = None
    confidentiality: str | None = None
    confidentiality_id: int | None = None
    policy: Any | None = None

class DataSecurity(DataClassification):
    class DataLifecycleStateId(SiblingEnum):
        UNKNOWN = 0
        DATA_AT_REST = 1
        DATA_IN_TRANSIT = 2
        DATA_IN_USE = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class DetectionSystemId(SiblingEnum):
        UNKNOWN = 0
        ENDPOINT = 1
        DLP_GATEWAY = 2
        MOBILE_DEVICE_MANAGEMENT = 3
        DATA_DISCOVERY_CLASSIFICATION = 4
        SECURE_WEB_GATEWAY = 5
        SECURE_EMAIL_GATEWAY = 6
        DIGITAL_RIGHTS_MANAGEMENT = 7
        CLOUD_ACCESS_SECURITY_BROKER = 8
        DATABASE_ACTIVITY_MONITORING = 9
        APPLICATION_LEVEL_DLP = 10
        DEVELOPER_SECURITY = 11
        DATA_SECURITY_POSTURE_MANAGEMENT = 12
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    data_lifecycle_state: str | None = None
    data_lifecycle_state_id: int | None = None
    detection_pattern: str | None = None
    detection_system: str | None = None
    detection_system_id: int | None = None
    pattern_match: str | None = None
    policy: Any | None = None

class Database(Entity):
    class TypeId(SiblingEnum):
        UNKNOWN = 0
        RELATIONAL = 1
        NETWORK = 2
        OBJECT_ORIENTED = 3
        CENTRALIZED = 4
        OPERATIONAL = 5
        NOSQL = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    created_time: int | None = None
    desc: str | None = None
    groups: list[Any] | None = None
    modified_time: int | None = None
    name: str | None = None
    size: int | None = None
    type_id: int
    uid: str | None = None

class Databucket(Entity):
    class TypeId(SiblingEnum):
        UNKNOWN = 0
        S3 = 1
        AZURE_BLOB = 2
        GCP_BUCKET = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    created_time: int | None = None
    desc: str | None = None
    file: Any | None = None
    groups: list[Any] | None = None
    modified_time: int | None = None
    name: str | None = None
    size: int | None = None
    type_id: int
    uid: str | None = None

class DceRpc(Object):
    command: str | None = None
    command_response: str | None = None
    flags: list[str]
    opnum: int | None = None
    rpc_interface: Any

class Device(Endpoint):
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

    class TypeId(SiblingEnum):
        UNKNOWN = 0
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    autoscale_uid: str | None = None
    boot_time: int | None = None
    created_time: int | None = None
    desc: str | None = None
    domain: str | None = None
    first_seen_time: int | None = None
    groups: list[Any] | None = None
    hostname: Any | None = None
    hypervisor: str | None = None
    image: Any | None = None
    imei: str | None = None
    ip: Any | None = None
    is_compliant: bool | None = None
    is_managed: bool | None = None
    is_personal: bool | None = None
    is_trusted: bool | None = None
    last_seen_time: int | None = None
    location: Any | None = None
    modified_time: int | None = None
    name: str | None = None
    network_interfaces: list[Any] | None = None
    org: Any | None = None
    region: str | None = None
    risk_level: str | None = None
    risk_level_id: int | None = None
    risk_score: int | None = None
    subnet: Any | None = None
    type_id: int
    uid: str | None = None
    uid_alt: str | None = None

class DeviceHwInfo(Object):
    bios_date: str | None = None
    bios_manufacturer: str | None = None
    bios_ver: str | None = None
    chassis: str | None = None
    cpu_bits: int | None = None
    cpu_cores: int | None = None
    cpu_count: int | None = None
    cpu_speed: int | None = None
    cpu_type: str | None = None
    desktop_display: Any | None = None
    keyboard_info: Any | None = None
    ram_size: int | None = None
    serial_number: str | None = None

class DigitalSignature(Object):
    class AlgorithmId(SiblingEnum):
        UNKNOWN = 0
        DSA = 1
        RSA = 2
        ECDSA = 3
        AUTHENTICODE = 4
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class StateId(SiblingEnum):
        VALID = 1
        EXPIRED = 2
        REVOKED = 3
        SUSPENDED = 4
        PENDING = 5
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    algorithm: str | None = None
    algorithm_id: int
    certificate: Any | None = None
    created_time: int | None = None
    developer_uid: str | None = None
    digest: Any | None = None
    state: str | None = None
    state_id: int | None = None

class Display(Object):
    color_depth: int | None = None
    physical_height: int | None = None
    physical_orientation: int | None = None
    physical_width: int | None = None
    scale_factor: int | None = None

class DnsAnswer(Dns):
    flag_ids: list[int] | None = None
    flags: list[str] | None = None
    rdata: str
    ttl: int | None = None

class DnsQuery(Dns):
    class OpcodeId(SiblingEnum):
        QUERY = 0
        INVERSE_QUERY = 1
        STATUS = 2
        RESERVED = 3
        NOTIFY = 4
        UPDATE = 5
        DSO_MESSAGE = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    hostname: Any
    opcode: str | None = None
    opcode_id: int | None = None

class DomainContact(Object):
    class TypeId(SiblingEnum):
        REGISTRANT = 1
        ADMINISTRATIVE = 2
        TECHNICAL = 3
        BILLING = 4
        ABUSE = 5
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    email_addr: Any | None = None
    location: Any | None = None
    name: str | None = None
    phone_number: str | None = None
    type_id: int
    uid: str | None = None

class Email(Object):
    cc: list[Any] | None = None
    delivered_to: Any | None = None
    message_uid: str | None = None
    raw_header: str | None = None
    reply_to: Any | None = None
    size: int | None = None
    smtp_from: Any | None = None
    smtp_to: list[Any] | None = None
    subject: str | None = None
    to: list[Any]
    uid: str | None = None
    x_originating_ip: list[Any] | None = None

class EmailAuth(Object):
    dkim: str | None = None
    dkim_domain: str | None = None
    dkim_signature: str | None = None
    dmarc: str | None = None
    dmarc_override: str | None = None
    dmarc_policy: str | None = None
    spf: str | None = None

class Endpoint(Entity):
    class TypeId(SiblingEnum):
        SERVER = 1
        DESKTOP = 2
        LAPTOP = 3
        TABLET = 4
        MOBILE = 5
        VIRTUAL = 6
        IOT = 7
        BROWSER = 8
        FIREWALL = 9
        SWITCH = 10
        HUB = 11
        ROUTER = 12
        IDS = 13
        IPS = 14
        LOAD_BALANCER = 15
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    agent_list: list[Any] | None = None
    domain: str | None = None
    hostname: Any | None = None
    hw_info: Any | None = None
    instance_uid: str | None = None
    interface_name: str | None = None
    interface_uid: str | None = None
    ip: Any | None = None
    location: Any | None = None
    mac: Any | None = None
    name: str | None = None
    os: Any | None = None
    owner: Any | None = None
    subnet_uid: str | None = None
    type_id: int | None = None
    uid: str | None = None
    vlan_uid: str | None = None
    vpc_uid: str | None = None
    zone: str | None = None

class EndpointConnection(Object):
    code: int | None = None
    network_endpoint: Any | None = None

class Enrichment(Object):
    created_time: int | None = None
    data: dict[str, Any]
    desc: str | None = None
    name: str
    provider: str | None = None
    reputation: Any | None = None
    short_desc: str | None = None
    src_url: Any | None = None
    value: str

class Epss(Object):
    created_time: int | None = None
    percentile: float | None = None
    score: str
    version: str | None = None

class Evidences(Object):
    actor: Any | None = None
    api: Any | None = None
    connection_info: Any | None = None
    container: Any | None = None
    data: dict[str, Any] | None = None
    database: Any | None = None
    databucket: Any | None = None
    device: Any | None = None
    dst_endpoint: Any | None = None
    email: Any | None = None
    file: Any | None = None
    job: Any | None = None
    process: Any | None = None
    query: Any | None = None
    src_endpoint: Any | None = None
    url: Any | None = None
    user: Any | None = None

class Extension(Entity):
    name: str
    uid: str
    version: str

class Feature(Entity):
    name: str | None = None
    uid: str | None = None
    version: str | None = None

class File(Entity):
    class ConfidentialityId(SiblingEnum):
        UNKNOWN = 0
        NOT_CONFIDENTIAL = 1
        CONFIDENTIAL = 2
        SECRET = 3
        TOP_SECRET = 4
        PRIVATE = 5
        RESTRICTED = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class TypeId(SiblingEnum):
        UNKNOWN = 0
        REGULAR_FILE = 1
        FOLDER = 2
        CHARACTER_DEVICE = 3
        BLOCK_DEVICE = 4
        LOCAL_SOCKET = 5
        NAMED_PIPE = 6
        SYMBOLIC_LINK = 7
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    accessed_time: int | None = None
    accessor: Any | None = None
    attributes: int | None = None
    company_name: str | None = None
    confidentiality: str | None = None
    confidentiality_id: int | None = None
    created_time: int | None = None
    creator: Any | None = None
    desc: str | None = None
    ext: str | None = None
    hashes: list[Any] | None = None
    is_system: bool | None = None
    mime_type: str | None = None
    modified_time: int | None = None
    modifier: Any | None = None
    name: Any
    owner: Any | None = None
    parent_folder: str | None = None
    path: str | None = None
    product: Any | None = None
    security_descriptor: str | None = None
    signature: Any | None = None
    size: int | None = None
    type_id: int
    uid: str | None = None
    version: str | None = None
    xattributes: Any | None = None

class Finding(Object):
    created_time: int | None = None
    desc: str | None = None
    first_seen_time: int | None = None
    last_seen_time: int | None = None
    modified_time: int | None = None
    product_uid: str | None = None
    related_events: list[Any] | None = None
    remediation: Any | None = None
    src_url: Any | None = None
    supporting_data: dict[str, Any] | None = None
    title: str
    types: list[str] | None = None
    uid: str

class FindingInfo(Object):
    analytic: Any | None = None
    attacks: list[Any] | None = None
    created_time: int | None = None
    data_sources: list[str] | None = None
    desc: str | None = None
    first_seen_time: int | None = None
    kill_chain: list[Any] | None = None
    last_seen_time: int | None = None
    modified_time: int | None = None
    product_uid: str | None = None
    related_analytics: list[Any] | None = None
    related_events: list[Any] | None = None
    src_url: Any | None = None
    title: str
    types: list[str] | None = None
    uid: str

class Fingerprint(Object):
    class AlgorithmId(SiblingEnum):
        UNKNOWN = 0
        MD5 = 1
        SHA_1 = 2
        SHA_256 = 3
        SHA_512 = 4
        CTPH = 5
        TLSH = 6
        QUICKXORHASH = 7
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    algorithm: str | None = None
    algorithm_id: int
    value: Any

class FirewallRule(Rule):
    condition: str | None = None
    duration: int | None = None
    match_details: list[str] | None = None
    match_location: str | None = None
    rate_limit: int | None = None
    sensitivity: str | None = None

class Group(Entity):
    desc: str | None = None
    domain: str | None = None
    name: str | None = None
    privileges: list[str] | None = None
    uid: str | None = None

class Hassh(Object):
    algorithm: str | None = None
    fingerprint: Any

class HttpCookie(Object):
    domain: str | None = None
    expiration_time: int | None = None
    http_only: bool | None = None
    is_http_only: bool | None = None
    is_secure: bool | None = None
    name: str
    path: str | None = None
    samesite: str | None = None
    secure: bool | None = None
    value: str

class HttpHeader(Object):
    name: str
    value: str

class HttpRequest(Object):
    args: str | None = None
    http_headers: list[Any] | None = None
    http_method: str | None = None
    length: int | None = None
    referrer: str | None = None
    uid: str | None = None
    url: Any | None = None
    user_agent: str | None = None
    version: str | None = None
    x_forwarded_for: list[Any] | None = None

class HttpResponse(Object):
    code: int
    content_type: str | None = None
    http_headers: list[Any] | None = None
    latency: int | None = None
    length: int | None = None
    message: str | None = None
    status: str | None = None

class Idp(Entity):
    name: str | None = None
    uid: str | None = None

class Image(Entity):
    labels: list[str] | None = None
    name: str | None = None
    path: str | None = None
    tag: str | None = None
    uid: str

class Ja4Fingerprint(Object):
    class TypeId(SiblingEnum):
        UNKNOWN = 0
        JA4 = 1
        JA4SERVER = 2
        JA4HTTP = 3
        JA4LATENCY = 4
        JA4X509 = 5
        JA4SSH = 6
        JA4TCP = 7
        JA4TCPSERVER = 8
        JA4TCPSCAN = 9
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    section_a: str | None = None
    section_b: str | None = None
    section_c: str | None = None
    section_d: str | None = None
    type_id: int
    value: str

class Job(Object):
    class RunStateId(SiblingEnum):
        UNKNOWN = 0
        READY = 1
        QUEUED = 2
        RUNNING = 3
        STOPPED = 4
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    cmd_line: str | None = None
    created_time: int | None = None
    desc: str | None = None
    file: Any
    last_run_time: int | None = None
    name: str
    next_run_time: int | None = None
    run_state: str | None = None
    run_state_id: int | None = None
    user: Any | None = None

class KbArticle(Object):
    class InstallStateId(SiblingEnum):
        UNKNOWN = 0
        INSTALLED = 1
        NOT_INSTALLED = 2
        INSTALLED_PENDING_REBOOT = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    avg_timespan: Any | None = None
    bulletin: str | None = None
    classification: str | None = None
    created_time: int | None = None
    install_state: str | None = None
    install_state_id: int | None = None
    is_superseded: bool | None = None
    os: Any | None = None
    product: Any | None = None
    severity: str | None = None
    size: int | None = None
    src_url: Any | None = None
    title: str | None = None
    uid: str

class Kernel(Object):
    class TypeId(SiblingEnum):
        SHARED_MUTEX = 1
        SYSTEM_CALL = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    is_system: bool | None = None
    name: str
    path: str | None = None
    system_call: str | None = None
    type_id: int

class KernelDriver(Object):
    file: Any

class KeyboardInfo(Object):
    function_keys: int | None = None
    ime: str | None = None
    keyboard_layout: str | None = None
    keyboard_subtype: int | None = None
    keyboard_type: str | None = None

class KillChainPhase(Object):
    class PhaseId(SiblingEnum):
        UNKNOWN = 0
        RECONNAISSANCE = 1
        WEAPONIZATION = 2
        DELIVERY = 3
        EXPLOITATION = 4
        INSTALLATION = 5
        COMMAND_CONTROL = 6
        ACTIONS_ON_OBJECTIVES = 7
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    phase: str | None = None
    phase_id: int

class LdapPerson(Object):
    cost_center: str | None = None
    created_time: int | None = None
    deleted_time: int | None = None
    email_addrs: list[Any] | None = None
    employee_uid: str | None = None
    given_name: str | None = None
    hire_time: int | None = None
    job_title: str | None = None
    labels: list[str] | None = None
    last_login_time: int | None = None
    ldap_cn: str | None = None
    ldap_dn: str | None = None
    leave_time: int | None = None
    location: Any | None = None
    manager: Any | None = None
    modified_time: int | None = None
    office_location: str | None = None
    surname: str | None = None

class LoadBalancer(Entity):
    classification: str | None = None
    code: int | None = None
    dst_endpoint: Any | None = None
    endpoint_connections: list[Any] | None = None
    error_message: str | None = None
    ip: Any | None = None
    message: str | None = None
    metrics: list[Any] | None = None
    name: str | None = None
    status_detail: str | None = None
    uid: str | None = None

class Location(Object):
    city: str | None = None
    continent: str | None = None
    coordinates: list[float] | None = None
    country: str | None = None
    desc: str | None = None
    geohash: str | None = None
    is_on_premises: bool | None = None
    isp: str | None = None
    lat: float | None = None
    long: float | None = None
    postal_code: str | None = None
    provider: str | None = None
    region: str | None = None

class Logger(Entity):
    device: Any | None = None
    log_level: str | None = None
    log_name: str | None = None
    log_provider: str | None = None
    log_version: str | None = None
    logged_time: int | None = None
    name: str | None = None
    product: Any | None = None
    transmit_time: int | None = None
    uid: str | None = None
    version: str | None = None

class Malware(Entity):
    classification_ids: list[int]
    classifications: list[str] | None = None
    cves: list[Any] | None = None
    name: str | None = None
    path: str | None = None
    provider: str | None = None
    uid: str | None = None

class ManagedEntity(Entity):
    class TypeId(SiblingEnum):
        DEVICE = 1
        USER = 2
        GROUP = 3
        ORGANIZATION = 4
        POLICY = 5
        EMAIL = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    data: dict[str, Any] | None = None
    device: Any | None = None
    email: Any | None = None
    group: Any | None = None
    name: str | None = None
    org: Any | None = None
    policy: Any | None = None
    type_id: int | None = None
    uid: str | None = None
    user: Any | None = None
    version: str | None = None

class Metadata(Object):
    correlation_uid: str | None = None
    event_code: str | None = None
    extension: Any | None = None
    extensions: list[Any] | None = None
    labels: list[str] | None = None
    log_level: str | None = None
    log_name: str | None = None
    log_provider: str | None = None
    log_version: str | None = None
    logged_time: int | None = None
    loggers: list[Any] | None = None
    modified_time: int | None = None
    original_time: str | None = None
    processed_time: int | None = None
    product: Any
    profiles: list[str] | None = None
    sequence: int | None = None
    tenant_uid: str | None = None
    uid: str | None = None
    version: str

class Metric(Object):
    name: str
    value: str

class Module(Object):
    class LoadTypeId(SiblingEnum):
        STANDARD = 1
        NON_STANDARD = 2
        SHELLCODE = 3
        MAPPED = 4
        NONSTANDARD_BACKED = 5
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    base_address: str | None = None
    file: Any | None = None
    function_name: str | None = None
    load_type: str | None = None
    load_type_id: int
    start_address: str | None = None

class NetworkConnectionInfo(Object):
    class BoundaryId(SiblingEnum):
        UNKNOWN = 0
        LOCALHOST = 1
        INTERNAL = 2
        EXTERNAL = 3
        SAME_VPC = 4
        INTERNETVPC_GATEWAY = 5
        VIRTUAL_PRIVATE_GATEWAY = 6
        INTRA_REGION_VPC = 7
        INTER_REGION_VPC = 8
        LOCAL_GATEWAY = 9
        GATEWAY_VPC = 10
        INTERNET_GATEWAY = 11
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class DirectionId(SiblingEnum):
        UNKNOWN = 0
        INBOUND = 1
        OUTBOUND = 2
        LATERAL = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    class ProtocolVerId(SiblingEnum):
        UNKNOWN = 0
        INTERNET_PROTOCOL_VERSION_4_IPV4 = 4
        INTERNET_PROTOCOL_VERSION_6_IPV6 = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    boundary: str | None = None
    boundary_id: int | None = None
    direction: str | None = None
    direction_id: int
    protocol_name: str | None = None
    protocol_num: int | None = None
    protocol_ver: str | None = None
    protocol_ver_id: int | None = None
    session: Any | None = None
    tcp_flags: int | None = None
    uid: str | None = None

class NetworkEndpoint(Endpoint):
    class TypeId(SiblingEnum):
        UNKNOWN = 0
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    autonomous_system: Any | None = None
    intermediate_ips: list[Any] | None = None
    port: Any | None = None
    proxy_endpoint: Any | None = None
    svc_name: str | None = None

class NetworkInterface(Entity):
    class TypeId(SiblingEnum):
        UNKNOWN = 0
        WIRED = 1
        WIRELESS = 2
        MOBILE = 3
        TUNNEL = 4
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    hostname: Any | None = None
    ip: Any | None = None
    mac: Any | None = None
    name: str | None = None
    namespace: str | None = None
    subnet_prefix: int | None = None
    type_id: int
    uid: str | None = None

class NetworkProxy(NetworkEndpoint):
    pass

class NetworkTraffic(Object):
    bytes: int | None = None
    bytes_in: int | None = None
    bytes_out: int | None = None
    chunks: int | None = None
    chunks_in: int | None = None
    chunks_out: int | None = None
    packets: int | None = None
    packets_in: int | None = None
    packets_out: int | None = None

class Object(OCSFBaseModel):
    pass

class Observable(Object):
    class TypeId(SiblingEnum):
        UNKNOWN = 0
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    name: str
    reputation: Any | None = None
    type_id: int
    value: str | None = None

class Organization(Entity):
    name: str | None = None
    ou_name: str | None = None
    ou_uid: str | None = None
    uid: str | None = None

class Os(Object):
    class TypeId(SiblingEnum):
        WINDOWS = 100
        WINDOWS_MOBILE = 101
        LINUX = 200
        ANDROID = 201
        MACOS = 300
        IOS = 301
        IPADOS = 302
        SOLARIS = 400
        AIX = 401
        HP_UX = 402
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    build: str | None = None
    country: str | None = None
    cpe_name: str | None = None
    cpu_bits: int | None = None
    edition: str | None = None
    lang: str | None = None
    name: str
    sp_name: str | None = None
    sp_ver: int | None = None
    type_id: int
    version: str | None = None

class Osint(Entity):
    class TypeId(SiblingEnum):
        UNKNOWN = 0
        IP_ADDRESS = 1
        DOMAIN = 2
        HOSTNAME = 3
        HASH = 4
        URL = 5
        USER_AGENT = 6
        DIGITAL_CERTIFICATE = 7
        EMAIL = 8
        EMAIL_ADDRESS = 9
        VULNERABILITY = 10
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

    answers: list[Any] | None = None
    attacks: list[Any] | None = None
    autonomous_system: Any | None = None
    comment: str | None = None
    confidence: str | None = None
    confidence_id: int | None = None
    email: Any | None = None
    email_auth: Any | None = None
    kill_chain: list[Any] | None = None
    location: Any | None = None
    signatures: list[Any] | None = None
    src_url: Any | None = None
    subdomains: list[str] | None = None
    tlp: str | None = None
    type_id: int
    value: str
    vendor_name: str | None = None
    vulnerabilities: list[Any] | None = None
    whois: Any | None = None

class Package(Object):
    class TypeId(SiblingEnum):
        APPLICATION = 1
        OPERATING_SYSTEM = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    architecture: str | None = None
    cpe_name: str | None = None
    epoch: int | None = None
    hash: Any | None = None
    license: str | None = None
    name: str
    purl: str | None = None
    release: str | None = None
    type_id: int | None = None
    vendor_name: str | None = None
    version: str

class PeripheralDevice(Entity):
    model: str | None = None
    name: str
    serial_number: str | None = None
    uid: str | None = None
    vendor_name: str | None = None

class Policy(Entity):
    desc: str | None = None
    group: Any | None = None
    is_applied: bool | None = None
    name: str | None = None
    uid: str | None = None
    version: str | None = None

class Process(Entity):
    class IntegrityId(SiblingEnum):
        UNKNOWN = 0
        UNTRUSTED = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4
        SYSTEM = 5
        PROTECTED = 6
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    cmd_line: str | None = None
    created_time: int | None = None
    file: Any | None = None
    integrity: str | None = None
    integrity_id: int | None = None
    lineage: list[str] | None = None
    loaded_modules: list[str] | None = None
    name: Any | None = None
    parent_process: Any | None = None
    pid: int | None = None
    sandbox: str | None = None
    session: Any | None = None
    terminated_time: int | None = None
    tid: int | None = None
    uid: str | None = None
    user: Any | None = None
    xattributes: Any | None = None

class Product(Entity):
    cpe_name: str | None = None
    feature: Any | None = None
    lang: str | None = None
    name: str | None = None
    path: str | None = None
    uid: str | None = None
    url_string: Any | None = None
    vendor_name: str
    version: str | None = None

class QueryInfo(Entity):
    bytes: int | None = None
    data: dict[str, Any] | None = None
    name: str | None = None
    query_string: str
    query_time: int | None = None
    uid: str | None = None

class RelatedEvent(Object):
    attacks: list[Any] | None = None
    kill_chain: list[Any] | None = None
    observables: list[Any] | None = None
    product_uid: str | None = None
    type_name: str | None = None
    type_uid: int | None = None
    uid: str

class Remediation(Object):
    desc: str
    kb_article_list: list[Any] | None = None
    kb_articles: list[str] | None = None
    references: list[str] | None = None

class Reputation(Object):
    class ScoreId(SiblingEnum):
        UNKNOWN = 0
        VERY_SAFE = 1
        SAFE = 2
        PROBABLY_SAFE = 3
        LEANS_SAFE = 4
        MAY_NOT_BE_SAFE = 5
        EXERCISE_CAUTION = 6
        SUSPICIOUSRISKY = 7
        POSSIBLY_MALICIOUS = 8
        PROBABLY_MALICIOUS = 9
        MALICIOUS = 10
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    base_score: float
    provider: str | None = None
    score: str | None = None
    score_id: int

class Request(Object):
    containers: list[Any] | None = None
    data: dict[str, Any] | None = None
    flags: list[str] | None = None
    uid: str

class ResourceDetails(Resource):
    agent_list: list[Any] | None = None
    cloud_partition: str | None = None
    criticality: str | None = None
    group: Any | None = None
    namespace: str | None = None
    owner: Any | None = None
    region: str | None = None
    version: str | None = None

class Response(Object):
    code: int | None = None
    containers: list[Any] | None = None
    data: dict[str, Any] | None = None
    error: str | None = None
    error_message: str | None = None
    flags: list[str] | None = None
    message: str | None = None

class RpcInterface(Object):
    ack_reason: int | None = None
    ack_result: int | None = None
    uuid: Any
    version: str

class Rule(Entity):
    category: str | None = None
    desc: str | None = None
    name: str | None = None
    uid: str | None = None
    version: str | None = None

class San(Object):
    name: str

class Scan(Entity):
    class TypeId(SiblingEnum):
        UNKNOWN = 0
        MANUAL = 1
        SCHEDULED = 2
        UPDATED_CONTENT = 3
        QUARANTINED_ITEMS = 4
        ATTACHED_MEDIA = 5
        USER_LOGON = 6
        ELAM = 7
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    name: str | None = None
    type_id: int
    uid: str | None = None

class SecurityState(Object):
    class StateId(SiblingEnum):
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
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    state: str | None = None
    state_id: int | None = None

class Service(Entity):
    labels: list[str] | None = None
    name: str | None = None
    uid: str | None = None
    version: str | None = None

class Session(Object):
    count: int | None = None
    created_time: int | None = None
    credential_uid: str | None = None
    expiration_reason: str | None = None
    expiration_time: int | None = None
    is_mfa: bool | None = None
    is_remote: bool | None = None
    is_vpn: bool | None = None
    issuer: str | None = None
    terminal: str | None = None
    uid: str | None = None
    uid_alt: str | None = None
    uuid: Any | None = None

class SubTechnique(Entity):
    name: str | None = None
    src_url: Any | None = None
    uid: str | None = None

class Table(Entity):
    created_time: int | None = None
    desc: str | None = None
    groups: list[Any] | None = None
    modified_time: int | None = None
    name: str | None = None
    size: int | None = None
    uid: str | None = None

class Tactic(Entity):
    name: str | None = None
    src_url: Any | None = None
    uid: str | None = None

class Technique(Entity):
    name: str | None = None
    src_url: Any | None = None
    uid: str | None = None

class Ticket(Object):
    class TypeId(SiblingEnum):
        UNKNOWN = 0
        INTERNAL = 1
        EXTERNAL = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    src_url: Any | None = None
    title: str | None = None
    type_id: int | None = None
    uid: str | None = None

class Timespan(Object):
    class TypeId(SiblingEnum):
        UNKNOWN = 0
        MILLISECONDS = 1
        SECONDS = 2
        MINUTES = 3
        HOURS = 4
        DAYS = 5
        WEEKS = 6
        MONTHS = 7
        YEARS = 8
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    duration: int | None = None
    duration_days: int | None = None
    duration_hours: int | None = None
    duration_mins: int | None = None
    duration_months: int | None = None
    duration_secs: int | None = None
    duration_weeks: int | None = None
    duration_years: int | None = None
    type_id: int | None = None

class Tls(Object):
    alert: int | None = None
    certificate: Any | None = None
    certificate_chain: list[str] | None = None
    cipher: str | None = None
    client_ciphers: list[str] | None = None
    extension_list: list[Any] | None = None
    handshake_dur: int | None = None
    ja3_hash: Any | None = None
    ja3s_hash: Any | None = None
    key_length: int | None = None
    sans: list[Any] | None = None
    server_ciphers: list[str] | None = None
    sni: str | None = None
    tls_extension_list: list[Any] | None = None
    version: str

class TlsExtension(Object):
    class TypeId(SiblingEnum):
        SERVER_NAME = 0
        MAXIMUM_FRAGMENT_LENGTH = 1
        STATUS_REQUEST = 5
        SUPPORTED_GROUPS = 10
        SIGNATURE_ALGORITHMS = 13
        USE_SRTP = 14
        HEARTBEAT = 15
        APPLICATION_LAYER_PROTOCOL_NEGOTIATION = 16
        SIGNED_CERTIFICATE_TIMESTAMP = 18
        CLIENT_CERTIFICATE_TYPE = 19
        SERVER_CERTIFICATE_TYPE = 20
        PADDING = 21
        PRE_SHARED_KEY = 41
        EARLY_DATA = 42
        SUPPORTED_VERSIONS = 43
        COOKIE = 44
        PSK_KEY_EXCHANGE_MODES = 45
        CERTIFICATE_AUTHORITIES = 47
        OID_FILTERS = 48
        POST_HANDSHAKE_AUTH = 49
        SIGNATURE_ALGORITHMS_CERT = 50
        KEY_SHARE = 51
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    data: dict[str, Any] | None = None
    type_id: int

class Url(Object):
    categories: list[str] | None = None
    category_ids: list[int] | None = None
    domain: str | None = None
    hostname: Any | None = None
    path: str | None = None
    port: Any | None = None
    query_string: str | None = None
    resource_type: str | None = None
    scheme: str | None = None
    subdomain: str | None = None
    url_string: Any | None = None

class User(Entity):
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

    class TypeId(SiblingEnum):
        UNKNOWN = 0
        USER = 1
        ADMIN = 2
        SYSTEM = 3
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    account: Any | None = None
    credential_uid: str | None = None
    domain: str | None = None
    email_addr: Any | None = None
    full_name: str | None = None
    groups: list[Any] | None = None
    ldap_person: Any | None = None
    name: Any | None = None
    org: Any | None = None
    risk_level: str | None = None
    risk_level_id: int | None = None
    risk_score: int | None = None
    type_id: int | None = None
    uid: str | None = None
    uid_alt: str | None = None

class Vulnerability(Object):
    affected_code: list[Any] | None = None
    affected_packages: list[Any] | None = None
    cve: Any | None = None
    cwe: Any | None = None
    desc: str | None = None
    first_seen_time: int | None = None
    fix_available: bool | None = None
    is_exploit_available: bool | None = None
    is_fix_available: bool | None = None
    kb_article_list: list[Any] | None = None
    kb_articles: list[str] | None = None
    last_seen_time: int | None = None
    packages: list[Any] | None = None
    references: list[str] | None = None
    related_vulnerabilities: list[str] | None = None
    remediation: Any | None = None
    severity: str | None = None
    title: str | None = None
    vendor_name: str | None = None

class WebResource(Resource):
    data: dict[str, Any] | None = None
    desc: str | None = None
    name: str | None = None
    uid: str | None = None
    url_string: Any | None = None

class Whois(Object):
    class DnssecStatusId(SiblingEnum):
        UNKNOWN = 0
        SIGNED = 1
        UNSIGNED = 2
        OTHER = 99
        @property
        def label(self) -> str: ...
        @classmethod
        def from_label(cls, label: str) -> Self: ...

    autonomous_system: Any | None = None
    created_time: int | None = None
    dnssec_status: str | None = None
    dnssec_status_id: int | None = None
    domain: str | None = None
    domain_contacts: list[Any] | None = None
    email_addr: Any | None = None
    last_seen_time: int | None = None
    name_servers: list[str] | None = None
    phone_number: str | None = None
    registrar: str | None = None
    status: str | None = None
    subdomains: list[str] | None = None
    subnet: Any | None = None
