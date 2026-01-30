"""The normalized identifier for the authentication factor. enumeration."""

from enum import IntEnum


class FactorTypeId(IntEnum):
    """The normalized identifier for the authentication factor.

    See: https://schema.ocsf.io/1.2.0/data_types/factor_type_id
    """

    UNKNOWN = 0  #
    SMS = 1  # User receives and inputs a code sent to their mobile device via SMS text message.
    SECURITY_QUESTION = 2  # The user responds to a security question as part of a question-based authentication factor
    PHONE_CALL = 3  # System calls the user's registered phone number and requires the user to answer and provide a response.
    BIOMETRIC = 4  # Devices that verify identity-based on user's physical identifiers, such as fingerprint scanners or retina scanners.
    PUSH_NOTIFICATION = 5  # Push notification is sent to user's registered device and requires the user to acknowledge.
    HARDWARE_TOKEN = 6  # Physical device that generates a code to be used for authentication.
    OTP = 7  # Application generates a one-time password (OTP) for use in authentication.
    EMAIL = 8  # A code or link is sent to a user's registered email address.
    U2F = 9  # Typically involves a hardware token, which the user physically interacts with to authenticate.
    WEBAUTHN = 10  # Web-based API that enables users to register devices as authentication factors.
    PASSWORD = 11  # The user enters a password that they have previously established.
    OTHER = 99  #
