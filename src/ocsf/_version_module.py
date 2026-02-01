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
        self.__path__ = []  # Mark as package

        # Namespace module references
        self._objects_module: Any = None
        self._events_module: Any = None

        # Load schema
        loader = get_schema_loader()
        self.schema = loader.load_schema(version)

        # Create model factory
        self.factory = ModelFactory(self.schema, version)

    def __getattr__(self, name: str) -> Any:
        """Only expose namespace modules, not individual models.

        Args:
            name: Attribute name ("objects", "events", or model name)

        Returns:
            Namespace module for "objects" or "events"

        Raises:
            AttributeError: If accessing a model directly (breaking change)
        """
        # Handle namespace module access
        if name == "objects":
            if self._objects_module is None:
                from ocsf._namespace_module import OCSFNamespaceModule

                self._objects_module = OCSFNamespaceModule(
                    f"{self.__name__}.objects", self, "objects"
                )
            return self._objects_module
        elif name == "events":
            if self._events_module is None:
                from ocsf._namespace_module import OCSFNamespaceModule

                self._events_module = OCSFNamespaceModule(f"{self.__name__}.events", self, "events")
            return self._events_module

        # No direct model access - raise helpful error
        raise AttributeError(
            f"module '{self.__name__}' has no attribute '{name}'. "
            f"Use 'from {self.__name__}.objects import {name}' or "
            f"'from {self.__name__}.events import {name}' instead."
        )

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
            # Check if dependency is already loaded (with any namespace prefix)
            is_loaded = any(
                cache_key == dep_name or cache_key.endswith(f":{dep_name}")
                for cache_key in self._model_cache
            )

            if not is_loaded:
                # Try to load from objects namespace first, then events
                loaded = False
                for namespace in ("objects", "events"):
                    try:
                        namespace_module = getattr(self, namespace)
                        _ = getattr(namespace_module, dep_name)
                        loaded = True
                        break
                    except AttributeError:
                        continue

                # If still not loaded, it might be a base class or special model
                if not loaded:
                    with contextlib.suppress(AttributeError):
                        # Try direct access (for base classes like BaseEvent, Object, etc.)
                        pass

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
        # Include both namespaced keys and non-namespaced model names
        namespace: dict[str, Any] = {"Any": Any}

        # Add models with both namespaced and non-namespaced keys
        for cache_key, model_cls in self._model_cache.items():
            namespace[cache_key] = model_cls  # e.g., "objects:User"
            # Also add without namespace prefix for Pydantic's forward ref resolution
            if ":" in cache_key:
                _, model_name = cache_key.split(":", 1)
                namespace[model_name] = model_cls  # e.g., "User"

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

        # Build namespace with both namespaced and non-namespaced keys
        namespace: dict[str, Any] = {"Any": Any}

        for cache_key, model_cls in self._model_cache.items():
            namespace[cache_key] = model_cls
            # Also add without namespace prefix for Pydantic's forward ref resolution
            if ":" in cache_key:
                _, model_name = cache_key.split(":", 1)
                namespace[model_name] = model_cls

        for model in self._model_cache.values():
            with contextlib.suppress(Exception):
                model.model_rebuild(_types_namespace=namespace, force=True)

    def __dir__(self) -> list[str]:
        """Support for dir() and autocomplete.

        Returns:
            List of namespace modules only
        """
        return ["objects", "events"]

    def __repr__(self) -> str:
        """String representation of the module."""
        return f"<module 'ocsf.v{self.version.replace('.', '_')}' (JIT)>"
