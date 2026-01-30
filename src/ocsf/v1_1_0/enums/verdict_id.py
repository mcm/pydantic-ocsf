"""The normalized verdict of an Incident. enumeration."""

from enum import IntEnum


class VerdictId(IntEnum):
    """The normalized verdict of an Incident.

    See: https://schema.ocsf.io/1.1.0/data_types/verdict_id
    """

    UNKNOWN = 0  # The type is unknown.
    FALSE_POSITIVE = 1  # The incident is a false positive.
    TRUE_POSITIVE = 2  # The incident is a true positive.
    DISREGARD = 3  # The incident can be disregarded as it is unimportant, an error or accident.
    SUSPICIOUS = 4  # The incident is suspicious.
    BENIGN = 5  # The incident is benign.
    TEST = 6  # The incident is a test.
    INSUFFICIENT_DATA = 7  # The incident has insufficient data to make a verdict.
    SECURITY_RISK = 8  # The incident is a security risk.
    MANAGED_EXTERNALLY = 9  # The incident remediation or required actions are managed externally.
    DUPLICATE = 10  # The incident is a duplicate.
    OTHER = 99  # The type is not mapped. See the <code>type</code> attribute, which contains a data source specific value.
