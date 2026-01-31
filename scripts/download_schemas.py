#!/usr/bin/env python3
"""Download OCSF schema JSON files for JIT model creation.

This script downloads schemas from the OCSF schema repository and
saves them to src/ocsf/schemas/ for bundling with the package.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

# OCSF versions to download
VERSIONS = [
    "1.7.0",
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
    # Try different filename patterns
    patterns = [
        SCHEMA_CACHE_DIR / f"ocsf-schema-{version}.json",
        SCHEMA_CACHE_DIR / f"ocsf-schema-v{version}.json",
    ]

    for schema_file in patterns:
        if schema_file.exists():
            with open(schema_file, encoding="utf-8") as f:
                return json.load(f)

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

    if not SCHEMA_CACHE_DIR.exists():
        print(f"ERROR: Schema cache directory not found: {SCHEMA_CACHE_DIR}")
        print("Run 'python scripts/generate.py' first to download schemas.")
        return 1

    checksums = {}
    success_count = 0
    skip_count = 0

    for version in VERSIONS:
        print(f"Processing v{version}...", end=" ")

        # Load from cache
        schema = load_cached_schema(version)

        if schema is None:
            print("SKIP (not in cache)")
            skip_count += 1
            continue

        # Save to output directory
        output_file = save_schema(version, schema)

        # Compute checksum
        checksum = compute_checksum(output_file)
        checksums[version] = checksum

        # Get stats
        num_objects = len(schema.get("objects", {}))
        num_events = len(schema.get("events", {}))

        print(f"OK ({num_objects} objects, {num_events} events)")
        success_count += 1

    # Save checksums
    checksums_file = OUTPUT_DIR / "checksums.json"
    with open(checksums_file, "w", encoding="utf-8") as f:
        json.dump(checksums, f, indent=2)

    print()
    print(f"Downloaded {success_count} schemas ({skip_count} skipped)")
    print(f"Checksums saved to {checksums_file}")

    return 0 if success_count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
