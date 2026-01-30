"""Integration tests for sibling attribute reconciliation."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from ocsf.v1_7_0.events import FileActivity


class TestSiblingReconciliation:
    """Test sibling attribute reconciliation during parsing."""

    @pytest.fixture
    def base_event_data(self):
        """Minimal valid event data with all required fields."""
        return {
            "time": 1706000000000,
            # type_uid is auto-calculated from activity_id, not specified here
            "actor": {
                "user": {"name": "alice", "type_id": 0},  # UNKNOWN
                "session": {"uid": "session-123"},
            },
            "device": {
                "hostname": "laptop01",
                "type_id": 0,  # UNKNOWN
            },
            "file": {
                "name": "test.txt",
                "type_id": 0,  # UNKNOWN
            },
            "metadata": {
                "version": "1.7.0",
                "product": {"name": "Test", "vendor_name": "TestVendor"},
            },
        }

    # --- Both present scenarios ---

    def test_both_present_matching(self, base_event_data):
        """Test both ID and label present with matching values."""
        data = {
            **base_event_data,
            "activity_id": 1,
            "activity_name": "Create",
            "severity_id": 4,  # Required field
        }
        event = FileActivity.model_validate(data)
        assert event.activity_id == FileActivity.ActivityId.CREATE
        assert event.activity_name == "Create"

    def test_both_present_matching_different_case(self, base_event_data):
        """Label with different casing should be normalized to canonical."""
        data = {
            **base_event_data,
            "activity_id": 1,
            "activity_name": "create",  # lowercase
            "severity_id": 4,  # Required field
        }
        event = FileActivity.model_validate(data)
        assert event.activity_name == "Create"  # Canonical casing

    def test_both_present_mismatched_raises(self, base_event_data):
        """Test that mismatched ID and label raise ValidationError."""
        data = {
            **base_event_data,
            "activity_id": 1,  # CREATE
            "activity_name": "Delete",  # Mismatch!
            "severity_id": 4,  # Required field
        }
        with pytest.raises(ValidationError) as exc_info:
            FileActivity.model_validate(data)
        error_msg = str(exc_info.value)
        assert "does not match" in error_msg

    def test_both_present_other_with_custom_label(self, base_event_data):
        """Test with a known ID and label pair."""
        # FileActivity doesn't have OTHER, so test a normal value
        data = {
            **base_event_data,
            "activity_id": 4,  # DELETE
            "activity_name": "Delete",
            "severity_id": 4,  # Required field
        }
        event = FileActivity.model_validate(data)
        assert event.activity_id == 4
        assert event.activity_name == "Delete"

    # --- Only ID scenarios ---

    def test_only_id_extrapolates_label(self, base_event_data):
        """Test that providing only ID extrapolates the label."""
        data = {
            **base_event_data,
            "activity_id": 1,  # CREATE
            "severity_id": 4,  # Required field
        }
        event = FileActivity.model_validate(data)
        assert event.activity_name == "Create"

    def test_only_id_invalid_raises(self, base_event_data):
        """Test that invalid ID value raises ValidationError."""
        data = {
            **base_event_data,
            "activity_id": 9999,  # Invalid
            "severity_id": 4,  # Required field
        }
        with pytest.raises(ValidationError) as exc_info:
            FileActivity.model_validate(data)
        error_msg = str(exc_info.value)
        assert "Invalid activity_id" in error_msg

    def test_only_id_other_extrapolates_other_label(self, base_event_data):
        """Test ID extrapolation for standard values."""
        # Note: FileActivity.ActivityId doesn't have OTHER (99), so we test a normal value
        data = {
            **base_event_data,
            "activity_id": 2,  # READ
            "severity_id": 4,  # Required field
        }
        event = FileActivity.model_validate(data)
        assert event.activity_name == "Read"

    # --- Only label scenarios ---

    def test_only_label_extrapolates_id(self, base_event_data):
        """Test that providing only label extrapolates the ID."""
        data = {
            **base_event_data,
            "activity_name": "Create",
            "severity_id": 4,  # Required field
        }
        event = FileActivity.model_validate(data)
        assert event.activity_id == FileActivity.ActivityId.CREATE

    def test_only_label_case_insensitive(self, base_event_data):
        """Test that label lookup is case-insensitive."""
        data = {
            **base_event_data,
            "activity_name": "create",  # lowercase
            "severity_id": 4,  # Required field
        }
        event = FileActivity.model_validate(data)
        assert event.activity_id == FileActivity.ActivityId.CREATE
        assert event.activity_name == "Create"  # Canonical

    def test_only_label_unknown_raises_error(self, base_event_data):
        """Test that unknown label raises error if no OTHER exists."""
        # FileActivity.ActivityId doesn't have OTHER, so unknown labels should raise
        from pydantic import ValidationError

        data = {
            **base_event_data,
            "activity_name": "Quarantine File",  # Unknown label
            "severity_id": 4,  # Required field
        }
        with pytest.raises(ValidationError) as exc_info:
            FileActivity.model_validate(data)
        error_msg = str(exc_info.value)
        assert "Unknown activity_name" in error_msg or "has no OTHER" in error_msg

    def test_json_parsing_unknown_label_maps_to_other(self):
        """Test that JSON parsing with unknown label maps to OTHER (lenient)."""
        from ocsf.v1_7_0.events import IncidentFinding

        # IncidentFinding.VerdictId HAS OTHER, so unknown labels should map to it
        data = {
            "time": 1706000000000,
            # type_uid auto-calculated from activity_id (5*100+1=501)
            "activity_id": 1,
            "severity_id": 4,
            "status_id": 1,
            "finding_info_list": [{"title": "Test", "uid": "finding-123"}],
            "metadata": {
                "version": "1.7.0",
                "product": {"name": "Test", "vendor_name": "Test"},
            },
            "verdict": "Custom Security Assessment",  # Unknown label
        }

        # JSON parsing should be lenient and map to OTHER
        event = IncidentFinding.model_validate(data)
        assert event.verdict_id == 99
        assert event.verdict == "Other"
        # Verify type_uid was auto-calculated
        assert event.type_uid == 501  # class_uid=5 * 100 + activity_id=1

    def test_direct_enum_construction_is_strict(self):
        """Test that direct enum construction raises ValueError for unknown labels."""
        from ocsf.v1_7_0.events import IncidentFinding

        # Direct construction should be STRICT, even if OTHER exists
        with pytest.raises(ValueError, match="Unknown VerdictId label"):
            IncidentFinding.VerdictId("Custom Security Assessment")


class TestSiblingReconciliationEdgeCases:
    """Edge cases and error conditions."""

    @pytest.fixture
    def base_event_data(self):
        """Minimal valid event data."""
        return {
            "time": 1706000000000,
            # type_uid is auto-calculated from activity_id, not specified here
            "actor": {
                "user": {"name": "alice", "type_id": 0},  # UNKNOWN
                "session": {"uid": "session-123"},
            },
            "device": {
                "hostname": "laptop01",
                "type_id": 0,  # UNKNOWN
            },
            "file": {
                "name": "test.txt",
                "type_id": 0,  # UNKNOWN
            },
            "metadata": {
                "version": "1.7.0",
                "product": {"name": "Test", "vendor_name": "TestVendor"},
            },
        }

    def test_none_values_treated_as_missing(self, base_event_data):
        """Explicit None should be treated same as missing."""
        data = {
            **base_event_data,
            "activity_id": 1,
            "activity_name": None,  # Explicit None
            "severity_id": 4,  # Required field
        }
        event = FileActivity.model_validate(data)
        assert event.activity_name == "Create"  # Extrapolated

    def test_both_id_and_label_none(self, base_event_data):
        """When both are None, no reconciliation should occur."""
        data = {
            **base_event_data,
            "activity_id": 1,  # Required for type_uid calculation
            "status_id": None,  # Test None for optional sibling pair
            "status": None,
            "severity_id": 4,  # Required field
        }
        event = FileActivity.model_validate(data)
        # Status should remain None
        assert event.status_id is None
        assert event.status is None
        # type_uid should be auto-calculated
        assert event.type_uid == 101  # class_uid=1 * 100 + activity_id=1
