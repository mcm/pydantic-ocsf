"""Dynamic version module that creates models on-demand."""

from __future__ import annotations

import contextlib
from enum import IntEnum
from types import ModuleType
from typing import Any

from ocsf._base import OCSFBaseModel
from ocsf._model_factory import ModelFactory
from ocsf._schema_loader import get_schema_loader


class OCSFVersionModule(ModuleType):
    """Module that creates OCSF models on-demand via __getattr__.

    This module acts as a namespace for OCSF models of a specific version.
    When you access an attribute (e.g., `ocsf.v1_7_0.User`), it creates the
    model dynamically from the schema and caches it for future use.

    Example:
        from ocsf.v1_7_0 import User  # Creates User model on first import
        from ocsf.v1_7_0 import User  # Returns cached User model
    """

    def __init__(self, name: str, version: str) -> None:
        """Initialize the version module.

        Args:
            name: Full module name (e.g., "ocsf.v1_7_0")
            version: Version string (e.g., "1.7.0")
        """
        super().__init__(name)
        self.version = version
        self._model_cache: dict[str, type[OCSFBaseModel]] = {}
        self.__file__ = f"<ocsf-jit:{version}>"
        self.__path__ = []

        # Load schema
        loader = get_schema_loader()
        self.schema = loader.load_schema(version)

        # Create model factory
        self.factory = ModelFactory(self.schema, version)

    def __getattr__(self, name: str) -> Any:
        """Create models on-demand when accessed.

        Args:
            name: Model name (e.g., "User", "FileActivity")

        Returns:
            Dynamically created Pydantic model class

        Raises:
            AttributeError: If the model name is not found
        """
        # Check cache first
        if name in self._model_cache:
            return self._model_cache[name]

        # Avoid infinite recursion for private attributes
        if name.startswith("_"):
            raise AttributeError(f"module '{self.__name__}' has no attribute '{name}'")

        # Create the model
        try:
            model = self.factory.create_model(name, self._model_cache)
        except Exception as e:
            # Convert to AttributeError for proper import error handling
            raise AttributeError(f"module '{self.__name__}' has no attribute '{name}'") from e

        # Cache it
        self._model_cache[name] = model

        # Load all dependencies for this model
        self._load_dependencies(model)

        # Rebuild with complete namespace
        self._try_rebuild_model(model)

        return model

    def _load_dependencies(self, model: type[OCSFBaseModel]) -> None:
        """Recursively load all models that this model references.

        Args:
            model: Model to load dependencies for
        """

        # Extract forward references from field annotations
        dependencies: set[str] = set()

        for _field_name, field_info in model.model_fields.items():
            annotation = field_info.annotation

            # Extract type from annotation
            self._extract_dependencies(annotation, dependencies)

        # Load each dependency recursively
        for dep_name in dependencies:
            if dep_name not in self._model_cache:
                # Dependency doesn't exist in schema, skip
                with contextlib.suppress(AttributeError):
                    # Recursively trigger loading
                    getattr(self, dep_name)

    def _extract_dependencies(self, annotation: Any, dependencies: set[str]) -> None:
        """Extract model names from a type annotation.

        Args:
            annotation: Type annotation to extract from
            dependencies: Set to add dependencies to
        """
        from typing import ForwardRef, Union, get_args, get_origin

        # Handle ForwardRef
        if isinstance(annotation, ForwardRef):
            # Extract the forward ref string
            ref_str = annotation.__forward_arg__

            # Parse string annotations like "list[Group] | None" or "Account | None"
            # Extract model names from the string
            self._parse_annotation_string(ref_str, dependencies)
            return

        # Handle Union types (X | Y)
        origin = get_origin(annotation)
        if origin is Union:
            for arg in get_args(annotation):
                self._extract_dependencies(arg, dependencies)
            return

        # Handle list[Model]
        if origin is list:
            for arg in get_args(annotation):
                self._extract_dependencies(arg, dependencies)
            return

    def _parse_annotation_string(self, annotation_str: str, dependencies: set[str]) -> None:
        """Parse a string annotation to extract model names.

        Args:
            annotation_str: String like "list[Group] | None" or "Account"
            dependencies: Set to add dependencies to
        """
        import re

        # Find all potential model names
        # Pattern: CamelCase words (model names)
        pattern = r"\b([A-Z][a-zA-Z0-9]*)\b"
        matches = re.findall(pattern, annotation_str)

        for match in matches:
            # Skip common type keywords
            if match not in ("None", "Any", "Union", "Optional"):
                dependencies.add(match)

    def _try_rebuild_model(self, model: type[OCSFBaseModel]) -> None:
        """Try to rebuild a single model with available dependencies.

        Args:
            model: Model to rebuild
        """
        from typing import Any

        # Build namespace with all available models + typing imports
        namespace = {
            "Any": Any,
            **dict(self._model_cache),
        }

        # Also include any enum classes attached to models
        for model_cls in self._model_cache.values():
            # Get nested enum classes (e.g., FileActivity.ActivityId)
            # Use __dict__ to avoid triggering Pydantic validation
            for _attr_name, attr in model_cls.__dict__.items():
                try:
                    if isinstance(attr, type) and issubclass(attr, IntEnum):
                        namespace[attr.__name__] = attr
                except (TypeError, AttributeError):
                    # Skip attributes that can't be checked
                    pass

        # Silently ignore - dependencies might not be loaded yet
        # Model will work with model_construct() and will be rebuilt
        # when dependencies are loaded
        with contextlib.suppress(Exception):
            model.model_rebuild(_types_namespace=namespace)

    def rebuild_all(self) -> None:
        """Force rebuild of all models in cache.

        This can be called by users after importing all models they need
        to ensure all forward references are resolved.
        """
        from typing import Any

        namespace = {
            "Any": Any,
            **dict(self._model_cache),
        }

        for model in self._model_cache.values():
            with contextlib.suppress(Exception):
                model.model_rebuild(_types_namespace=namespace, force=True)

    def __dir__(self) -> list[str]:
        """Support for dir() and autocomplete.

        Returns:
            List of all available model names in this version
        """
        return sorted(self.factory.get_all_model_names())

    def __repr__(self) -> str:
        """String representation of the module."""
        return f"<module 'ocsf.v{self.version.replace('.', '_')}' (JIT)>"
