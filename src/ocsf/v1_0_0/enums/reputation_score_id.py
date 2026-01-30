"""The normalized reputation score identifier. enumeration."""

from enum import IntEnum


class ReputationScoreId(IntEnum):
    """The normalized reputation score identifier.

    See: https://schema.ocsf.io/1.0.0/data_types/reputation_score_id
    """

    UNKNOWN = 0  # The reputation score is unknown.
    VERY_SAFE = 1  # Long history of good behavior.
    SAFE = 2  # Consistently good behavior.
    PROBABLY_SAFE = 3  # Reasonable history of good behavior.
    LEANS_SAFE = 4  # Starting to establish a history of normal behavior.
    MAY_NOT_BE_SAFE = 5  # No established history of normal behavior.
    EXERCISE_CAUTION = 6  # Starting to establish a history of suspicious or risky behavior.
    SUSPICIOUS_RISKY = 7  # A site with a history of suspicious or risky behavior. (spam, scam, potentially unwanted software, potentially malicious).
    POSSIBLY_MALICIOUS = 8  # Strong possibility of maliciousness.
    PROBABLY_MALICIOUS = 9  # Indicators of maliciousness.
    MALICIOUS = 10  # Proven evidence of maliciousness.
    OTHER = 99  # The reputation score is not mapped. See the <code>rep_score</code> attribute, which contains a data source specific value.
