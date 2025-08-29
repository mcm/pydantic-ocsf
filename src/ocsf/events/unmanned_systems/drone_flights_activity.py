from enum import Enum, property as enum_property
from typing import Any, ClassVar

from pydantic import model_validator

from ocsf.events.unmanned_systems.unmanned_systems import UnmannedSystems
from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.network_traffic import NetworkTraffic
from ocsf.objects.unmanned_aerial_system import UnmannedAerialSystem
from ocsf.objects.unmanned_system_operating_area import UnmannedSystemOperatingArea
from ocsf.objects.user import User


class ActivityId(Enum):
    UNKNOWN = 0
    CAPTURE = 1
    RECORD = 2
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return ActivityId[obj]
        else:
            return ActivityId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "CAPTURE": "Capture",
            "RECORD": "Record",
            "OTHER": "Other",
        }
        return name_map[super().name]


class AuthProtocolId(Enum):
    UNKNOWN = 0
    NONE = 1
    UAS_ID_SIGNATURE = 2
    OPERATOR_ID_SIGNATURE = 3
    MESSAGE_SET_SIGNATURE = 4
    AUTHENTICATION_PROVIDED_BY_NETWORK_REMOTE_ID = 5
    SPECIFIC_AUTHENTICATION_METHOD = 6
    RESERVED = 7
    PRIVATE_USER = 8
    EAP = 9
    RADIUS = 10
    BASIC_AUTHENTICATION = 11
    LDAP = 12
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return AuthProtocolId[obj]
        else:
            return AuthProtocolId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "NONE": "None",
            "UAS_ID_SIGNATURE": "UAS ID Signature",
            "OPERATOR_ID_SIGNATURE": "Operator ID Signature",
            "MESSAGE_SET_SIGNATURE": "Message Set Signature",
            "AUTHENTICATION_PROVIDED_BY_NETWORK_REMOTE_ID": "Authentication Provided by Network Remote ID",
            "SPECIFIC_AUTHENTICATION_METHOD": "Specific Authentication Method",
            "RESERVED": "Reserved",
            "PRIVATE_USER": "Private User",
            "EAP": "EAP",
            "RADIUS": "RADIUS",
            "BASIC_AUTHENTICATION": "Basic Authentication",
            "LDAP": "LDAP",
            "OTHER": "Other",
        }
        return name_map[super().name]


class StatusId(Enum):
    UNKNOWN = 0
    UNDECLARED = 1
    GROUND = 2
    AIRBORNE = 3
    EMERGENCY = 4
    REMOTE_ID_SYSTEM_FAILURE = 5
    RESERVED = 6
    OTHER = 99

    @classmethod
    def validate_python(cls, obj: Any):
        try:
            obj = int(obj)
        except ValueError:
            obj = str(obj).upper()
            return StatusId[obj]
        else:
            return StatusId(obj)

    @enum_property
    def name(self):
        name_map = {
            "UNKNOWN": "Unknown",
            "UNDECLARED": "Undeclared",
            "GROUND": "Ground",
            "AIRBORNE": "Airborne",
            "EMERGENCY": "Emergency",
            "REMOTE_ID_SYSTEM_FAILURE": "Remote ID System Failure",
            "RESERVED": "Reserved",
            "OTHER": "Other",
        }
        return name_map[super().name]


class DroneFlightsActivity(UnmannedSystems):
    schema_name: ClassVar[str] = "drone_flights_activity"
    class_id: int = 8001
    class_name: str = "Drone Flights Activity"

    # Required
    activity_id: ActivityId
    unmanned_aerial_system: UnmannedAerialSystem
    unmanned_system_operator: User

    # Recommended
    status_id: StatusId | None = None
    unmanned_system_operating_area: UnmannedSystemOperatingArea | None = None

    # Optional
    auth_protocol: str | None = None
    auth_protocol_id: AuthProtocolId | None = None
    classification: str | None = None
    comment: str | None = None
    protocol_name: str | None = None
    src_endpoint: NetworkEndpoint | None = None
    status: str | None = None
    traffic: NetworkTraffic | None = None

    @model_validator(mode="after")
    def validate_at_least_one(self):
        if all(
            getattr(self, field) is None
            for field in [
                "src_endpoint",
                "unmanned_aerial_system",
                "unmanned_system_operator",
                "unmanned_system_operating_area",
            ]
        ):
            raise ValueError(
                "At least one of `src_endpoint`, `unmanned_aerial_system`, `unmanned_system_operator`, `unmanned_system_operating_area` must be provided"
            )
        return self
