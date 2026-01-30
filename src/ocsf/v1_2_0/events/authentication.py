"""Authentication event class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_2_0.enums.authentication_activity_id import AuthenticationActivityId
    from ocsf.v1_2_0.objects.actor import Actor
    from ocsf.v1_2_0.objects.auth_factor import AuthFactor
    from ocsf.v1_2_0.objects.certificate import Certificate
    from ocsf.v1_2_0.objects.enrichment import Enrichment
    from ocsf.v1_2_0.objects.http_request import HttpRequest
    from ocsf.v1_2_0.objects.metadata import Metadata
    from ocsf.v1_2_0.objects.network_endpoint import NetworkEndpoint
    from ocsf.v1_2_0.objects.object import Object
    from ocsf.v1_2_0.objects.observable import Observable
    from ocsf.v1_2_0.objects.process import Process
    from ocsf.v1_2_0.objects.service import Service
    from ocsf.v1_2_0.objects.session import Session
    from ocsf.v1_2_0.objects.user import User


class Authentication(OCSFBaseModel):
    """Authentication events report authentication session activities such as user attempts a logon or logoff, successfully or otherwise.

    OCSF Class UID: 2
    Category:

    See: https://schema.ocsf.io/1.2.0/classes/authentication
    """

    # Nested Enums for sibling attribute pairs
    class SeverityId(SiblingEnum):
        """<p>The normalized identifier of the event/finding severity.</p>The normalized severity is a measurement the effort and expense required to manage and resolve an event or incident. Smaller numerical values represent lower impact events, and larger numerical values represent higher impact events.

        OCSF Attribute: severity_id
        """

        UNKNOWN = 0
        INFORMATIONAL = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4
        CRITICAL = 5
        FATAL = 6
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Informational",
                2: "Low",
                3: "Medium",
                4: "High",
                5: "Critical",
                6: "Fatal",
                99: "Other",
            }

    class StatusId(SiblingEnum):
        """The normalized identifier of the event status.

        OCSF Attribute: status_id
        """

        UNKNOWN = 0
        SUCCESS = 1
        FAILURE = 2
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Success",
                2: "Failure",
                99: "Other",
            }

    class AuthProtocolId(SiblingEnum):
        """The normalized identifier of the authentication protocol used to create the user session.

        OCSF Attribute: auth_protocol_id
        """

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

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "NTLM",
                2: "Kerberos",
                3: "Digest",
                4: "OpenID",
                5: "SAML",
                6: "OAUTH 2.0",
                7: "PAP",
                8: "CHAP",
                9: "EAP",
                10: "RADIUS",
                99: "Other",
            }

    class LogonTypeId(SiblingEnum):
        """The normalized logon type identifier.

        OCSF Attribute: logon_type_id
        """

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

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "System",
                2: "Interactive",
                3: "Network",
                4: "Batch",
                5: "OS Service",
                7: "Unlock",
                8: "Network Cleartext",
                9: "New Credentials",
                10: "Remote Interactive",
                11: "Cached Interactive",
                12: "Cached Remote Interactive",
                13: "Cached Unlock",
                99: "Other",
            }

    # Class identifiers
    class_uid: Literal[2] = Field(
        default=2, description="The unique identifier of the event class."
    )
    category_uid: Literal[0] = Field(default=0, description="The category unique identifier.")
    metadata: Metadata = Field(
        ..., description="The metadata associated with the event or a finding."
    )
    severity_id: SeverityId = Field(
        ...,
        description="<p>The normalized identifier of the event/finding severity.</p>The normalized severity is a measurement the effort and expense required to manage and resolve an event or incident. Smaller numerical values represent lower impact events, and larger numerical values represent higher impact events.",
    )
    user: User = Field(..., description="The subject (user/role or account) to authenticate.")
    activity_id: AuthenticationActivityId | None = Field(
        default=None,
        description="The normalized identifier of the activity that triggered the event.",
    )
    actor: Actor | None = Field(
        default=None, description="The actor that requested the authentication."
    )
    auth_factors: list[AuthFactor] | None = Field(
        default=None,
        description="Describes a category of methods used for identity verification in an authentication attempt.",
    )
    auth_protocol: str | None = Field(
        default=None,
        description="The authentication protocol as defined by the caption of 'auth_protocol_id'. In the case of 'Other', it is defined by the event source. [Recommended]",
    )
    auth_protocol_id: AuthProtocolId | None = Field(
        default=None,
        description="The normalized identifier of the authentication protocol used to create the user session. [Recommended]",
    )
    certificate: Certificate | None = Field(
        default=None,
        description="The certificate associated with the authentication or pre-authentication (Kerberos). [Recommended]",
    )
    dst_endpoint: NetworkEndpoint | None = Field(
        default=None,
        description="The endpoint to which the authentication was targeted. [Recommended]",
    )
    enrichments: list[Enrichment] | None = Field(
        default=None,
        description='The additional information from an external data source, which is associated with the event or a finding. For example add location information for the IP address in the DNS answers:</p><code>[{"name": "answers.ip", "value": "92.24.47.250", "type": "location", "data": {"city": "Socotra", "continent": "Asia", "coordinates": [-25.4153, 17.0743], "country": "YE", "desc": "Yemen"}}]</code>',
    )
    http_request: HttpRequest | None = Field(
        default=None, description="Details about the underlying HTTP request."
    )
    include: str | None = Field(default=None, description="")
    is_cleartext: bool | None = Field(
        default=None,
        description="Indicates whether the credentials were passed in clear text.<p><b>Note:</b> True if the credentials were passed in a clear text protocol such as FTP or TELNET, or if Windows detected that a user's logon password was passed to the authentication package in clear text.</p>",
    )
    is_mfa: bool | None = Field(
        default=None,
        description="Indicates whether Multi Factor Authentication was used during authentication. [Recommended]",
    )
    is_new_logon: bool | None = Field(
        default=None,
        description="Indicates logon is from a device not seen before or a first time account logon.",
    )
    is_remote: bool | None = Field(
        default=None,
        description="The attempted authentication is over a remote connection. [Recommended]",
    )
    logon_process: Process | None = Field(
        default=None,
        description="The trusted process that validated the authentication credentials.",
    )
    logon_type: str | None = Field(
        default=None,
        description="The logon type, normalized to the caption of the logon_type_id value. In the case of 'Other', it is defined by the event source. [Recommended]",
    )
    logon_type_id: LogonTypeId | None = Field(
        default=None, description="The normalized logon type identifier. [Recommended]"
    )
    message: str | None = Field(
        default=None,
        description="The description of the event/finding, as defined by the source. [Recommended]",
    )
    observables: list[Observable] | None = Field(
        default=None,
        description="The observables associated with the event or a finding. [Recommended]",
    )
    raw_data: str | None = Field(
        default=None, description="The raw event/finding data as received from the source."
    )
    service: Service | None = Field(
        default=None,
        description="The service or gateway to which the user or process is being authenticated [Recommended]",
    )
    session: Session | None = Field(
        default=None, description="The authenticated user or service session. [Recommended]"
    )
    severity: str | None = Field(
        default=None,
        description="The event/finding severity, normalized to the caption of the severity_id value. In the case of 'Other', it is defined by the source.",
    )
    src_endpoint: NetworkEndpoint | None = Field(
        default=None, description="Details about the source of the IAM activity. [Recommended]"
    )
    status: str | None = Field(
        default=None,
        description="The event status, normalized to the caption of the status_id value. In the case of 'Other', it is defined by the event source. [Recommended]",
    )
    status_code: str | None = Field(
        default=None,
        description="The event status code, as reported by the event source.<br /><br />For example, in a Windows Failed Authentication event, this would be the value of 'Failure Code', e.g. 0x18. [Recommended]",
    )
    status_detail: str | None = Field(
        default=None,
        description="The details about the authentication request. For example, possible details for Windows logon or logoff events are:<ul><li>Success</li><ul><li>LOGOFF_USER_INITIATED</li><li>LOGOFF_OTHER</li></ul><li>Failure</li><ul><li>USER_DOES_NOT_EXIST</li><li>INVALID_CREDENTIALS</li><li>ACCOUNT_DISABLED</li><li>ACCOUNT_LOCKED_OUT</li><li>PASSWORD_EXPIRED</li></ul></ul>",
    )
    status_id: StatusId | None = Field(
        default=None, description="The normalized identifier of the event status. [Recommended]"
    )
    unmapped: Object | None = Field(
        default=None,
        description="The attributes that are not mapped to the event schema. The names and values of those attributes are specific to the event source.",
    )

    @model_validator(mode="before")
    @classmethod
    def _reconcile_siblings(cls, data: Any) -> Any:
        """Reconcile sibling attribute pairs during parsing.

        For each sibling pair (e.g., activity_id/activity_name):
        - If both present: validate they match, use canonical label casing
        - If only ID: extrapolate label from enum
        - If only label: extrapolate ID from enum (unknown → OTHER=99)
        - If neither: leave for field validation to handle required/optional

        Special handling for type_uid:
        - Auto-calculated as class_uid * 100 + activity_id if not provided
        - Validated against activity_id if both provided
        """
        if not isinstance(data, dict):
            return data

        # Sibling pairs for this event class
        siblings: list[tuple[str, str, type[SiblingEnum]]] = [
            ("severity_id", "severity", cls.SeverityId),
            ("status_id", "status", cls.StatusId),
            ("auth_protocol_id", "auth_protocol", cls.AuthProtocolId),
            ("logon_type_id", "logon_type", cls.LogonTypeId),
        ]

        for id_field, label_field, enum_cls in siblings:
            id_val = data.get(id_field)
            label_val = data.get(label_field)

            has_id = id_val is not None
            has_label = label_val is not None

            if has_id and has_label:
                # Both present: validate consistency
                try:
                    enum_member = enum_cls(id_val)
                except (ValueError, KeyError) as e:
                    raise ValueError(f"Invalid {id_field} value: {id_val}") from e

                expected_label = enum_member.label

                # OTHER (99) allows any custom label
                if enum_member.value != 99:
                    if expected_label.lower() != str(label_val).lower():
                        raise ValueError(
                            f"{id_field}={id_val} ({expected_label}) "
                            f"does not match {label_field}={label_val!r}"
                        )
                    # Use canonical label casing
                    data[label_field] = expected_label
                # For OTHER, preserve the custom label as-is

            elif has_id:
                # Only ID provided: extrapolate label
                try:
                    enum_member = enum_cls(id_val)
                    data[label_field] = enum_member.label
                except (ValueError, KeyError) as e:
                    raise ValueError(f"Invalid {id_field} value: {id_val}") from e

            elif has_label:
                # Only label provided: extrapolate ID
                try:
                    enum_member = enum_cls(str(label_val))
                    data[id_field] = enum_member.value
                    data[label_field] = enum_member.label  # Canonical casing
                except (ValueError, KeyError):
                    # Unknown label during JSON parsing → map to OTHER (99) if available
                    # This is lenient for untrusted data, unlike direct enum construction
                    if hasattr(enum_cls, "OTHER"):
                        data[id_field] = 99
                        data[label_field] = "Other"  # Use canonical OTHER label
                    else:
                        raise ValueError(
                            f"Unknown {label_field} value: {label_val!r} "
                            f"and {enum_cls.__name__} has no OTHER member"
                        ) from None

        return data
