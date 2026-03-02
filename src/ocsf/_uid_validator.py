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
        """Pre-fill and validate UID fields for OCSF events.

        category_uid and class_uid are fixed constants for each event type.
        type_uid is calculated as class_uid * 100 + activity_id.

        If any of these are provided by the caller, they must match the
        expected values — they exist only for OCSF wire-format compatibility
        and should not carry user-supplied semantics.
        """
        if not isinstance(data, dict):
            return data

        # category_uid: fixed constant for this event type
        if category_uid is not None:
            if "category_uid" in data and data["category_uid"] is not None:
                if data["category_uid"] != category_uid:
                    raise ValueError(
                        f"category_uid must be {category_uid} for this event type, "
                        f"got {data['category_uid']!r}"
                    )
            else:
                data["category_uid"] = category_uid

        # class_uid: fixed constant for this event type
        if class_uid is not None:
            if "class_uid" in data and data["class_uid"] is not None:
                if data["class_uid"] != class_uid:
                    raise ValueError(
                        f"class_uid must be {class_uid} for this event type, "
                        f"got {data['class_uid']!r}"
                    )
            else:
                data["class_uid"] = class_uid

        # type_uid: calculated as class_uid * 100 + activity_id
        cls_uid = data.get("class_uid", class_uid)
        activity_id = data.get("activity_id")

        if cls_uid is not None and activity_id is not None:
            if hasattr(activity_id, "value"):
                activity_id = activity_id.value
            expected_type_uid = cls_uid * 100 + int(activity_id)

            if "type_uid" in data and data["type_uid"] is not None:
                if data["type_uid"] != expected_type_uid:
                    raise ValueError(
                        f"type_uid must be {expected_type_uid} "
                        f"(class_uid={cls_uid} * 100 + activity_id={activity_id}), "
                        f"got {data['type_uid']!r}"
                    )
            else:
                data["type_uid"] = expected_type_uid

        return data

    return _prefill_uids
