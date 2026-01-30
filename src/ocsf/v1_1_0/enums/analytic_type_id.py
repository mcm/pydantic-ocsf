"""The analytic type ID. enumeration."""

from enum import IntEnum


class AnalyticTypeId(IntEnum):
    """The analytic type ID.

    See: https://schema.ocsf.io/1.1.0/data_types/analytic_type_id
    """

    UNKNOWN = 0  #
    RULE = 1  #
    BEHAVIORAL = 2  #
    STATISTICAL = 3  #
    LEARNING__ML_DL_ = 4  #
    OTHER = 99  #
