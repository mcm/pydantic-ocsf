"""<p>The normalized identifier of the boundary of the connection. </p><p> For cloud connections, this translates to the traffic-boundary (same VPC, through IGW, etc.). For traditional networks, this is described as Local, Internal, or External.</p> enumeration."""

from enum import IntEnum


class NetworkConnectionInfoBoundaryId(IntEnum):
    """<p>The normalized identifier of the boundary of the connection. </p><p> For cloud connections, this translates to the traffic-boundary (same VPC, through IGW, etc.). For traditional networks, this is described as Local, Internal, or External.</p>

    See: https://schema.ocsf.io/1.7.0/data_types/network_connection_info_boundary_id
    """

    UNKNOWN = 0  # The connection boundary is unknown.
    LOCALHOST = 1  # Local network traffic on the same endpoint.
    INTERNAL = 2  # Internal network traffic between two endpoints inside network.
    EXTERNAL = (
        3  # External network traffic between two endpoints on the Internet or outside the network.
    )
    SAME_VPC = 4  # Through another resource in the same VPC
    INTERNET_VPC_GATEWAY = 5  # Through an Internet gateway or a gateway VPC endpoint
    VIRTUAL_PRIVATE_GATEWAY = 6  # Through a virtual private gateway
    INTRA_REGION_VPC = 7  # Through an intra-region VPC peering connection
    INTER_REGION_VPC = 8  # Through an inter-region VPC peering connection
    LOCAL_GATEWAY = 9  # Through a local gateway
    GATEWAY_VPC = 10  # Through a gateway VPC endpoint (Nitro-based instances only)
    INTERNET_GATEWAY = 11  # Through an Internet gateway (Nitro-based instances only)
    OTHER = 99  # The boundary is not mapped. See the <code>boundary</code> attribute, which contains a data source specific value.
