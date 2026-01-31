"""Dynamic Pydantic model factory for OCSF schemas."""

from __future__ import annotations

from typing import Any

from pydantic import Field, create_model

from ocsf._base import OCSFBaseModel
from ocsf._exceptions import ModelNotFoundError


class ModelFactory:
    """Factory for creating Pydantic models from OCSF schemas.

    Creates models on-demand using Pydantic's create_model() function,
    resolving inheritance and forward references as needed.
    """

    def __init__(self, schema: dict[str, Any], version: str) -> None:
        """Initialize the model factory.

        Args:
            schema: Parsed OCSF schema dictionary
            version: Version string (e.g., "1.7.0")
        """
        self.schema = schema
        self.version = version
        self.objects = schema.get("objects", {})
        self.events = schema.get("events", {})
        self.dictionary = schema.get("dictionary", {})
        self.dict_attributes = self.dictionary.get("attributes", {})

    def create_model(
        self, name: str, model_cache: dict[str, type[OCSFBaseModel]]
    ) -> type[OCSFBaseModel]:
        """Create a Pydantic model for the given OCSF object/event.

        Args:
            name: Name of the object/event (e.g., "User", "FileActivity")
            model_cache: Cache of already-created models for reference

        Returns:
            Dynamically created Pydantic model class

        Raises:
            ModelNotFoundError: If the model name is not found in the schema
        """
        from ocsf._utils import snake_to_pascal

        # Convert PascalCase name to snake_case for schema lookup
        # Try both the provided name and snake_case version
        schema_name = self._pascal_to_snake(name)

        # Check if it exists in objects or events
        spec = (
            self.objects.get(schema_name)
            or self.events.get(schema_name)
            or self.objects.get(name)  # Also try original name
            or self.events.get(name)
        )
        if spec is None:
            # Convert all schema names to PascalCase for error message
            available = [
                snake_to_pascal(k) for k in list(self.objects.keys()) + list(self.events.keys())
            ]
            raise ModelNotFoundError(name, self.version, available)

        # Phase 1: Resolve inheritance - ensure parent exists
        base_class = OCSFBaseModel
        if "extends" in spec:
            parent_schema_name = spec["extends"]
            # Convert to PascalCase for model name
            parent_name = snake_to_pascal(parent_schema_name)
            # Create parent first if not in cache
            if parent_name not in model_cache:
                parent_model = self.create_model(parent_name, model_cache)
                model_cache[parent_name] = parent_model
            base_class = model_cache[parent_name]

        # Phase 2: Extract inline enums
        from ocsf._enum_factory import create_sibling_enum, extract_inline_enums

        attributes = spec.get("attributes", {})
        inline_enums = extract_inline_enums(attributes, self.dictionary)

        # Create enum classes
        enum_classes = {}
        for field_name, (enum_values, sibling_id) in inline_enums.items():
            if sibling_id:  # Only create enum for ID fields
                # Convert activity_id -> ActivityId
                enum_name = snake_to_pascal(field_name)
                enum_cls = create_sibling_enum(enum_name, enum_values, name)
                enum_classes[field_name] = enum_cls

        # Phase 3: Build field definitions
        field_defs = {}

        for field_name, field_spec in attributes.items():
            # Skip special schema directives like $include
            if field_name.startswith("$"):
                continue

            # Skip non-dict field specs (shouldn't happen but be safe)
            if not isinstance(field_spec, dict):
                continue

            # Check if this field has an inline enum
            if field_name in enum_classes:
                # Use the enum type
                enum_cls = enum_classes[field_name]
                is_required = field_spec.get("requirement") == "required"

                # Build type annotation with enum
                field_type_annotation = enum_cls if is_required else f"{enum_cls.__name__} | None"
            else:
                field_type_annotation = self._build_field_type(field_name, field_spec)

            is_required = field_spec.get("requirement") == "required"

            # Create field with appropriate default
            if is_required:
                field_defs[field_name] = (field_type_annotation, Field(...))
            else:
                field_defs[field_name] = (
                    field_type_annotation,
                    Field(default=None),
                )

        # Phase 4: Create the model
        model = create_model(  # type: ignore[call-overload]
            name,
            __base__=base_class,
            __module__="ocsf.models",
            **field_defs,
        )

        # Phase 5: Attach enum classes as nested classes
        for _field_name, enum_cls in enum_classes.items():
            # Attach with the PascalCase name (e.g., ActivityId)
            setattr(model, enum_cls.__name__, enum_cls)

        # Phase 6: Add sibling reconciliation validators
        from ocsf._sibling_validator import create_sibling_reconciler

        for field_name in enum_classes:
            # For activity_id, label field is activity_name
            if field_name.endswith("_id"):
                label_field = field_name[:-3]  # Remove _id

                # Check if label field exists in attributes
                if label_field in attributes or f"{label_field}_name" in attributes:
                    # Some use activity_name instead of activity
                    if f"{label_field}_name" in attributes:
                        label_field = f"{label_field}_name"

                    enum_cls = enum_classes[field_name]
                    reconciler = create_sibling_reconciler(field_name, label_field, enum_cls)

                    # Attach the validator to the model
                    # Pydantic will pick up validators defined on the class
                    validator_name = f"_reconcile_{field_name}"
                    setattr(model, validator_name, reconciler)

        return model  # type: ignore[no-any-return]

    def _build_field_type(self, field_name: str, field_spec: dict[str, Any]) -> Any:
        """Build a Python type annotation from an OCSF field specification.

        Args:
            field_name: Name of the field (for dictionary lookup)
            field_spec: Field specification from schema

        Returns:
            Python type annotation (may include forward references as strings)
        """
        from ocsf._utils import ocsf_type_to_python, snake_to_pascal

        # Merge with dictionary definition if field spec is minimal
        if field_name in self.dict_attributes:
            dict_def = self.dict_attributes[field_name]
            # Merge: local spec overrides dictionary
            merged_spec = {**dict_def, **field_spec}
        else:
            merged_spec = field_spec

        ocsf_type = merged_spec.get("type", "string_t")
        is_array = merged_spec.get("is_array", False)
        is_required = merged_spec.get("requirement") == "required"

        # Check if type references an object (OCSF uses object names as types)
        if ocsf_type in self.objects or ocsf_type in self.events:
            # This is an object reference - convert to PascalCase
            python_type = snake_to_pascal(ocsf_type)
        # Handle explicit object_type field
        elif "object_type" in merged_spec:
            python_type = snake_to_pascal(merged_spec["object_type"])
        # Handle enum types
        elif "enum" in merged_spec:
            # For now, treat as int (Phase 2 will add enum support)
            python_type = "int"
        # Map primitive types
        else:
            python_type = ocsf_type_to_python(
                ocsf_type,
                is_array=False,
                object_type=None,
                enum_name=None,
            )

        # Handle arrays
        type_annotation = f"list[{python_type}]" if is_array else python_type

        # Add None for optional fields
        if not is_required:
            type_annotation = f"{type_annotation} | None"

        return type_annotation

    def _pascal_to_snake(self, name: str) -> str:
        """Convert PascalCase to snake_case.

        Args:
            name: PascalCase name (e.g., "User", "FileActivity", "Entity")

        Returns:
            snake_case name (e.g., "user", "file_activity", "_entity")

        Note:
            OCSF uses leading underscores for some base classes like _entity, _dns.
            We need to check both with and without leading underscore.
        """
        import re

        # Insert underscores before uppercase letters that follow lowercase letters
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        # Insert underscores before uppercase letters that follow lowercase or uppercase letters
        s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
        snake_name = s2.lower()

        # Check if the schema has this with a leading underscore
        # (OCSF uses _entity, _dns, _resource for base classes)
        if f"_{snake_name}" in self.objects or f"_{snake_name}" in self.events:
            return f"_{snake_name}"

        return snake_name

    def get_all_model_names(self) -> list[str]:
        """Get all available model names in this schema (in PascalCase).

        Returns:
            List of model names (both objects and events) in PascalCase
        """
        from ocsf._utils import snake_to_pascal

        return [snake_to_pascal(k) for k in list(self.objects.keys()) + list(self.events.keys())]
