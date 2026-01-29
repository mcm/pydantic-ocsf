#!/usr/bin/env python3
"""Generate OCSF Pydantic models for all supported versions."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from generator.schema_parser import parse_schema
from generator.model_generator import generate_models


VERSIONS = ["1.7.0", "1.6.0", "1.5.0", "v1.2.0", "v1.1.0", "v1.0.0"]
OUTPUT_DIR = project_root / "src" / "ocsf"
CACHE_DIR = project_root / ".schema_cache"


def get_package_version(latest_ocsf_version: str) -> str:
    """Generate package version in format {ocsf_version}.{date}.

    Args:
        latest_ocsf_version: Latest OCSF version (e.g., "1.7.0")

    Returns:
        Version string like "1.7.0.20260129"
    """
    # Strip 'v' prefix if present
    ocsf_ver = latest_ocsf_version.lstrip("v")
    # Get current date in YYYYMMDD format
    date_str = datetime.now().strftime("%Y%m%d")
    return f"{ocsf_ver}.{date_str}"


def main() -> None:
    """Generate models for all OCSF versions."""
    for version in VERSIONS:
        print(f"\n{'=' * 60}")
        print(f"Generating OCSF {version}")
        print("=" * 60)

        schema = parse_schema(version, cache_dir=CACHE_DIR)
        generate_models(schema, OUTPUT_DIR)

    # Generate package version based on latest OCSF version and current date
    latest_version = VERSIONS[0]  # First version in list is the latest
    package_version = get_package_version(latest_version)

    print(f"\nPackage version: {package_version}")

    # Update top-level __init__.py to export from latest version
    init_content = f'''"""Pydantic models for the Open Cybersecurity Schema Framework (OCSF).

This package provides type-safe, validated models for OCSF security events.

Example:
    from ocsf import FileActivity, File, SeverityId

    event = FileActivity(
        time=1706000000000,
        activity_id=1,
        severity_id=SeverityId.INFORMATIONAL,
        file=File(name="test.txt"),
    )

The default imports are from OCSF 1.7.0 (latest). For other versions:
    from ocsf.v1_7_0 import FileActivity  # OCSF 1.7.0
    from ocsf.v1_6_0 import FileActivity  # OCSF 1.6.0
    from ocsf.v1_5_0 import FileActivity  # OCSF 1.5.0
    from ocsf.v1_2_0 import FileActivity  # OCSF 1.2.0
    from ocsf.v1_1_0 import FileActivity  # OCSF 1.1.0
    from ocsf.v1_0_0 import FileActivity  # OCSF 1.0.0
"""

from ocsf._base import OCSFBaseModel as OCSFBaseModel
from ocsf.v1_7_0 import *  # noqa: F401, F403

__version__ = "{package_version}"
'''
    (OUTPUT_DIR / "__init__.py").write_text(init_content)

    # Format generated code
    print("\nFormatting generated code...")
    subprocess.run(["ruff", "check", "--fix", str(OUTPUT_DIR)], check=True)
    subprocess.run(["ruff", "format", str(OUTPUT_DIR)], check=True)

    print("\nGeneration complete!")


if __name__ == "__main__":
    main()
