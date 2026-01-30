"""The list of normalized identifiers of the malware classifications. enumeration."""

from enum import IntEnum


class ClassificationIds(IntEnum):
    """The list of normalized identifiers of the malware classifications.

    See: https://schema.ocsf.io/1.6.0/data_types/classification_ids
    """

    ADWARE = 1  #
    BACKDOOR = 2  #
    BOT = 3  #
    BOOTKIT = 4  #
    DDOS = 5  #
    DOWNLOADER = 6  #
    DROPPER = 7  #
    EXPLOIT_KIT = 8  #
    KEYLOGGER = 9  #
    RANSOMWARE = 10  #
    REMOTE_ACCESS_TROJAN = 11  #
    RESOURCE_EXPLOITATION = 13  #
    ROGUE_SECURITY_SOFTWARE = 14  #
    ROOTKIT = 15  #
    SCREEN_CAPTURE = 16  #
    SPYWARE = 17  #
    TROJAN = 18  #
    VIRUS = 19  #
    WEBSHELL = 20  #
    WIPER = 21  #
    WORM = 22  #
