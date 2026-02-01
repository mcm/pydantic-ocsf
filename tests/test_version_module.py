#!/usr/bin/env python3
"""Test OCSFVersionModule behavior."""

import pytest

from ocsf._version_module import OCSFVersionModule


class TestVersionModule:
    """Test version module functionality."""

    def test_module_creation(self):
        """Test creating a version module."""
        module = OCSFVersionModule("ocsf.v1_7_0", "1.7.0")

        assert module.__name__ == "ocsf.v1_7_0"
        assert module.version == "1.7.0"
        assert hasattr(module, "schema")
        assert hasattr(module, "factory")

    def test_getattr_creates_model(self):
        """Test __getattr__ creates models on demand."""
        import ocsf.v1_7_0

        # First access should create the model
        User = ocsf.v1_7_0.objects.User
        assert User is not None
        assert User.__name__ == "User"

    def test_model_caching(self):
        """Test that models are cached after first creation."""
        import ocsf.v1_7_0

        # First access
        User1 = ocsf.v1_7_0.objects.User

        # Second access should return cached model
        User2 = ocsf.v1_7_0.objects.User

        assert User1 is User2, "Should return same cached instance"

    def test_forward_reference_resolution(self):
        """Test that forward references are resolved."""
        import ocsf.v1_7_0

        User = ocsf.v1_7_0.objects.User

        # Check field annotations are resolved
        account_field = User.model_fields.get("account")
        assert account_field is not None

        # Forward ref should be resolved (not a string)
        annotation = account_field.annotation
        # After rebuild, should be actual type or Union, not ForwardRef
        assert annotation is not None

    def test_dir_autocomplete(self):
        """Test __dir__ returns available models."""
        import ocsf.v1_7_0

        available = dir(ocsf.v1_7_0)

        # Should include namespace modules only
        assert "objects" in available
        assert "events" in available

        # Should NOT include individual model names
        assert "User" not in available
        assert "FileActivity" not in available

        # Should be sorted
        assert available == sorted(available)

    def test_repr(self):
        """Test module string representation."""
        import ocsf.v1_7_0

        repr_str = repr(ocsf.v1_7_0)
        assert "ocsf.v1_7_0" in repr_str
        assert "JIT" in repr_str or "jit" in repr_str.lower()

    def test_private_attribute_raises_error(self):
        """Test accessing private attributes raises AttributeError."""
        import ocsf.v1_7_0

        with pytest.raises(AttributeError):
            _ = ocsf.v1_7_0._some_private_attr

    def test_invalid_model_name_raises_error(self):
        """Test accessing non-existent model raises AttributeError."""
        import ocsf.v1_7_0

        with pytest.raises(AttributeError) as exc_info:
            _ = ocsf.v1_7_0.NonExistentModel

        assert "NonExistentModel" in str(exc_info.value)

    def test_dependency_loading(self):
        """Test that dependencies are loaded automatically."""
        import ocsf.v1_7_0

        # Import a model with dependencies
        User = ocsf.v1_7_0.objects.User

        # Its dependencies should be loaded (with namespaced keys)
        assert (
            "objects:Account" in ocsf.v1_7_0._model_cache or "Account" in ocsf.v1_7_0._model_cache
        )

    def test_rebuild_all(self):
        """Test rebuild_all() method."""
        import ocsf.v1_7_0

        # Load some models
        User = ocsf.v1_7_0.objects.User
        Account = ocsf.v1_7_0.objects.Account

        # Rebuild all should not raise errors
        ocsf.v1_7_0.rebuild_all()

        # Models should still work
        user = User(name="test", uid="123")
        assert user.name == "test"

    def test_multiple_model_access(self):
        """Test accessing multiple models in sequence."""
        import ocsf.v1_7_0

        # Access multiple models
        models = [
            ocsf.v1_7_0.objects.User,
            ocsf.v1_7_0.objects.Account,
            ocsf.v1_7_0.objects.File,
            ocsf.v1_7_0.objects.Process,
            ocsf.v1_7_0.objects.Device,
        ]

        # All should be valid model classes
        for model in models:
            assert model is not None
            assert hasattr(model, "model_fields")
            assert hasattr(model, "model_validate")

    def test_cache_contains_loaded_models(self):
        """Test that _model_cache tracks loaded models."""
        import ocsf.v1_7_0

        initial_cache_size = len(ocsf.v1_7_0._model_cache)

        # Load a new model
        _ = ocsf.v1_7_0.objects.User

        # Cache should have grown or stayed same (User might already be loaded)
        assert len(ocsf.v1_7_0._model_cache) >= initial_cache_size

        # User should be in cache (with namespaced key)
        assert "objects:User" in ocsf.v1_7_0._model_cache


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
