"""The endpoint type ID. enumeration."""

from enum import IntEnum


class EndpointTypeId(IntEnum):
    """The endpoint type ID.

    See: https://schema.ocsf.io/1.6.0/data_types/endpoint_type_id
    """

    SERVER = 1  # A <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:Server/'>server</a>.
    DESKTOP = 2  # A <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:DesktopComputer/'>desktop computer</a>.
    LAPTOP = 3  # A <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:LaptopComputer/'>laptop computer</a>.
    TABLET = 4  # A <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:TabletComputer/'>tablet computer</a>.
    MOBILE = 5  # A <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:MobilePhone/'>mobile phone</a>.
    VIRTUAL = 6  # A <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:VirtualizationSoftware/'>virtual machine</a>.
    IOT = 7  # An <a target='_blank' href='https://www.techtarget.com/iotagenda/definition/IoT-device'>IOT (Internet of Things) device</a>.
    BROWSER = 8  # A <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:Browser/'>web browser</a>.
    FIREWALL = 9  # A <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:Firewall/'>networking firewall</a>.
    SWITCH = 10  # A <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:Switch/'>networking switch</a>.
    HUB = 11  # A <a target='_blank' href='https://en.wikipedia.org/wiki/Ethernet_hub'>networking hub</a>.
    ROUTER = 12  # A <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:Router/'>networking router</a>.
    IDS = 13  # An <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:IntrusionDetectionSystem/'>intrusion detection system</a>.
    IPS = 14  # An <a target='_blank' href='https://d3fend.mitre.org/dao/artifact/d3f:IntrusionPreventionSystem/'>intrusion prevention system</a>.
    LOAD_BALANCER = 15  # A <a target='_blank' href='https://en.wikipedia.org/wiki/Load_balancing_(computing)'>Load Balancer device.</a>
