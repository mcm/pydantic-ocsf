from enum import Enum, property as enum_property
from typing import Any, ClassVar

from ocsf.events.application.application import Application
from ocsf.objects.http_request import HttpRequest
from ocsf.objects.http_response import HttpResponse
from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.tls import TLS
from ocsf.objects.web_resource import WebResource


class ActivityId(Enum):
    UNKNOWN = 0
    CREATE = 1
    READ = 2
    UPDATE = 3
    DELETE = 4
    SEARCH = 5
    IMPORT = 6
    EXPORT = 7
    SHARE = 8
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
            "CREATE": "Create",
            "READ": "Read",
            "UPDATE": "Update",
            "DELETE": "Delete",
            "SEARCH": "Search",
            "IMPORT": "Import",
            "EXPORT": "Export",
            "SHARE": "Share",
            "OTHER": "Other",
        }
        return name_map[super().name]


class WebResourcesActivity(Application):
    schema_name: ClassVar[str] = "web_resources_activity"
    class_id: int = 6001
    class_name: str = "Web Resources Activity"

    # Required
    activity_id: ActivityId
    web_resources: list[WebResource]

    # Recommended
    dst_endpoint: NetworkEndpoint | None = None
    http_request: HttpRequest | None = None
    src_endpoint: NetworkEndpoint | None = None
    web_resources_result: list[WebResource] | None = None

    # Optional
    http_response: HttpResponse | None = None
    tls: TLS | None = None
