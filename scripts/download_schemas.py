#!/usr/bin/env python3
"""Download OCSF schema JSON files for JIT model creation.

This script downloads schemas from the OCSF schema repository and
saves them to src/ocsf/schemas/ for bundling with the package.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tarfile
from io import BytesIO
from pathlib import Path
from typing import Any

import httpx

# OCSF versions to download
VERSIONS = [
    "1.7.0",
    "1.6.0",
    "1.5.0",
    "1.4.0",
    "1.3.0",
    "1.2.0",
    "1.1.0",
    "1.0.0",
]

# Base URL for schema files in the OCSF schema repo
# Note: We use the schema cache that was already downloaded by generate.py
SCHEMA_CACHE_DIR = Path(__file__).parent.parent / ".schema_cache"
OUTPUT_DIR = Path(__file__).parent.parent / "src" / "ocsf" / "schemas"


def load_cached_schema(version: str) -> dict | None:
    """Load schema from local cache directory.

    Args:
        version: Version string (e.g., "1.7.0")

    Returns:
        Parsed schema dict, or None if not found
    """
    schema_file = SCHEMA_CACHE_DIR / f"ocsf-schema-v{version}.json"

    if schema_file.exists():
        print("    [*] Found schema in cache")
        with open(schema_file, encoding="utf-8") as f:
            return json.load(f)

    return None


def save_cached_schema(version: str, schema: dict) -> None:
    """Save schema to local cache directory.

    Args:
        version: Version string (e.g., "1.7.0")
        schema: Schema dictionary

    Returns:
        None
    """
    schema_file = SCHEMA_CACHE_DIR / f"ocsf-schema-v{version}.json"

    with open(schema_file, "w", encoding="utf-8") as f:
        return json.dump(schema, f)

    return None


def save_schema(version: str, schema: dict) -> Path:
    """Save schema to output directory.

    Args:
        version: Version string (e.g., "1.7.0")
        schema: Schema dictionary

    Returns:
        Path to saved file
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / f"v{version.replace('.', '_')}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)

    return output_file


def download_schema(version: str) -> dict:
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
    URL_PATTERNS = [
        f"https://github.com/ocsf/ocsf-schema/archive/refs/tags/{version}.tar.gz",
        f"https://github.com/ocsf/ocsf-schema/archive/refs/tags/v{version}.tar.gz",
    ]

    if version == "dev":
        URL_PATTERNS = ["https://github.com/ocsf/ocsf-schema/archive/refs/heads/main.tar.gz"]

    for url in URL_PATTERNS:
        # Download tarball
        print(f"    [*] Downloading {url}...", end=" ")

        with httpx.Client(follow_redirects=True, timeout=60.0) as client:
            response = client.get(url)
            print(response.status_code)
            if response.status_code == 404:
                continue
            response.raise_for_status()

        # Extract and parse
        return _parse_tarball(response.content, version)

    raise ValueError(version)


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
                print(f"    [!] Warning: Could not parse {rel_path}")
                continue

            # Categorize by path
            item_type = rel_path.split("/")[0]
            if item_type in ("events", "objects", "categories"):
                if "name" in data:
                    schema[item_type][data["name"]] = data
                else:
                    # Use filename without extension as key
                    filename = Path(rel_path).stem
                    schema[item_type][filename] = data
            elif rel_path == "dictionary.json":
                schema["dictionary"] = data
            elif rel_path == "categories.json":
                schema["categories_meta"] = data
            elif rel_path == "version.json":
                schema["version_info"] = data

    # Enums are typically defined in dictionary.json under "types"
    # or inline within object/event attribute definitions
    if "dictionary" in schema and "types" in schema["dictionary"]:
        for name, type_def in schema["dictionary"]["types"].items():
            if "enum" in type_def:
                schema["enums"][name] = type_def

    return schema


def compute_checksum(file_path: Path) -> str:
    """Compute SHA256 checksum of a file.

    Args:
        file_path: Path to file

    Returns:
        Hex digest of SHA256 checksum
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def main() -> int:
    """Download and save all OCSF schemas.

    Returns:
        Exit code (0 for success)
    """
    print("Downloading OCSF schemas...")
    print(f"Source: {SCHEMA_CACHE_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print()

    os.makedirs(SCHEMA_CACHE_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    checksums = {}
    success_count = 0
    skip_count = 0

    for version in VERSIONS:
        verstr = "dev" if version == "dev" else f"v{version}"
        print(f"[+] Processing {verstr}...")

        # Load from cache unless it's dev
        schema = load_cached_schema(version) if version != "dev" else None

        if schema is None:
            try:
                schema = download_schema(version)
            except Exception:
                skip_count += 1
                continue
            else:
                if version == "dev":
                    version = schema["version_info"]["version"]
                    schema["version"] = version
                save_cached_schema(version, schema)

        # Save to output directory
        output_file = save_schema(version, schema)

        # Compute checksum
        checksum = compute_checksum(output_file)
        checksums[version] = checksum

        # Get stats
        num_objects = len(schema.get("objects", {}))
        num_events = len(schema.get("events", {}))

        print(f"    [*] OK ({num_objects} objects, {num_events} events)")
        success_count += 1

    # Save checksums
    checksums_file = OUTPUT_DIR / "checksums.json"
    with open(checksums_file, "w", encoding="utf-8") as f:
        json.dump(checksums, f, indent=2)

    print()
    print(f"    [*] Downloaded {success_count} schemas ({skip_count} skipped)")
    print(f"    [*] Checksums saved to {checksums_file}")

    return 0 if success_count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
