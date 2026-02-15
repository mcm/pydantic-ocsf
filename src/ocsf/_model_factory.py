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
        self,
        name: str,
        model_cache: dict[str, type[OCSFBaseModel]],
        namespace_filter: str | None = None,
    ) -> type[OCSFBaseModel]:
        """Create a Pydantic model for the given OCSF object/event.

        Args:
            name: Name of the object/event (e.g., "User", "FileActivity")
            model_cache: Cache of already-created models for reference
            namespace_filter: Optional filter - "objects", "events", or None

        Returns:
            Dynamically created Pydantic model class

        Raises:
            ModelNotFoundError: If the model name is not found in the schema
        """
        from ocsf._utils import snake_to_pascal

        # Convert PascalCase name to snake_case for schema lookup
        # Try both the provided name and snake_case version
        schema_name = self._pascal_to_snake(name)

        # Apply namespace filter
        if namespace_filter == "objects":
            spec = self.objects.get(schema_name) or self.objects.get(name)
        elif namespace_filter == "events":
            spec = self.events.get(schema_name) or self.events.get(name)
        else:
            # No filter - search both (backward compatibility)
            spec = (
                self.objects.get(schema_name)
                or self.events.get(schema_name)
                or self.objects.get(name)
                or self.events.get(name)
            )

        if spec is None:
            # Convert all schema names to PascalCase for error message
            available = [
                snake_to_pascal(k) for k in list(self.objects.keys()) + list(self.events.keys())
            ]
            if namespace_filter:
                raise ModelNotFoundError(
                    f"{name} (in {namespace_filter} namespace)", self.version, available
                )
            else:
                raise ModelNotFoundError(name, self.version, available)

        # Phase 1: Resolve inheritance - ensure parent exists
        base_class = OCSFBaseModel
        if "extends" in spec:
            parent_schema_name = spec["extends"]
            # Convert to PascalCase for model name
            parent_name = snake_to_pascal(parent_schema_name)
            # Create parent first if not in cache
            # Use namespaced cache key when namespace_filter is provided
            if namespace_filter:
                parent_cache_key = f"{namespace_filter}:{parent_name}"
            else:
                parent_cache_key = parent_name

            if parent_cache_key not in model_cache:
                parent_model = self.create_model(parent_name, model_cache, namespace_filter)
                model_cache[parent_cache_key] = parent_model
            base_class = model_cache[parent_cache_key]

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

        for schema_field_name, field_spec in attributes.items():
            # Skip special schema directives like $include
            if schema_field_name.startswith("$"):
                continue

            # Skip non-dict field specs (shouldn't happen but be safe)
            if not isinstance(field_spec, dict):
                continue

            # Convert reserved keywords to have trailing underscore
            field_name, field_alias = self._handle_reserved_keyword(schema_field_name)

            # Check if this field has an inline enum
            if schema_field_name in enum_classes:
                # Use the enum type
                enum_cls = enum_classes[schema_field_name]
                is_required = field_spec.get("requirement") == "required"

                # Build type annotation with enum
                field_type_annotation = enum_cls if is_required else f"{enum_cls.__name__} | None"
            else:
                field_type_annotation = self._build_field_type(schema_field_name, field_spec)

            is_required = field_spec.get("requirement") == "required"

            # Create field with appropriate default and alias
            if is_required:
                if field_alias:
                    field_defs[field_name] = (field_type_annotation, Field(..., alias=field_alias))
                else:
                    field_defs[field_name] = (field_type_annotation, Field(...))
            else:
                if field_alias:
                    field_defs[field_name] = (
                        field_type_annotation,
                        Field(default=None, alias=field_alias),
                    )
                else:
                    field_defs[field_name] = (
                        field_type_annotation,
                        Field(default=None),
                    )

        # Phase 3b: Infer sibling label fields for enum-backed ID fields
        # Per OCSF spec, sibling attributes may be explicitly in the schema or
        # defined in the dictionary's 'sibling' attribute, or must be inferred
        from ocsf._utils import infer_sibling_label_field

        for field_name in enum_classes:
            if field_name.endswith("_id"):
                # First, check if the dictionary definition specifies a sibling field
                dict_def = self.dict_attributes.get(field_name, {})
                explicit_sibling = dict_def.get("sibling")

                if explicit_sibling:
                    # Use the explicit sibling name from the dictionary
                    # Handle reserved keywords (e.g., "type" -> "type_")
                    label_field, label_alias = self._handle_reserved_keyword(explicit_sibling)
                else:
                    # Fall back to inference if no explicit sibling
                    label_field = infer_sibling_label_field(field_name)
                    label_alias = None

                # Only add if not already defined (some are explicit in schema)
                if label_field not in field_defs:
                    # Add as optional string field with alias if needed
                    if label_alias:
                        field_defs[label_field] = (
                            "str | None",
                            Field(
                                default=None,
                                alias=label_alias,
                                description=f"Label for {field_name}",
                            ),
                        )
                    else:
                        field_defs[label_field] = (
                            "str | None",
                            Field(default=None, description=f"Label for {field_name}"),
                        )

        # Phase 4: Prepare validators
        validators_dict = {}

        # Phase 4a: Add sibling reconciliation validators
        from ocsf._sibling_validator import create_sibling_reconciler
        from ocsf._utils import infer_sibling_label_field

        for field_name in enum_classes:
            if field_name.endswith("_id"):
                # Use the same logic as Phase 3b to determine the label field
                dict_def = self.dict_attributes.get(field_name, {})
                explicit_sibling = dict_def.get("sibling")

                if explicit_sibling:
                    # Use the explicit sibling name from the dictionary
                    # Note: We capture the alias but don't use it here because the Field
                    # definition already has it set (from Phase 3b). We only need the
                    # Python field name to reference the field in validators.
                    label_field, _label_alias = self._handle_reserved_keyword(explicit_sibling)
                else:
                    # Fall back to inference
                    label_field = infer_sibling_label_field(field_name)

                # Check if label field exists in our field definitions
                # (either from schema or inferred in Phase 3b)
                if label_field in field_defs:
                    enum_cls = enum_classes[field_name]
                    reconciler = create_sibling_reconciler(field_name, label_field, enum_cls)
                    validator_name = f"_reconcile_{field_name}"
                    validators_dict[validator_name] = reconciler

        # Phase 4b: Add UID pre-fill validator for events only
        if namespace_filter == "events" or (
            namespace_filter is None and schema_name in self.events
        ):
            from ocsf._uid_validator import create_uid_prefill_validator

            # Resolve category_uid by tracing inheritance
            category_uid = self._resolve_category_uid(spec)

            # Get class_uid from event's uid field
            class_uid = spec.get("uid")

            # Only add validator if we have at least one UID to pre-fill
            if category_uid is not None or class_uid is not None:
                uid_validator = create_uid_prefill_validator(category_uid, class_uid)
                validators_dict["_prefill_uids"] = uid_validator

        # Phase 5: Create the model with validators
        model = create_model(  # type: ignore[call-overload]
            name,
            __base__=base_class,
            __module__="ocsf.models",
            __validators__=validators_dict if validators_dict else None,
            **field_defs,
        )

        # Phase 6: Attach enum classes as nested classes
        for _field_name, enum_cls in enum_classes.items():
            # Attach with the PascalCase name (e.g., ActivityId)
            setattr(model, enum_cls.__name__, enum_cls)

        return model  # type: ignore[no-any-return]

    def _build_field_type(self, field_name: str, field_spec: dict[str, Any]) -> Any:
        """Build a Python type annotation from an OCSF field specification.

        Args:
            field_name: Name of the field (for dictionary lookup)
            field_spec: Field specification from schema

        Returns:
            Python type annotation (may include forward references as strings)
        """
        from pydantic import SerializeAsAny  # noqa: F401 - Used in string annotations

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
        needs_serialize_as_any = False

        # Check if type references an object (OCSF uses object names as types)
        if ocsf_type in self.objects or ocsf_type in self.events:
            # This is an object reference - convert to PascalCase
            python_type = snake_to_pascal(ocsf_type)
            # Check if it's the Object type which needs SerializeAsAny
            needs_serialize_as_any = ocsf_type == "object"
        # Handle explicit object_type field
        elif "object_type" in merged_spec:
            python_type = snake_to_pascal(merged_spec["object_type"])
            # Check if it's the Object type which needs SerializeAsAny
            needs_serialize_as_any = merged_spec["object_type"] == "object"
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

        # Wrap Object type with SerializeAsAny for proper serialization
        if needs_serialize_as_any:
            python_type = f"SerializeAsAny[{python_type}]"

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

    def _resolve_category_uid(self, spec: dict[str, Any]) -> int | None:
        """Resolve category UID by tracing inheritance chain.

        Args:
            spec: Event specification from schema

        Returns:
            Category UID (1-8) or None if not found/not applicable
        """
        # Build category name -> UID mapping from categories_meta
        categories_meta = self.schema.get("categories_meta", {})
        category_attrs = categories_meta.get("attributes", {})
        category_map = {name: info["uid"] for name, info in category_attrs.items()}

        # Check if this event has a category field
        if "category" in spec and spec["category"]:
            category_name = spec["category"]
            return category_map.get(category_name)

        # Trace through inheritance chain to find category
        if "extends" in spec:
            parent_name = spec["extends"]
            parent_spec = self.events.get(parent_name)
            if parent_spec:
                return self._resolve_category_uid(parent_spec)

        return None

    def _handle_reserved_keyword(self, field_name: str) -> tuple[str, str | None]:
        """Handle reserved keyword field names.

        Fields that are Python reserved keywords need a trailing underscore
        (e.g., type -> type_) and should use the original name as an alias
        for serialization.

        Args:
            field_name: Field name from schema (e.g., "type", "class", "normal_field")

        Returns:
            Tuple of (python_field_name, alias)
            - python_field_name: Field name to use in Python (e.g., "type_", "class_", "normal_field")
            - alias: Original name to use for serialization (e.g., "type", "class") or None
        """
        # Python reserved keywords that need underscore suffix
        RESERVED_KEYWORDS = {
            "False",
            "None",
            "True",
            "and",
            "as",
            "assert",
            "async",
            "await",
            "break",
            "class",
            "continue",
            "def",
            "del",
            "elif",
            "else",
            "except",
            "finally",
            "for",
            "from",
            "global",
            "if",
            "import",
            "in",
            "is",
            "lambda",
            "nonlocal",
            "not",
            "or",
            "pass",
            "raise",
            "return",
            "try",
            "while",
            "with",
            "yield",
            "type",
        }

        # Check if field name is a reserved keyword
        if field_name in RESERVED_KEYWORDS or field_name.lower() in {
            k.lower() for k in RESERVED_KEYWORDS
        }:
            # Return field name with underscore and original name as alias
            return (f"{field_name}_", field_name)

        # Not a reserved keyword, return as-is with no alias
        return (field_name, None)

    def get_all_model_names(self) -> list[str]:
        """Get all available model names in this schema (in PascalCase).

        Returns:
            List of model names (both objects and events) in PascalCase
        """
        from ocsf._utils import snake_to_pascal

        return [snake_to_pascal(k) for k in list(self.objects.keys()) + list(self.events.keys())]
