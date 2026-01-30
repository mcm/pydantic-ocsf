"""Matches the MITRE D3FEND™ Tactic. Note: the Model and Detect Tactics are not supported as remediations by the OCSF Remediation event class. enumeration."""

from enum import IntEnum


class ProcessRemediationActivityActivityId(IntEnum):
    """Matches the MITRE D3FEND™ Tactic. Note: the Model and Detect Tactics are not supported as remediations by the OCSF Remediation event class.

    See: https://schema.ocsf.io/1.6.0/data_types/process_remediation_activity_activity_id
    """

    ISOLATE = 1  # Creates logical or physical barriers in a system which reduces opportunities for adversaries to create further accesses. Defined by D3FEND™ <a target='_blank' href='https://d3fend.mitre.org/tactic/d3f:Isolate/'>d3f:Isolate</a>.
    EVICT = 2  # Removes an adversary or malicious resource from a device or computer network. Defined by D3FEND™ <a target='_blank' href='https://d3fend.mitre.org/tactic/d3f:Evict/'>d3f:Evict</a>.
    RESTORE = 3  # Returns the system to a better state. Defined by D3FEND™ <a target='_blank' href='https://d3fend.mitre.org/tactic/d3f:Restore/'>d3f:Restore</a>.
    HARDEN = 4  # Increases the opportunity cost of computer network exploitation. Defined by D3FEND™ <a target='_blank' href='https://d3fend.mitre.org/tactic/d3f:Harden/'>d3f:Harden</a>.
    DETECT = 5  # Further identify adversary access to or unauthorized activity on computer networks. Defined by D3FEND™ <a target='_blank' href='https://d3fend.mitre.org/tactic/d3f:Detect/'>d3f:Detect</a>.
