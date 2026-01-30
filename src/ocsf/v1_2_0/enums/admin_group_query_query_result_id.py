"""The normalized identifier of the query result. enumeration."""

from enum import IntEnum


class AdminGroupQueryQueryResultId(IntEnum):
    """The normalized identifier of the query result.

    See: https://schema.ocsf.io/1.2.0/data_types/admin_group_query_query_result_id
    """

    UNKNOWN = 0  # The query result is unknown.
    EXISTS = 1  # The target was found.
    PARTIAL = 2  # The target was partially found.
    DOES_NOT_EXIST = 3  # The target was not found.
    ERROR = 4  # The discovery attempt failed.
    UNSUPPORTED = 5  # Discovery of the target was not supported.
    OTHER = 99  # The query result is not mapped. See the <code>query_result</code> attribute, which contains a data source specific value.
