"""The state of the socket. enumeration."""

from enum import IntEnum


class NetworkConnectionQueryStateId(IntEnum):
    """The state of the socket.

    See: https://schema.ocsf.io/1.7.0/data_types/network_connection_query_state_id
    """

    UNKNOWN = 0  # The socket state is unknown.
    ESTABLISHED = (
        1  # The socket has an established connection between a local application and a remote peer.
    )
    SYN_SENT = 2  # The socket is actively trying to establish a connection to a remote peer.
    SYN_RECV = 3  # The socket has passively received a connection request from a remote peer.
    FIN_WAIT1 = 4  # The socket connection has been closed by the local application, the remote peer has not yet acknowledged the close, and the system is waiting for it to close its half of the connection.
    FIN_WAIT2 = 5  # The socket connection has been closed by the local application, the remote peer has acknowledged the close, and the system is waiting for it to close its half of the connection.
    TIME_WAIT = 6  # The socket connection has been closed by the local application, the remote peer has closed its half of the connection, and the system is waiting to be sure that the remote peer received the last acknowledgement.
    CLOSED = 7  # The socket is not in use.
    CLOSE_WAIT = 8  # The socket connection has been closed by the remote peer, and the system is waiting for the local application to close its half of the connection.
    LAST_ACK = 9  # The socket connection has been closed by the remote peer, the local application has closed its half of the connection, and the system is waiting for the remote peer to acknowledge the close.
    LISTEN = 10  # The socket is listening for incoming connections.
    CLOSING = 11  # The socket connection has been closed by the local application and the remote peer simultaneously, and the remote peer has not yet acknowledged the close attempt of the local application.
