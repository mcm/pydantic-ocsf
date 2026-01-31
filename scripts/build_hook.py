"""Hatchling build hook to download schemas before building package."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from hatchling.plugin import hookimpl


@hookimpl
def hatch_register_build_hook() -> type[BuildHook]:
    """Register the build hook."""
    return BuildHook


class BuildHook:
    """Build hook to download schemas."""

    PLUGIN_NAME = "custom"

    def __init__(self, root: str, config: dict) -> None:
        """Initialize the build hook.

        Args:
            root: Project root directory
            config: Build hook configuration
        """
        self.root = Path(root)
        self.config = config

    def initialize(self, version: str, build_data: dict) -> None:
        """Run before building the package.

        Args:
            version: Package version being built
            build_data: Build metadata
        """
        print("Running build hook: downloading schemas and generating stubs...")

        # Step 1: Run the download script
        script = self.root / "scripts" / "download_schemas.py"
        result = subprocess.run(  # noqa: S603
            [sys.executable, str(script)],
            cwd=self.root,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print("ERROR: Failed to download schemas")
            print(result.stdout)
            print(result.stderr)
            raise RuntimeError("Schema download failed")

        print(result.stdout)
        print("✓ Schemas downloaded successfully")

        # Step 2: Generate stub files
        stub_script = self.root / "scripts" / "regenerate_stubs.py"
        result = subprocess.run(  # noqa: S603
            [sys.executable, str(stub_script)],
            cwd=self.root,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print("ERROR: Failed to generate stubs")
            print(result.stdout)
            print(result.stderr)
            raise RuntimeError("Stub generation failed")

        print(result.stdout)
        print("✓ Type stubs generated successfully")
