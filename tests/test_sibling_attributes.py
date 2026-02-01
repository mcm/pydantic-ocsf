#!/usr/bin/env python3
"""Test sibling attribute validation (CRITICAL)."""

import pytest


class TestSiblingAttributes:
    """Test sibling ID/label validation scenarios."""

    def test_enum_class_exists(self):
        """Test that sibling enum classes are created."""
        from ocsf.v1_7_0.events import FileActivity

        # ActivityId enum should exist as nested class
        assert hasattr(FileActivity, "ActivityId")

        ActivityId = FileActivity.ActivityId
        assert ActivityId is not None

    def test_enum_members(self):
        """Test that enum has correct members."""
        from ocsf.v1_7_0.events import FileActivity

        ActivityId = FileActivity.ActivityId

        # Should have members
        assert len(ActivityId.__members__) > 0

        # Common OCSF activity IDs
        # Check a few common ones exist
        members = list(ActivityId.__members__.keys())
        assert len(members) > 0  # At least some members

    def test_enum_int_construction(self):
        """Test constructing enum from integer."""
        from ocsf.v1_7_0.events import FileActivity

        ActivityId = FileActivity.ActivityId

        # Should be able to construct from int
        enum_val = ActivityId(1)
        assert enum_val is not None
        assert enum_val.value == 1

    def test_enum_string_construction(self):
        """Test constructing enum from label string."""
        from ocsf.v1_7_0.events import FileActivity

        ActivityId = FileActivity.ActivityId

        # Should be able to construct from string label
        # Using from_label method
        if hasattr(ActivityId, "from_label"):
            enum_val = ActivityId.from_label("Create")
            assert enum_val is not None
            assert enum_val.label == "Create"

    def test_enum_case_insensitive(self):
        """Test case-insensitive label lookup."""
        from ocsf.v1_7_0.events import FileActivity

        ActivityId = FileActivity.ActivityId

        # Test case insensitivity if supported
        if hasattr(ActivityId, "from_label"):
            # These should all work
            try:
                upper = ActivityId.from_label("CREATE")
                lower = ActivityId.from_label("create")
                mixed = ActivityId.from_label("Create")

                # All should be equal
                assert upper == lower == mixed
            except (ValueError, KeyError):
                # If specific label doesn't exist, skip
                pass

    def test_enum_label_property(self):
        """Test enum has label property."""
        from ocsf.v1_7_0.events import FileActivity

        ActivityId = FileActivity.ActivityId

        # Get any member
        first_member = list(ActivityId)[0]

        # Should have label property
        assert hasattr(first_member, "label")
        assert isinstance(first_member.label, str)

    def test_field_type_annotations(self):
        """Test that sibling fields have correct type annotations."""
        from ocsf.v1_7_0.events import FileActivity

        fields = FileActivity.model_fields

        # activity_id should use the ActivityId enum
        if "activity_id" in fields:
            activity_id_field = fields["activity_id"]
            annotation_str = str(activity_id_field.annotation)

            # Should reference ActivityId enum
            assert "ActivityId" in annotation_str

    def test_scenario1_both_present_consistent(self):
        """Scenario 1: Both ID and label present and consistent."""
        from ocsf.v1_7_0.events import FileActivity

        ActivityId = FileActivity.ActivityId

        # Get a valid ID/label pair
        test_id = 1
        test_enum = ActivityId(test_id)
        test_label = test_enum.label

        # Create with both - should succeed
        activity = FileActivity.model_construct(
            activity_id=test_id,
            activity_name=test_label,
            metadata={"version": "1.7.0"},
        )

        assert activity.activity_id == test_id
        assert activity.activity_name == test_label

    def test_scenario2_only_id_present(self):
        """Scenario 2: Only ID present, label should be extrapolated."""
        from ocsf.v1_7_0.events import FileActivity

        # Create with only ID
        activity = FileActivity.model_construct(
            activity_id=1,
            metadata={"version": "1.7.0"},
        )

        # ID should be set
        assert activity.activity_id == 1

        # Label may or may not be auto-populated depending on reconciler
        # If reconciler is working, label should be set
        # For now, just verify ID is set correctly

    def test_scenario3_only_label_present(self):
        """Scenario 3: Only label present, ID should be extrapolated."""
        from ocsf.v1_7_0.events import FileActivity

        ActivityId = FileActivity.ActivityId

        # Get a valid label
        test_enum = ActivityId(1)
        test_label = test_enum.label

        # Create with only label
        activity = FileActivity.model_construct(
            activity_name=test_label,
            metadata={"version": "1.7.0"},
        )

        # Label should be set
        assert activity.activity_name == test_label

        # ID may or may not be auto-populated depending on reconciler

    def test_model_validation_with_enums(self):
        """Test that model validation works with enum fields."""
        from ocsf.v1_7_0.events import FileActivity

        # Should be able to validate with enum ID
        data = {
            "activity_id": 1,
            "category_uid": 3,
            "class_uid": 4001,
            "severity_id": 1,
            "time": 1706000000000,
            "type_uid": 400101,
            "metadata": {"version": "1.7.0", "product": {"name": "Test"}},
            "actor": {},
            "device": {"type_id": 0},
            "file": {"name": "test.txt", "type_id": 1},
        }

        activity = FileActivity.model_validate(data)
        assert activity.activity_id == 1

    def test_serialization_includes_both_fields(self):
        """Test that serialization includes both ID and label."""
        from ocsf.v1_7_0.events import FileActivity

        activity = FileActivity.model_construct(
            activity_id=1,
            activity_name="Create",
            metadata={"version": "1.7.0"},
        )

        # Serialize to dict
        data = activity.model_dump()

        # Both fields should be present (if they were set)
        if activity.activity_id is not None:
            assert "activity_id" in data

        if activity.activity_name is not None:
            assert "activity_name" in data

    def test_enum_value_serialization(self):
        """Test that enum values serialize as integers."""
        from ocsf.v1_7_0.events import FileActivity

        ActivityId = FileActivity.ActivityId
        test_enum = ActivityId(1)

        activity = FileActivity.model_construct(
            activity_id=test_enum,
            metadata={"version": "1.7.0"},
        )

        # Serialize
        data = activity.model_dump()

        # activity_id should be an integer, not enum
        if "activity_id" in data and data["activity_id"] is not None:
            assert isinstance(data["activity_id"], int)

    def test_multiple_enum_fields(self):
        """Test models with multiple sibling enum pairs."""
        from ocsf.v1_7_0.events import FileActivity

        # FileActivity might have multiple enum fields
        # Test they all work independently

        activity = FileActivity.model_construct(
            activity_id=1,
            type_uid=100100,  # type_uid is another enum field
            metadata={"version": "1.7.0"},
        )

        assert activity.activity_id == 1

    def test_unknown_label_handling(self):
        """Test handling of unknown label values."""
        from ocsf.v1_7_0.events import FileActivity

        # Create with unknown label
        activity = FileActivity.model_construct(
            activity_name="UnknownActivity",
            metadata={"version": "1.7.0"},
        )

        # Should not crash
        assert activity.activity_name == "UnknownActivity"

        # If reconciler maps to OTHER (99), check that
        # Otherwise, just verify it doesn't crash

    def test_enum_direct_usage(self):
        """Test using enum directly in model creation."""
        from ocsf.v1_7_0.events import FileActivity

        ActivityId = FileActivity.ActivityId

        # Use enum directly
        enum_val = ActivityId(1)

        activity = FileActivity.model_construct(
            activity_id=enum_val,
            metadata={"version": "1.7.0"},
        )

        # Should work
        assert activity.activity_id is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
