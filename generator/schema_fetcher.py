"""Fetch OCSF schema from GitHub."""

from __future__ import annotations

import json
import tarfile
from io import BytesIO
from pathlib import Path
from typing import Any

import httpx

GITHUB_TARBALL_URL = "https://github.com/ocsf/ocsf-schema/archive/refs/tags/{version}.tar.gz"

SUPPORTED_VERSIONS = ["1.7.0", "1.6.0", "1.5.0", "v1.2.0", "v1.1.0", "v1.0.0"]


def fetch_schema(version: str, cache_dir: Path | None = None) -> dict[str, Any]:
    """Fetch and parse OCSF schema for a given version.

    Args:
        version: OCSF version tag (e.g., "v1.7.0")
        cache_dir: Optional directory to cache downloaded schema

    Returns:
        Dictionary containing parsed schema with keys:
        - "version": str
        - "categories": dict
        - "events": dict
        - "objects": dict
        - "enums": dict (extracted from events/objects)
    """
    if version not in SUPPORTED_VERSIONS:
        raise ValueError(f"Unsupported version: {version}. Supported: {SUPPORTED_VERSIONS}")

    # Check cache first
    if cache_dir:
        cache_file = cache_dir / f"ocsf-schema-{version}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text())

    # Download tarball
    url = GITHUB_TARBALL_URL.format(version=version)
    print(f"Downloading {url}...")

    with httpx.Client(follow_redirects=True, timeout=60.0) as client:
        response = client.get(url)
        response.raise_for_status()

    # Extract and parse
    schema = _parse_tarball(response.content, version)

    # Cache if requested
    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(schema, indent=2))

    return schema


def _parse_tarball(content: bytes, version: str) -> dict[str, Any]:
    """Parse OCSF schema from tarball content."""
    schema: dict[str, Any] = {
        "version": version,
        "categories": {},
        "events": {},
        "objects": {},
        "enums": {},
    }

    with tarfile.open(fileobj=BytesIO(content), mode="r:gz") as tar:
        # Find the root directory name (e.g., "ocsf-schema-1.7.0")
        root_dir = None
        for member in tar.getmembers():
            if member.isdir() and member.name.count("/") == 0:
                root_dir = member.name
                break

        if not root_dir:
            raise ValueError("Could not find root directory in tarball")

        # Parse each schema component
        for member in tar.getmembers():
            if not member.isfile() or not member.name.endswith(".json"):
                continue

            # Get path relative to root
            rel_path = member.name[len(root_dir) + 1 :]

            # Extract and parse JSON
            f = tar.extractfile(member)
            if f is None:
                continue

            try:
                data = json.loads(f.read().decode("utf-8"))
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {rel_path}")
                continue

            # Categorize by path
            if rel_path.startswith("events/"):
                _add_to_schema(schema["events"], rel_path, data)
            elif rel_path.startswith("objects/"):
                _add_to_schema(schema["objects"], rel_path, data)
            elif rel_path.startswith("categories/"):
                _add_to_schema(schema["categories"], rel_path, data)
            elif rel_path == "dictionary.json":
                schema["dictionary"] = data
            elif rel_path == "categories.json":
                schema["categories_meta"] = data
            elif rel_path == "version.json":
                schema["version_info"] = data

    # Extract enums from dictionary and objects
    _extract_enums(schema)

    return schema


def _add_to_schema(target: dict[str, Any], path: str, data: dict[str, Any]) -> None:
    """Add parsed JSON to schema, keyed by the 'name' field if present."""
    if "name" in data:
        target[data["name"]] = data
    else:
        # Use filename without extension as key
        filename = Path(path).stem
        target[filename] = data


def _extract_enums(schema: dict[str, Any]) -> None:
    """Extract enum definitions from dictionary and inline definitions."""
    # Enums are typically defined in dictionary.json under "types"
    # or inline within object/event attribute definitions
    if "dictionary" in schema and "types" in schema["dictionary"]:
        for name, type_def in schema["dictionary"]["types"].items():
            if "enum" in type_def:
                schema["enums"][name] = type_def


if __name__ == "__main__":
    # Test the fetcher
    import sys

    version = sys.argv[1] if len(sys.argv) > 1 else "v1.2.0"
    cache = Path(".schema_cache")

    schema = fetch_schema(version, cache_dir=cache)

    print(f"\nSchema {version} summary:")
    print(f"  Categories: {len(schema.get('categories', {}))}")
    print(f"  Events: {len(schema.get('events', {}))}")
    print(f"  Objects: {len(schema.get('objects', {}))}")
    print(f"  Enums: {len(schema.get('enums', {}))}")
