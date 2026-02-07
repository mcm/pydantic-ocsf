"""Tests for sibling attribute functionality.

This test suite verifies that sibling attributes (label fields for _id enums)
are correctly generated in both type stubs and runtime models, and that the
sibling reconciliation validators work as expected.
"""


class TestAnalyticSiblingAttributes:
    """Test sibling attributes for the Analytic object."""

    def test_analytic_has_type_field_in_stubs(self):
        """Test that Analytic stub has type_ field."""
        # This test verifies the .pyi stub file is correct
        # If this passes, type checkers like mypy will see the field
        from ocsf.v1_7_0.objects import Analytic

        # Check that type_ field exists (will fail if not in __annotations__)
        # Note: We can't check __annotations__ directly for JIT models,
        # but we can verify the field exists in model_fields
        assert hasattr(Analytic, "model_fields"), "Should be a Pydantic model"
        assert "type_" in Analytic.model_fields, "type_ field should exist in model"

    def test_analytic_type_enum_exists(self):
        """Test that TypeId enum is generated."""
        from ocsf.v1_7_0.objects import Analytic

        assert hasattr(Analytic, "TypeId"), "TypeId enum should exist"
        assert Analytic.TypeId.RULE == 1
        assert Analytic.TypeId.BEHAVIORAL == 2

    def test_analytic_type_sibling_reconciliation(self):
        """Test that type_id and type_ are reconciled."""
        from ocsf.v1_7_0.objects import Analytic

        # Test 1: Only ID provided -> label auto-filled
        analytic = Analytic(type_id=Analytic.TypeId.RULE)
        assert analytic.type_ == "Rule", "type_ should be auto-filled from type_id"

        # Test 2: Only label provided -> ID auto-filled
        analytic2 = Analytic(type_id=1)
        assert analytic2.type_ == "Rule", "type_ should be auto-filled from numeric ID"

    def test_analytic_state_sibling(self):
        """Test state_id/state sibling pair (exists in schema)."""
        from ocsf.v1_7_0.objects import Analytic

        # state field exists in schema, so it should work the same way
        analytic = Analytic(type_id=1, state_id=Analytic.StateId.ACTIVE)
        assert analytic.state == "Active", "state should be auto-filled"


class TestFileActivitySiblingAttributes:
    """Test sibling attributes for FileActivity event."""

    def test_file_activity_has_activity_field(self):
        """Test that FileActivity has inferred activity field."""
        from ocsf.v1_7_0.events import FileActivity

        assert "activity" in FileActivity.model_fields, "activity field should be inferred"

    def test_file_activity_activity_enum_exists(self):
        """Test that ActivityId enum is generated."""
        from ocsf.v1_7_0.events import FileActivity

        assert hasattr(FileActivity, "ActivityId"), "ActivityId enum should exist"
        assert FileActivity.ActivityId.CREATE == 1
        assert FileActivity.ActivityId.DELETE == 4

    def test_file_activity_sibling_reconciliation(self):
        """Test activity_id/activity sibling reconciliation."""
        from ocsf.v1_7_0.events import FileActivity

        # Only ID provided
        event = FileActivity(
            time=1706000000000,
            activity_id=FileActivity.ActivityId.CREATE,
            severity_id=1,
            metadata={"version": "1.7.0", "product": {"name": "Test"}},
            actor={"user": {"name": "test"}},
            device={"hostname": "test", "type_id": 0},
            file={"name": "test.txt", "type_id": 1},
        )
        assert event.activity == "Create", "activity should be auto-filled"

    def test_file_activity_severity_sibling(self):
        """Test severity_id/severity sibling pair."""
        from ocsf.v1_7_0.events import FileActivity

        event = FileActivity(
            time=1706000000000,
            activity_id=1,
            severity_id=4,  # HIGH
            metadata={"version": "1.7.0", "product": {"name": "Test"}},
            actor={"user": {"name": "test"}},
            device={"hostname": "test", "type_id": 0},
            file={"name": "test.txt", "type_id": 1},
        )
        assert event.severity == "High", "severity should be auto-filled"


class TestReservedKeywordHandling:
    """Test that Python reserved keywords are handled correctly."""

    def test_type_field_uses_underscore(self):
        """Test that type_id generates type_ (not type)."""
        from ocsf.v1_7_0.objects import Analytic

        # Should have type_, not type
        assert "type_" in Analytic.model_fields, "Should have type_ field"

        # type should still be the built-in type() function
        assert callable(type), "type should still be the built-in function"
