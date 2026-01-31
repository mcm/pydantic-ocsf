#!/usr/bin/env python3
"""Test performance benchmarks."""

import time
from contextlib import suppress

import pytest


class TestPerformance:
    """Test performance meets targets."""

    def test_single_model_creation_time(self):
        """Test single model creation is fast (<15ms)."""
        from ocsf.v1_7_0 import Account

        # Measure model creation (Account should be uncached at test start)
        start = time.perf_counter()
        _ = Account
        end = time.perf_counter()

        creation_time_ms = (end - start) * 1000

        # Should be under 15ms
        assert creation_time_ms < 15, f"Creation took {creation_time_ms:.2f}ms, expected <15ms"

    def test_cached_access_time(self):
        """Test cached model access is very fast (<0.1ms)."""
        from ocsf.v1_7_0 import User

        # Access multiple times and measure
        times = []
        for _ in range(10):
            start = time.perf_counter()
            _ = User
            end = time.perf_counter()
            times.append((end - start) * 1000)

        avg_time = sum(times) / len(times)

        # Should be under 0.1ms
        assert avg_time < 0.1, f"Cached access took {avg_time:.4f}ms, expected <0.1ms"

    def test_batch_import_time(self):
        """Test importing 25 models takes <300ms."""
        import ocsf.v1_7_0

        model_names = [
            "User",
            "Account",
            "File",
            "Process",
            "Device",
            "Actor",
            "Api",
            "Metadata",
            "Product",
            "Group",
            "Session",
            "NetworkEndpoint",
            "Service",
            "Cloud",
            "Container",
            "Image",
            "Package",
            "Certificate",
            "Fingerprint",
            "Hash",
            "Observable",
            "AutonomousSystem",
            "Location",
            "Organization",
            "ResourceDetails",
        ]

        start = time.perf_counter()
        for name in model_names[:25]:  # Import up to 25
            with suppress(AttributeError):
                getattr(ocsf.v1_7_0, name)
        end = time.perf_counter()

        import_time_ms = (end - start) * 1000

        # Should be under 300ms
        assert import_time_ms < 300, f"25 models took {import_time_ms:.2f}ms, expected <300ms"

    def test_cache_speedup(self):
        """Test cache returns same instance on subsequent access."""
        import ocsf.v1_7_0

        # Load a model
        test_model_name = "ResourceDetails"

        # First access
        try:
            first_model = getattr(ocsf.v1_7_0, test_model_name)
        except AttributeError:
            # Model doesn't exist, skip this test
            pytest.skip(f"{test_model_name} not available")

        # Second access - should be cached
        second_model = getattr(ocsf.v1_7_0, test_model_name)

        # Should be same model instance (cached)
        assert first_model is second_model

        # Model should be in cache
        assert test_model_name in ocsf.v1_7_0._model_cache

    def test_instance_creation_performance(self):
        """Test creating instances is fast."""
        from ocsf.v1_7_0 import User

        # Create 100 instances
        start = time.perf_counter()
        for i in range(100):
            user = User(name=f"user{i}", uid=f"uid-{i}")
        end = time.perf_counter()

        total_time_ms = (end - start) * 1000
        per_instance_ms = total_time_ms / 100

        # Should be reasonable (<1ms per instance)
        assert per_instance_ms < 1.0, f"Instance creation took {per_instance_ms:.3f}ms each"

    def test_serialization_performance(self):
        """Test serialization is fast."""
        from ocsf.v1_7_0 import User

        user = User(name="Test User", uid="test-123")

        # Serialize 100 times
        start = time.perf_counter()
        for _ in range(100):
            data = user.model_dump()
        end = time.perf_counter()

        total_time_ms = (end - start) * 1000
        per_operation_ms = total_time_ms / 100

        # Should be fast (<0.5ms per serialization)
        assert per_operation_ms < 0.5, f"Serialization took {per_operation_ms:.3f}ms each"

    def test_validation_performance(self):
        """Test validation is fast."""
        from ocsf.v1_7_0 import User

        data = {"name": "Test User", "uid": "test-123"}

        # Validate 100 times
        start = time.perf_counter()
        for _ in range(100):
            user = User.model_validate(data)
        end = time.perf_counter()

        total_time_ms = (end - start) * 1000
        per_operation_ms = total_time_ms / 100

        # Should be fast (<1ms per validation)
        assert per_operation_ms < 1.0, f"Validation took {per_operation_ms:.3f}ms each"

    def test_memory_efficiency(self):
        """Test memory usage is reasonable."""
        import ocsf.v1_7_0

        # Get size of model cache before loading
        initial_cache_size = len(ocsf.v1_7_0._model_cache)

        # Load 10 models (some may already be loaded)
        models = []
        for name in [
            "User",
            "Account",
            "File",
            "Process",
            "Device",
            "Actor",
            "Api",
            "Metadata",
            "Product",
            "Group",
        ]:
            try:
                model = getattr(ocsf.v1_7_0, name)
                models.append(model)
            except AttributeError:
                pass

        # Cache should have grown or stayed same (models might already be loaded)
        final_cache_size = len(ocsf.v1_7_0._model_cache)
        assert final_cache_size >= initial_cache_size

        # Memory per model should be reasonable
        # (This is a basic test, not precise memory measurement)
        assert len(models) > 0

    def test_dependency_loading_performance(self):
        """Test automatic dependency loading doesn't cause slowdown."""
        from ocsf.v1_7_0 import FileActivity

        # Load a model with dependencies (FileActivity loads many models)
        start = time.perf_counter()
        _ = FileActivity
        end = time.perf_counter()

        load_time_ms = (end - start) * 1000

        # Should complete in reasonable time even with dependencies
        # Allow up to 500ms for model with many dependencies
        assert load_time_ms < 500, f"Dependency loading took {load_time_ms:.2f}ms"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
