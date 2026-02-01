"""Validator for pre-filling category_uid, class_uid, and type_uid."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, model_validator

if TYPE_CHECKING:
    from pydantic._internal._decorators import ModelValidatorDecoratorInfo, PydanticDescriptorProxy


def create_uid_prefill_validator(
    category_uid: int | None,
    class_uid: int | None,
) -> PydanticDescriptorProxy[ModelValidatorDecoratorInfo]:
    """Create a validator that pre-fills UID fields for OCSF events.

    Args:
        category_uid: The category UID to pre-fill (or None)
        class_uid: The class UID to pre-fill (or None)

    Returns:
        Pydantic model_validator function
    """

    @model_validator(mode="before")  # type: ignore[misc]
    @classmethod
    def _prefill_uids(cls: type[BaseModel], data: Any) -> Any:
        """Pre-fill category_uid, class_uid, and type_uid if not provided by user."""
        if not isinstance(data, dict):
            return data

        # Pre-fill category_uid if not present
        if category_uid is not None and "category_uid" not in data:
            data["category_uid"] = category_uid

        # Pre-fill class_uid if not present
        if class_uid is not None and "class_uid" not in data:
            data["class_uid"] = class_uid

        # Calculate type_uid if not present
        # Formula: type_uid = class_uid * 100 + activity_id
        if "type_uid" not in data:
            # Use class_uid from data (may have just been pre-filled)
            cls_uid = data.get("class_uid", class_uid)
            activity_id = data.get("activity_id")

            if cls_uid is not None and activity_id is not None:
                # Handle enum values - extract integer
                if hasattr(activity_id, "value"):
                    activity_id = activity_id.value
                data["type_uid"] = cls_uid * 100 + int(activity_id)

        return data

    return _prefill_uids
