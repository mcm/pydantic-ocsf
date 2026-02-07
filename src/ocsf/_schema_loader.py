"""Schema loading and caching utilities for OCSF JIT model factory."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ocsf._exceptions import SchemaError, VersionNotFoundError


class SchemaLoader:
    """Load and cache OCSF schemas from bundled JSON files.

    Schemas are loaded on-demand and cached in memory for subsequent access.
    """

    def __init__(self, schema_dir: Path | None = None) -> None:
        """Initialize the schema loader.

        Args:
            schema_dir: Directory containing schema JSON files.
                       If None, uses default bundled schemas.
        """
        if schema_dir is None:
            # Default to schemas/ directory next to this file
            schema_dir = Path(__file__).parent / "schemas"

        self.schema_dir = schema_dir
        self._cache: dict[str, dict[str, Any]] = {}
        self._available_versions: list[str] | None = None

    def get_available_versions(self) -> list[str]:
        """Get list of available OCSF versions.

        Returns:
            Sorted list of version strings (e.g., ["1.0.0", "1.7.0"])
        """
        if self._available_versions is not None:
            return self._available_versions

        if not self.schema_dir.exists():
            self._available_versions = []
            return []

        versions = []
        for file in self.schema_dir.glob("v*.json"):
            # Extract version from filename (e.g., "v1_7_0.json" -> "1.7.0")
            version_str = file.stem[1:]  # Remove 'v' prefix
            version = version_str.replace("_", ".")
            versions.append(version)

        self._available_versions = sorted(versions)
        return self._available_versions

    def load_schema(self, version: str) -> dict[str, Any]:
        """Load schema for a specific version.

        Args:
            version: Version string (e.g., "1.7.0")

        Returns:
            Parsed schema dictionary

        Raises:
            VersionNotFoundError: If version is not available
            SchemaError: If schema file is invalid or corrupted
        """
        # Check cache first
        if version in self._cache:
            return self._cache[version]

        # Verify version exists
        available = self.get_available_versions()
        if version not in available:
            raise VersionNotFoundError(version, available)

        # Load schema from file
        schema_file = self.schema_dir / f"v{version.replace('.', '_')}.json"

        try:
            with open(schema_file, encoding="utf-8") as f:
                schema = json.load(f)
        except json.JSONDecodeError as e:
            raise SchemaError(f"Invalid JSON: {e}", version) from e
        except OSError as e:
            raise SchemaError(f"Cannot read schema file: {e}", version) from e

        # Validate basic schema structure
        if not isinstance(schema, dict):
            raise SchemaError("Schema must be a JSON object", version)

        if "objects" not in schema and "events" not in schema:
            raise SchemaError("Schema must contain 'objects' or 'events'", version)

        # Cache and return
        self._cache[version] = schema
        return schema

    def clear_cache(self) -> None:
        """Clear the schema cache."""
        self._cache.clear()
        self._available_versions = None


# Global schema loader instance
_global_loader: SchemaLoader | None = None


def get_schema_loader() -> SchemaLoader:
    """Get the global schema loader instance.

    Returns:
        The global SchemaLoader instance
    """
    global _global_loader
    if _global_loader is None:
        _global_loader = SchemaLoader()
    return _global_loader
