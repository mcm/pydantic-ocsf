from datetime import datetime
from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.network.network import Network
from ocsf.objects.dns_answer import DnsAnswer
from ocsf.objects.dns_query import DnsQuery
from ocsf.objects.network_connection_info import NetworkConnectionInfo
from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.network_traffic import NetworkTraffic


class ActivityId(Enum):
    UNKNOWN = 0
    QUERY = 1
    RESPONSE = 2
    TRAFFIC = 6
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return ActivityId[obj]
        else:
            return ActivityId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "QUERY": "Query",
            "RESPONSE": "Response",
            "TRAFFIC": "Traffic",
            "OTHER": "Other",
        }
        return name_map[super().name]


class RcodeId(Enum):
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

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return RcodeId[obj]
        else:
            return RcodeId(obj)

    @enum_property
    def name(self):
        name_map = {
            "NOERROR": "NoError",
            "FORMERROR": "FormError",
            "SERVERROR": "ServError",
            "NXDOMAIN": "NXDomain",
            "NOTIMP": "NotImp",
            "REFUSED": "Refused",
            "YXDOMAIN": "YXDomain",
            "YXRRSET": "YXRRSet",
            "NXRRSET": "NXRRSet",
            "NOTAUTH": "NotAuth",
            "NOTZONE": "NotZone",
            "DSOTYPENI": "DSOTYPENI",
            "BADSIG_VERS": "BADSIG_VERS",
            "BADKEY": "BADKEY",
            "BADTIME": "BADTIME",
            "BADMODE": "BADMODE",
            "BADNAME": "BADNAME",
            "BADALG": "BADALG",
            "BADTRUNC": "BADTRUNC",
            "BADCOOKIE": "BADCOOKIE",
            "UNASSIGNED": "Unassigned",
            "RESERVED": "Reserved",
            "OTHER": "Other",
        }
        return name_map[super().name]


class DnsActivity(Network):
    schema_name: ClassVar[str] = "dns_activity"
    class_id: int = 4003
    class_name: str = "DNS Activity"

    # Required
    activity_id: ActivityId

    # Recommended
    answers: list[DnsAnswer] | None = None
    dst_endpoint: NetworkEndpoint | None = None
    query: DnsQuery | None = None
    query_time: datetime | None = None
    rcode: str | None = None
    rcode_id: RcodeId | None = None
    response_time: datetime | None = None

    # Optional
    connection_info: NetworkConnectionInfo | None = None
    traffic: NetworkTraffic | None = None
