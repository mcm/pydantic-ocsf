"""Tests for automatic type_uid calculation from activity_id."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from ocsf.v1_7_0.events import FileActivity, IncidentFinding


class TestTypeUidAutoCalculation:
    """Test automatic type_uid calculation."""

    def test_type_uid_auto_calculated_from_activity_id(self):
        """Test that type_uid is automatically calculated when only activity_id is provided."""
        data = {
            "time": 1706000000000,
            "activity_id": 1,  # CREATE
            "severity_id": 4,
            "actor": {
                "user": {"name": "alice", "type_id": 0},
                "session": {"uid": "session-123"},
            },
            "device": {"hostname": "laptop01", "type_id": 0},
            "file": {"name": "test.txt", "type_id": 0},
            "metadata": {
                "version": "1.7.0",
                "product": {"name": "Test", "vendor_name": "Test"},
            },
        }

        event = FileActivity.model_validate(data)

        # type_uid should be auto-calculated as class_uid * 100 + activity_id
        assert event.type_uid == 101  # 1 * 100 + 1
        assert event.activity_id == FileActivity.ActivityId.CREATE

    def test_type_uid_validated_when_both_provided(self):
        """Test that type_uid is validated against activity_id when both are provided."""
        data = {
            "time": 1706000000000,
            "activity_id": 2,  # READ
            "type_uid": 102,  # Correct value: 1 * 100 + 2
            "severity_id": 4,
            "actor": {
                "user": {"name": "alice", "type_id": 0},
                "session": {"uid": "session-123"},
            },
            "device": {"hostname": "laptop01", "type_id": 0},
            "file": {"name": "test.txt", "type_id": 0},
            "metadata": {
                "version": "1.7.0",
                "product": {"name": "Test", "vendor_name": "Test"},
            },
        }

        event = FileActivity.model_validate(data)
        assert event.type_uid == 102
        assert event.activity_id == FileActivity.ActivityId.READ

    def test_type_uid_mismatch_raises_error(self):
        """Test that mismatched type_uid and activity_id raises an error."""
        data = {
            "time": 1706000000000,
            "activity_id": 1,  # CREATE
            "type_uid": 104,  # Wrong! Should be 101 for CREATE
            "severity_id": 4,
            "actor": {
                "user": {"name": "alice", "type_id": 0},
                "session": {"uid": "session-123"},
            },
            "device": {"hostname": "laptop01", "type_id": 0},
            "file": {"name": "test.txt", "type_id": 0},
            "metadata": {
                "version": "1.7.0",
                "product": {"name": "Test", "vendor_name": "Test"},
            },
        }

        with pytest.raises(ValidationError) as exc_info:
            FileActivity.model_validate(data)

        error_msg = str(exc_info.value)
        assert "type_uid=104 does not match calculated value" in error_msg
        assert "101" in error_msg  # Expected value

    def test_type_name_auto_populated_from_activity_name(self):
        """Test that type_name is automatically set based on activity."""
        data = {
            "time": 1706000000000,
            "activity_id": 1,  # CREATE
            "activity_name": "Create",
            "severity_id": 4,
            "actor": {
                "user": {"name": "alice", "type_id": 0},
                "session": {"uid": "session-123"},
            },
            "device": {"hostname": "laptop01", "type_id": 0},
            "file": {"name": "test.txt", "type_id": 0},
            "metadata": {
                "version": "1.7.0",
                "product": {"name": "Test", "vendor_name": "Test"},
            },
        }

        event = FileActivity.model_validate(data)

        assert event.type_uid == 101
        assert event.type_name == "Create"  # Same as activity_name

    def test_type_name_from_type_uid_only(self):
        """Test that type_name is extrapolated when only type_uid is provided."""
        data = {
            "time": 1706000000000,
            "activity_id": 1,  # Required for calculation
            "type_uid": 101,
            # type_name not provided
            "severity_id": 4,
            "actor": {
                "user": {"name": "alice", "type_id": 0},
                "session": {"uid": "session-123"},
            },
            "device": {"hostname": "laptop01", "type_id": 0},
            "file": {"name": "test.txt", "type_id": 0},
            "metadata": {
                "version": "1.7.0",
                "product": {"name": "Test", "vendor_name": "Test"},
            },
        }

        event = FileActivity.model_validate(data)

        assert event.type_uid == 101
        assert event.type_name == "Create"  # Extrapolated from type_uid

    def test_type_uid_works_with_activity_name_only(self):
        """Test that type_uid is calculated when only activity_name is provided."""
        data = {
            "time": 1706000000000,
            "activity_name": "Delete",  # Only activity_name provided
            # activity_id will be extrapolated to 4
            # type_uid will be calculated as 1*100+4=104
            "severity_id": 4,
            "actor": {
                "user": {"name": "alice", "type_id": 0},
                "session": {"uid": "session-123"},
            },
            "device": {"hostname": "laptop01", "type_id": 0},
            "file": {"name": "test.txt", "type_id": 0},
            "metadata": {
                "version": "1.7.0",
                "product": {"name": "Test", "vendor_name": "Test"},
            },
        }

        event = FileActivity.model_validate(data)

        assert event.activity_id == FileActivity.ActivityId.DELETE
        assert event.activity_name == "Delete"
        assert event.type_uid == 104  # 1 * 100 + 4
        assert event.type_name == "Delete"

    def test_different_event_class_uid(self):
        """Test type_uid calculation for a different event class."""
        # IncidentFinding has class_uid=5
        data = {
            "time": 1706000000000,
            "activity_id": 1,  # CREATE
            "severity_id": 4,
            "status_id": 1,
            "finding_info_list": [{"title": "Test", "uid": "finding-123"}],
            "metadata": {
                "version": "1.7.0",
                "product": {"name": "Test", "vendor_name": "Test"},
            },
        }

        event = IncidentFinding.model_validate(data)

        # type_uid should be 5 * 100 + 1 = 501
        assert event.type_uid == 501
        assert event.activity_id == IncidentFinding.ActivityId.CREATE

    def test_event_type_id_enum_values(self):
        """Test that EventTypeId enum has correct values."""
        # FileActivity class_uid = 1
        assert FileActivity.EventTypeId.CREATE == 101
        assert FileActivity.EventTypeId.READ == 102
        assert FileActivity.EventTypeId.UPDATE == 103
        assert FileActivity.EventTypeId.DELETE == 104
        assert FileActivity.EventTypeId.RENAME == 105

        # IncidentFinding class_uid = 5
        assert IncidentFinding.EventTypeId.CREATE == 501
        assert IncidentFinding.EventTypeId.UPDATE == 502
        assert IncidentFinding.EventTypeId.CLOSE == 503

    def test_event_type_id_enum_label(self):
        """Test that EventTypeId enum has correct labels."""
        assert FileActivity.EventTypeId.CREATE.label == "Create"
        assert FileActivity.EventTypeId.READ.label == "Read"
        assert FileActivity.EventTypeId.DELETE.label == "Delete"

        assert IncidentFinding.EventTypeId.CREATE.label == "Create"
        assert IncidentFinding.EventTypeId.UPDATE.label == "Update"
        assert IncidentFinding.EventTypeId.CLOSE.label == "Close"

    def test_type_uid_enum_construction(self):
        """Test constructing EventTypeId enum from integer values."""
        # Create from int
        type_id = FileActivity.EventTypeId(101)
        assert type_id == FileActivity.EventTypeId.CREATE
        assert type_id.label == "Create"

        # Create from string label
        type_id = FileActivity.EventTypeId("Read")
        assert type_id == FileActivity.EventTypeId.READ
        assert type_id.value == 102
