"""The normalized impact of the incident or finding. Per NIST, this is the magnitude of harm that can be expected to result from the consequences of unauthorized disclosure, modification, destruction, or loss of information or information system availability. enumeration."""

from enum import IntEnum


class IncidentFindingImpactId(IntEnum):
    """The normalized impact of the incident or finding. Per NIST, this is the magnitude of harm that can be expected to result from the consequences of unauthorized disclosure, modification, destruction, or loss of information or information system availability.

    See: https://schema.ocsf.io/1.5.0/data_types/incident_finding_impact_id
    """

    UNKNOWN = 0  # The normalized impact is unknown.
    LOW = 1  # The magnitude of harm is low.
    MEDIUM = 2  # The magnitude of harm is moderate.
    HIGH = 3  # The magnitude of harm is high.
    CRITICAL = 4  # The magnitude of harm is high and the scope is widespread.
    OTHER = 99  # The impact is not mapped. See the <code>impact</code> attribute, which contains a data source specific value.
