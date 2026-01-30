"""The analytic type ID. enumeration."""

from enum import IntEnum


class AnalyticTypeId(IntEnum):
    """The analytic type ID.

    See: https://schema.ocsf.io/1.7.0/data_types/analytic_type_id
    """

    UNKNOWN = 0  #
    RULE = 1  # A Rule in security analytics refers to predefined criteria or conditions set to monitor, alert, or enforce policies, playing a crucial role in access control, threat detection, and regulatory compliance across security systems.
    BEHAVIORAL = 2  # Behavioral analytics focus on monitoring and analyzing user or system actions to identify deviations from established patterns, aiding in the detection of insider threats, fraud, and advanced persistent threats (APTs).
    STATISTICAL = 3  # Statistical analytics pertains to analyzing data patterns and anomalies using statistical models to predict, detect, and respond to potential threats, enhancing overall security posture through informed decision-making.
    LEARNING__ML_DL_ = 4  # Learning (ML/DL) encompasses techniques that can "learn" from known data to create analytics that generalize to new data. There may be a statistical component to these techniques, but it is not a requirement.
    FINGERPRINTING = 5  # Fingerprinting is the technique of collecting detailed system data, including software versions and configurations, to enhance threat detection, data loss prevention (DLP), and endpoint detection and response (EDR) capabilities.
    TAGGING = 6  # Tagging refers to the practice of assigning labels or identifiers to data, users, assets, or activities to monitor, control access, and facilitate incident response across various security domains such as DLP and EDR.
    KEYWORD_MATCH = 7  # Keyword Match involves scanning content for specific terms to identify sensitive information, potential threats, or policy violations, aiding in DLP and compliance monitoring.
    REGULAR_EXPRESSIONS = 8  # Regular Expressions are used to define complex search patterns for identifying, validating, and extracting specific data sets or threats within digital content, enhancing DLP, EDR, and threat detection mechanisms.
    EXACT_DATA_MATCH = 9  # Exact Data Match is a precise comparison technique used to detect the unauthorized use or exposure of specific, sensitive information, crucial for enforcing DLP policies and protecting against data breaches.
    PARTIAL_DATA_MATCH = 10  # Partial Data Match involves identifying instances where segments of sensitive information or patterns match, facilitating nuanced DLP and threat detection without requiring complete data conformity.
    INDEXED_DATA_MATCH = 11  # Indexed Data Match refers to comparing content against a pre-compiled index of sensitive information to efficiently detect and prevent unauthorized access or breaches, streamlining DLP and compliance efforts.
    OTHER = 99  #
