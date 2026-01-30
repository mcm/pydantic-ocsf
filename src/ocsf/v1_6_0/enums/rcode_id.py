"""The normalized identifier of the DNS server response code. See <a target='_blank' href='https://datatracker.ietf.org/doc/html/rfc6895'>RFC-6895</a>. enumeration."""

from enum import IntEnum


class RcodeId(IntEnum):
    """The normalized identifier of the DNS server response code. See <a target='_blank' href='https://datatracker.ietf.org/doc/html/rfc6895'>RFC-6895</a>.

    See: https://schema.ocsf.io/1.6.0/data_types/rcode_id
    """

    NOERROR = 0  # No Error.
    FORMERROR = 1  # Format Error.
    SERVERROR = 2  # Server Failure.
    NXDOMAIN = 3  # Non-Existent Domain.
    NOTIMP = 4  # Not Implemented.
    REFUSED = 5  # Query Refused.
    YXDOMAIN = 6  # Name Exists when it should not.
    YXRRSET = 7  # RR Set Exists when it should not.
    NXRRSET = 8  # RR Set that should exist does not.
    NOTAUTH = 9  # Not Authorized or Server Not Authoritative for zone.
    NOTZONE = 10  # Name not contained in zone.
    DSOTYPENI = 11  # DSO-TYPE Not Implemented.
    BADSIG_VERS = 16  # TSIG Signature Failure or Bad OPT Version.
    BADKEY = 17  # Key not recognized.
    BADTIME = 18  # Signature out of time window.
    BADMODE = 19  # Bad TKEY Mode.
    BADNAME = 20  # Duplicate key name.
    BADALG = 21  # Algorithm not supported.
    BADTRUNC = 22  # Bad Truncation.
    BADCOOKIE = 23  # Bad/missing Server Cookie.
    UNASSIGNED = 24  # The codes deemed to be unassigned by the RFC (unassigned codes: 12-15, 24-3840, 4096-65534).
    RESERVED = 25  # The codes deemed to be reserved by the RFC (codes: 3841-4095, 65535).
    OTHER = 99  # The dns response code is not defined by the RFC.
