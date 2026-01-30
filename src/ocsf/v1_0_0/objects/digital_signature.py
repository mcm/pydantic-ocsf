"""Digital Signature object."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum

if TYPE_CHECKING:
    from ocsf.v1_0_0.objects.certificate import Certificate
    from ocsf.v1_0_0.objects.fingerprint import Fingerprint


class DigitalSignature(OCSFBaseModel):
    """The Digital Signature object contains information about the cryptographic mechanism used to verify the authenticity, integrity, and origin of the file or application.

    See: https://schema.ocsf.io/1.0.0/objects/digital_signature
    """

    # Nested Enums for sibling attribute pairs
    class AlgorithmId(SiblingEnum):
        """The identifier of the normalized digital signature algorithm.

        OCSF Attribute: algorithm_id
        """

        UNKNOWN = 0
        DSA = 1
        RSA = 2
        ECDSA = 3
        AUTHENTICODE = 4
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "DSA",
                2: "RSA",
                3: "ECDSA",
                4: "Authenticode",
                99: "Other",
            }

    algorithm_id: AlgorithmId = Field(
        ..., description="The identifier of the normalized digital signature algorithm."
    )
    algorithm: str | None = Field(
        default=None,
        description="The digital signature algorithm used to create the signature, normalized to the caption of 'algorithm_id'. In the case of 'Other', it is defined by the event source.",
    )
    certificate: Certificate | None = Field(
        default=None,
        description="The certificate object containing information about the digital certificate. [Recommended]",
    )
    created_time: int | None = Field(
        default=None, description="The time when the digital signature was created."
    )
    developer_uid: str | None = Field(
        default=None, description="The developer ID on the certificate that signed the file."
    )
    digest: Fingerprint | None = Field(
        default=None,
        description="The message digest attribute contains the fixed length message hash representation and the corresponding hashing algorithm information.",
    )

    @model_validator(mode="before")
    @classmethod
    def _reconcile_siblings(cls, data: Any) -> Any:
        """Reconcile sibling attribute pairs during parsing.

        For each sibling pair (e.g., activity_id/activity_name):
        - If both present: validate they match, use canonical label casing
        - If only ID: extrapolate label from enum
        - If only label: extrapolate ID from enum (unknown → OTHER=99)
        - If neither: leave for field validation to handle required/optional
        """
        if not isinstance(data, dict):
            return data

        # Sibling pairs for this object class
        siblings: list[tuple[str, str, type[SiblingEnum]]] = [
            ("algorithm_id", "algorithm", cls.AlgorithmId),
        ]

        for id_field, label_field, enum_cls in siblings:
            id_val = data.get(id_field)
            label_val = data.get(label_field)

            has_id = id_val is not None
            has_label = label_val is not None

            if has_id and has_label:
                # Both present: validate consistency
                assert id_val is not None  # Type narrowing for mypy
                try:
                    enum_member = enum_cls(id_val)
                except (ValueError, KeyError) as e:
                    raise ValueError(f"Invalid {id_field} value: {id_val}") from e

                expected_label = enum_member.label

                # OTHER (99) allows any custom label
                if enum_member.value != 99:
                    if expected_label.lower() != str(label_val).lower():
                        raise ValueError(
                            f"{id_field}={id_val} ({expected_label}) "
                            f"does not match {label_field}={label_val!r}"
                        )
                    # Use canonical label casing
                    data[label_field] = expected_label
                # For OTHER, preserve the custom label as-is

            elif has_id:
                # Only ID provided: extrapolate label
                assert id_val is not None  # Type narrowing for mypy
                try:
                    enum_member = enum_cls(id_val)
                    data[label_field] = enum_member.label
                except (ValueError, KeyError) as e:
                    raise ValueError(f"Invalid {id_field} value: {id_val}") from e

            elif has_label:
                # Only label provided: extrapolate ID
                try:
                    enum_member = enum_cls(str(label_val))
                    data[id_field] = enum_member.value
                    data[label_field] = enum_member.label  # Canonical casing
                except (ValueError, KeyError):
                    # Unknown label during JSON parsing → map to OTHER (99) if available
                    # This is lenient for untrusted data, unlike direct enum construction
                    if hasattr(enum_cls, "OTHER"):
                        data[id_field] = 99
                        data[label_field] = "Other"  # Use canonical OTHER label
                    else:
                        raise ValueError(
                            f"Unknown {label_field} value: {label_val!r} "
                            f"and {enum_cls.__name__} has no OTHER member"
                        ) from None

        return data
