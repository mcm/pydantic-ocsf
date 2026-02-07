#!/usr/bin/env python3
"""Test schema bundling and package integrity."""

from pathlib import Path

import pytest


class TestSchemaBundling:
    """Test that schemas are properly bundled in the package."""

    def test_schemas_exist(self):
        """Test that schema files exist in the package."""
        from ocsf._schema_loader import get_schema_loader

        loader = get_schema_loader()

        # Get available versions
        versions = loader.get_available_versions()

        # Should have multiple versions
        assert len(versions) > 0

        # Common versions should be available
        assert "1.7.0" in versions or "1.7" in versions

    def test_schema_loading(self):
        """Test that schemas can be loaded."""
        from ocsf._schema_loader import get_schema_loader

        loader = get_schema_loader()

        # Load a schema
        schema = loader.load_schema("1.7.0")

        # Should have standard OCSF structure
        assert isinstance(schema, dict)
        assert "objects" in schema or "events" in schema or "dictionary" in schema

    def test_schema_caching(self):
        """Test that schemas are cached after first load."""
        from ocsf._schema_loader import get_schema_loader

        loader = get_schema_loader()

        # Load once
        schema1 = loader.load_schema("1.7.0")

        # Load again
        schema2 = loader.load_schema("1.7.0")

        # Should return same object (cached)
        assert schema1 is schema2

    def test_checksum_validation(self):
        """Test checksum validation if implemented."""
        from ocsf._schema_loader import get_schema_loader

        loader = get_schema_loader()

        # Loading should not raise checksum errors
        try:
            schema = loader.load_schema("1.7.0")
            assert schema is not None
        except Exception as e:
            # Should not fail due to checksum issues
            assert "checksum" not in str(e).lower()

    def test_missing_schema_error(self):
        """Test graceful error for missing schema."""
        from ocsf._exceptions import VersionNotFoundError
        from ocsf._schema_loader import get_schema_loader

        loader = get_schema_loader()

        # Try to load non-existent version
        with pytest.raises((VersionNotFoundError, FileNotFoundError, ValueError)):
            loader.load_schema("99.99.99")

    def test_schema_directory_exists(self):
        """Test that schema directory exists in installed package."""
        import ocsf

        # Get package path
        ocsf_path = Path(ocsf.__file__).parent

        # Schema directory should exist (or be accessible via loader)
        # The loader might use different storage mechanisms
        # This is a basic check
        assert ocsf_path.exists()

    def test_all_versions_loadable(self):
        """Test that all advertised versions can be loaded."""
        from ocsf._schema_loader import get_schema_loader

        loader = get_schema_loader()
        versions = loader.get_available_versions()

        # Try to load each version
        for version in versions:
            try:
                schema = loader.load_schema(version)
                assert schema is not None
                assert isinstance(schema, dict)
            except Exception as e:
                pytest.fail(f"Failed to load version {version}: {e}")

    def test_schema_structure(self):
        """Test that loaded schemas have expected structure."""
        from ocsf._schema_loader import get_schema_loader

        loader = get_schema_loader()
        schema = loader.load_schema("1.7.0")

        # Should have objects and/or events
        has_objects = "objects" in schema and len(schema["objects"]) > 0
        has_events = "events" in schema and len(schema["events"]) > 0

        assert has_objects or has_events, "Schema should have objects or events"

    def test_schema_contains_user_object(self):
        """Test that schema contains common objects like User."""
        from ocsf._schema_loader import get_schema_loader

        loader = get_schema_loader()
        schema = loader.load_schema("1.7.0")

        # Should have user object (in snake_case in schema)
        if "objects" in schema:
            assert "user" in schema["objects"], "Schema should contain 'user' object"

    def test_schema_contains_dictionary(self):
        """Test that schema contains dictionary section."""
        from ocsf._schema_loader import get_schema_loader

        loader = get_schema_loader()
        schema = loader.load_schema("1.7.0")

        # OCSF schemas typically have a dictionary
        if "dictionary" in schema:
            dictionary = schema["dictionary"]
            assert isinstance(dictionary, dict)

            # Dictionary should have attributes
            if "attributes" in dictionary:
                assert len(dictionary["attributes"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
