"""The cyber kill chain phase identifier. enumeration."""

from enum import IntEnum


class KillChainPhaseId(IntEnum):
    """The cyber kill chain phase identifier.

    See: https://schema.ocsf.io/1.0.0/data_types/kill_chain_phase_id
    """

    UNKNOWN = 0  # The kill chain phase is unknown.
    RECONNAISSANCE = 1  # The attackers pick a target and perform a detailed analysis, start collecting information (email addresses, conferences information, etc.) and evaluate the victim’s vulnerabilities to determine how to exploit them.
    WEAPONIZATION = 2  # The attackers develop a malware weapon and aim to exploit the discovered vulnerabilities.
    DELIVERY = (
        3  # The intruders will use various tactics, such as phishing, infected USB drives, etc.
    )
    EXPLOITATION = (
        4  # The intruders start leveraging vulnerabilities to executed code on the victim’s system.
    )
    INSTALLATION = 5  # The intruders install malware on the victim’s system.
    COMMAND___CONTROL = 6  # Malware opens a command channel to enable the intruders to remotely manipulate the victim's system.
    ACTIONS_ON_OBJECTIVES = (
        7  # With hands-on keyboard access, intruders accomplish the mission’s goal.
    )
    OTHER = 99  #
