"""Namespace module for OCSF objects and events separation."""

from __future__ import annotations

from types import ModuleType
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ocsf._version_module import OCSFVersionModule


class OCSFNamespaceModule(ModuleType):
    """Namespace module that filters access to objects or events."""

    def __init__(self, name: str, parent: OCSFVersionModule, namespace_type: str) -> None:
        """Initialize namespace module.

        Args:
            name: Full module name (e.g., "ocsf.v1_7_0.objects")
            parent: Parent OCSFVersionModule instance
            namespace_type: "objects" or "events"
        """
        super().__init__(name)
        self._parent = parent
        self._namespace_type = namespace_type
        self.__file__ = f"<ocsf-jit:{parent.version}:{namespace_type}>"
        self.__path__ = []

    def __getattr__(self, name: str) -> Any:
        """Get model from parent cache if in correct namespace."""
        if name.startswith("_"):
            raise AttributeError(f"module '{self.__name__}' has no attribute '{name}'")

        # Use namespaced cache key to handle collisions (e.g., Finding object vs Finding event)
        cache_key = f"{self._namespace_type}:{name}"

        # Check if model exists in parent cache
        if cache_key in self._parent._model_cache:
            return self._parent._model_cache[cache_key]

        # Verify model exists in this namespace before creating
        if not self._is_in_namespace(name):
            # Provide helpful error
            other = "events" if self._namespace_type == "objects" else "objects"
            raise AttributeError(
                f"'{name}' is not in {self._namespace_type} namespace. "
                f"Try importing from ocsf.{self._parent.version.replace('.', '_')}.{other}"
            )

        # Model not in cache - create it via parent with namespace filter
        try:
            model = self._parent.factory.create_model(
                name, self._parent._model_cache, namespace_filter=self._namespace_type
            )
        except Exception as e:
            raise AttributeError(f"module '{self.__name__}' has no attribute '{name}'") from e

        # Cache with namespaced key and load dependencies via parent
        self._parent._model_cache[cache_key] = model
        self._parent._load_dependencies(model)
        self._parent._try_rebuild_model(model)

        return model

    def _is_in_namespace(self, name: str) -> bool:
        """Check if model belongs to this namespace."""
        from ocsf._utils import pascal_to_snake

        schema_name = pascal_to_snake(name)
        schema = self._parent.schema

        if self._namespace_type == "objects":
            return schema_name in schema.get("objects", {})
        else:  # events
            return schema_name in schema.get("events", {})

    def __dir__(self) -> list[str]:
        """Return only models from this namespace."""
        from ocsf._utils import snake_to_pascal

        schema = self._parent.schema
        if self._namespace_type == "objects":
            names = schema.get("objects", {}).keys()
        else:
            names = schema.get("events", {}).keys()

        return sorted([snake_to_pascal(name) for name in names])
