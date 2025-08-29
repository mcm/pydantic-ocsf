from typing import ClassVar

from ocsf.objects.network_endpoint import NetworkEndpoint


class NetworkProxy(NetworkEndpoint):
    schema_name: ClassVar[str] = "network_proxy"
