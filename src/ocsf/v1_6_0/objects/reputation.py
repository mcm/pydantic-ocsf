"""Reputation object."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from ocsf._base import OCSFBaseModel
from ocsf._sibling_enum import SiblingEnum


class Reputation(OCSFBaseModel):
    """The Reputation object describes the reputation/risk score of an entity (e.g. device, user, domain).

    See: https://schema.ocsf.io/1.6.0/objects/reputation
    """

    # Nested Enums for sibling attribute pairs
    class ScoreId(SiblingEnum):
        """The normalized reputation score identifier.

        OCSF Attribute: score_id
        """

        UNKNOWN = 0
        VERY_SAFE = 1
        SAFE = 2
        PROBABLY_SAFE = 3
        LEANS_SAFE = 4
        MAY_NOT_BE_SAFE = 5
        EXERCISE_CAUTION = 6
        SUSPICIOUSRISKY = 7
        POSSIBLY_MALICIOUS = 8
        PROBABLY_MALICIOUS = 9
        MALICIOUS = 10
        OTHER = 99

        @classmethod
        def _get_label_map(cls) -> dict[int, str]:
            return {
                0: "Unknown",
                1: "Very Safe",
                2: "Safe",
                3: "Probably Safe",
                4: "Leans Safe",
                5: "May not be Safe",
                6: "Exercise Caution",
                7: "Suspicious/Risky",
                8: "Possibly Malicious",
                9: "Probably Malicious",
                10: "Malicious",
                99: "Other",
            }

    base_score: float = Field(
        ..., description="The reputation score as reported by the event source."
    )
    score_id: ScoreId = Field(..., description="The normalized reputation score identifier.")
    provider: str | None = Field(
        default=None, description="The provider of the reputation information. [Recommended]"
    )
    score: str | None = Field(
        default=None,
        description="The reputation score, normalized to the caption of the score_id value. In the case of 'Other', it is defined by the event source.",
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
            ("score_id", "score", cls.ScoreId),
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
