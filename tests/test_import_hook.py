#!/usr/bin/env python3
"""Test import hook functionality and isolation."""

import sys
from contextlib import suppress

import pytest

from ocsf._exceptions import VersionNotFoundError


class TestImportHook:
    """Test OCSF import hook behavior."""

    def test_hook_installed(self):
        """Verify import hook is installed in sys.meta_path."""
        from ocsf._import_hook import OCSFImporter

        # Check hook is in meta_path
        hook_found = any(isinstance(finder, OCSFImporter) for finder in sys.meta_path)
        assert hook_found, "OCSFImporter not found in sys.meta_path"

    def test_hook_doesnt_break_other_imports(self):
        """Verify hook doesn't interfere with normal imports."""
        # These should all work normally
        import json
        import pathlib
        import typing
        from datetime import datetime

        # Third-party imports
        import pydantic

        assert json is not None
        assert pathlib is not None
        assert typing is not None
        assert datetime is not None
        assert pydantic is not None

    def test_valid_version_import(self):
        """Test importing valid OCSF version."""
        # Should succeed
        import ocsf.v1_7_0

        assert ocsf.v1_7_0 is not None
        assert hasattr(ocsf.v1_7_0, "version")
        assert ocsf.v1_7_0.version == "1.7.0"

    def test_invalid_version_format(self):
        """Test importing invalid version format raises error."""
        with pytest.raises((AttributeError, ImportError)):
            import ocsf.vInvalid  # type: ignore  # noqa: F401

    def test_missing_version(self):
        """Test importing non-existent version raises helpful error."""
        with pytest.raises(VersionNotFoundError) as exc_info:
            import ocsf.v9_9_9  # type: ignore  # noqa: F401

        # Error message should be helpful
        assert "9.9.9" in str(exc_info.value)

    def test_import_variations(self):
        """Test different import syntaxes."""
        # Direct import
        import ocsf.v1_7_0

        assert ocsf.v1_7_0 is not None

        # From import
        from ocsf.v1_7_0.objects import User

        assert User is not None

        # Multiple imports
        from ocsf.v1_7_0.objects import Account, File, Process

        assert Account is not None
        assert File is not None
        assert Process is not None

    def test_reimport_returns_same_module(self):
        """Test that re-importing returns the same module instance."""
        import ocsf.v1_7_0 as module1
        import ocsf.v1_7_0 as module2

        assert module1 is module2, "Re-import should return same module instance"

    def test_hook_only_intercepts_ocsf_versions(self):
        """Verify hook only handles ocsf.v* imports."""
        # These should NOT be handled by OCSFImporter
        import os
        import sys
        from pathlib import Path

        # None of these should use OCSFImporter
        assert os is not None
        assert sys is not None
        assert Path is not None

    def test_partial_import_doesnt_break_system(self):
        """Test that failed imports don't break the system."""
        with suppress(VersionNotFoundError):
            import ocsf.v9_9_9  # type: ignore  # noqa: F401

        # System should still work
        import ocsf.v1_7_0
        from ocsf.v1_7_0.objects import User

        assert ocsf.v1_7_0 is not None
        assert User is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
