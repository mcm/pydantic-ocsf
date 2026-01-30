"""Encryption Details object."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum


class EncryptionDetails(OCSFBaseModel):
    """Details about the encrytpion methodology utilized.

    See: https://schema.ocsf.io/1.5.0/objects/encryption_details
    """

    # Nested Enums for sibling attribute pairs
    class AlgorithmId(SiblingEnum):
        """The encryption algorithm used.

        OCSF Attribute: algorithm_id
        """

        DES = 1
        TRIPLEDES = 2
        AES = 3
        RSA = 4
        ECC = 5
        SM2 = 6

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                1: "DES",
                2: "TripleDES",
                3: "AES",
                4: "RSA",
                5: "ECC",
                6: "SM2",
            }

    algorithm: str | None = Field(
        default=None,
        description="The encryption algorithm used, normalized to the caption of 'algorithm_id",
    )
    algorithm_id: AlgorithmId | None = Field(
        default=None, description="The encryption algorithm used. [Recommended]"
    )
    key_length: int | None = Field(
        default=None, description="The length of the encryption key used."
    )
    key_uid: str | None = Field(
        default=None,
        description="The unique identifier of the key used for encrpytion. For example, AWS KMS Key ARN.",
    )
    type_: str | None = Field(
        default=None, description="The type of the encryption used. [Recommended]"
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
