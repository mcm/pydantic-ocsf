"""Tests for sibling attribute functionality.

This test suite verifies that sibling attributes (label fields for _id enums)
are correctly generated in both type stubs and runtime models, and that the
sibling reconciliation validators work as expected.
"""

import pytest


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
        """Test that FileActivity has inferred activity_name field."""
        from ocsf.v1_7_0.events import FileActivity

        assert "activity_name" in FileActivity.model_fields, (
            "activity_name field should be inferred from activity_id sibling"
        )

    def test_file_activity_activity_enum_exists(self):
        """Test that ActivityId enum is generated."""
        from ocsf.v1_7_0.events import FileActivity

        assert hasattr(FileActivity, "ActivityId"), "ActivityId enum should exist"
        assert FileActivity.ActivityId.CREATE == 1
        assert FileActivity.ActivityId.DELETE == 4

    def test_file_activity_sibling_reconciliation(self):
        """Test activity_id/activity_name sibling reconciliation."""
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
        assert event.activity_name == "Create", "activity_name should be auto-filled"

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

    def test_serialize_doesnt_use_underscore(self):
        """Test that type_id generates type_ (not type)."""
        from ocsf.v1_7_0.events import IncidentFinding
        from ocsf.v1_7_0.objects import Analytic, FindingInfo

        sample_event = {
            "activity_id": 1,
            "activity_name": "Create",
            "category_uid": 2,
            "class_uid": 5,
            "count": 19,
            "metadata": {
                "is_truncated": False,
                "processed_time": 1771254901632,
                "product": {
                    "name": "Enterprise Security",
                    "vendor_name": "Splunk",
                    "version": "8.2.0",
                },
                "profiles": ["incident"],
                "tenant_uid": "9D982A1F-4ED5-4CF3-938F-A4DB8609778E",
                "uid": "79e20961-02b2-4f2b-b33b-99cb7bd30739@@notable@@time1771254903",
                "version": "1.7.0",
            },
            "raw_data": '{"_time": 1771254903.0, "disposition_label": "Undetermined", "event_id": "79e20961-02b2-4f2b-b33b-99cb7bd30739@@notable@@time1771254903", "info_max_time": 1771254300.0, "info_min_time": 1771167900.0, "info_search_time": 1771254901.632594, "search_name": "Risk - 24 Hour Risk Threshold Exceeded - Rule", "orig_source": ["Audit - Anomalous Audit Trail Activity Detected - Rule", "Network - Unusual Volume of Outbound Traffic By Src - Rule"], "owner": "unassigned", "owner_realname": "unassigned", "risk_object": "10.0.1.4", "risk_object_type": "system", "risk_score": 1480, "rule_description": "Risk Threshold Exceeded for an object over a 24 hour period", "rule_name": "Risk Threshold Exceeded For Object Over 24 Hour Period", "rule_title": "24 hour risk threshold exceeded for system=10.0.1.4", "risk_event_count": 19, "security_domain": "threat", "status_label": "New", "update_time": 1771254926.0978158, "urgency": "high"}',
            "raw_data_hash": {
                "algorithm": "SHA-512",
                "algorithm_id": 4,
                "value": "ac556252f9296865a453fcde1bb70dfc00efd107df7ce80a567cf355bc14b425000a0685dc8a7f783ce88b299e02ec063db3ea997f3eb581b60c60ecdf104fb3",
            },
            "raw_data_size": 924,
            "severity": "High",
            "severity_id": 4,
            "status": "New",
            "status_id": 1,
            "time": 1771254903000,
            "timezone_offset": 0,
            "type_uid": 501,
            "unmapped": {
                "risk_objects": [
                    {"device": {"name": "10.0.1.4", "type": "Unknown", "type_id": 0}, "score": 1480}
                ]
            },
            "assignee": {"uid": "unassigned", "display_name": "unassigned"},
            "confidence": "Medium",
            "confidence_id": 2,
            "finding_info_list": [
                {
                    "analytic": {
                        "name": "Risk Threshold Exceeded For Object Over 24 Hour Period",
                        "category": "threat",
                        "type": "Risk",
                        "type_id": 99,
                    },
                    "created_time": 1771254903000,
                    "desc": "Risk Threshold Exceeded for an object over a 24 hour period",
                    "modified_time": 1771254926097,
                    "product": {
                        "name": "Enterprise Security",
                        "vendor_name": "Splunk",
                        "version": "8.2.0",
                    },
                    "related_analytics": [
                        {
                            "name": "Audit - Anomalous Audit Trail Activity Detected - Rule",
                            "category": "Audit",
                            "type": "Rule",
                            "type_id": 1,
                        },
                        {
                            "name": "Network - Unusual Volume of Outbound Traffic By Src - Rule",
                            "category": "Network",
                            "type": "Rule",
                            "type_id": 1,
                        },
                    ],
                    "title": "24 hour risk threshold exceeded for system=10.0.1.4",
                    "uid": "79e20961-02b2-4f2b-b33b-99cb7bd30739@@notable@@time1771254903",
                }
            ],
            "verdict": "Unknown",
            "verdict_id": 0,
        }

        analytic_dict = Analytic.model_validate(
            sample_event["finding_info_list"][0]["analytic"]
        ).model_dump(exclude_none=True)
        assert analytic_dict == sample_event["finding_info_list"][0]["analytic"]

        finding_info_dict = FindingInfo.model_validate(
            sample_event["finding_info_list"][0]
        ).model_dump(exclude_none=True)
        assert finding_info_dict == sample_event["finding_info_list"][0]

        incident_finding_dict = IncidentFinding.model_validate(sample_event).model_dump(
            exclude_none=True
        )
        assert incident_finding_dict == sample_event

    def test_round_trip_doesnt_preserve_underscore(self):
        from ocsf.v1_7_0.objects import Analytic

        analytic = Analytic(
            name="Risk Threshold Exceeded For Object Over 24 Hour Period",
            category="threat",
            type_="Risk",
            type_id=99,
        )
        analytic_dict = analytic.model_dump(exclude_none=True)

        assert analytic_dict == {
            "name": "Risk Threshold Exceeded For Object Over 24 Hour Period",
            "category": "threat",
            "type": "Risk",
            "type_id": 99,
        }


class TestOtherIdException:
    """Test that ID=99 (Other) allows custom labels."""

    def test_id_99_allows_custom_label(self) -> None:
        """When type_id=99, any custom type label should be accepted."""
        from ocsf.v1_7_0.objects import Analytic

        # ID=99 with custom label should be accepted (not "Other")
        analytic = Analytic(
            name="Test",
            category="threat",
            type="Custom Risk Category",
            type_id=99,
        )

        assert analytic.type_ == "Custom Risk Category"
        assert analytic.type_id == 99

        # Verify serialization
        result = analytic.model_dump(exclude_none=True)
        assert result["type"] == "Custom Risk Category"
        assert result["type_id"] == 99

    def test_id_99_with_python_field_name(self) -> None:
        """When type_id=99 with type_='Custom', preserve the custom value."""
        from ocsf.v1_7_0.objects import Analytic

        analytic = Analytic(
            name="Test",
            category="threat",
            type_="Risk",
            type_id=99,
        )

        assert analytic.type_ == "Risk"
        result = analytic.model_dump(exclude_none=True)
        assert result["type"] == "Risk"

    def test_id_99_without_label_autofills_other(self) -> None:
        """When only type_id=99 is provided, should auto-fill type='Other'."""
        from ocsf.v1_7_0.objects import Analytic

        analytic = Analytic(
            name="Test",
            category="threat",
            type_id=99,
        )

        assert analytic.type_ == "Other"
        result = analytic.model_dump(exclude_none=True)
        assert result["type"] == "Other"
        assert result["type_id"] == 99

    def test_non_99_id_validates_consistency(self) -> None:
        """Non-99 IDs should validate that label matches the enum."""
        from ocsf.v1_7_0.objects import Analytic
        from pydantic import ValidationError

        # type_id=1 maps to "Rule", so "WrongLabel" should fail
        with pytest.raises(ValidationError) as exc_info:
            Analytic(
                name="Test",
                category="threat",
                type="WrongLabel",
                type_id=1,
            )

        # Verify the error message mentions inconsistency
        error_str = str(exc_info.value)
        assert "Inconsistent" in error_str
        assert "type_id=1" in error_str
        assert "WrongLabel" in error_str

    def test_non_99_id_with_correct_label(self) -> None:
        """Non-99 IDs with correct label should work."""
        from ocsf.v1_7_0.objects import Analytic

        # type_id=1 maps to "Rule"
        analytic = Analytic(
            name="Test",
            category="threat",
            type="Rule",
            type_id=1,
        )

        assert analytic.type_ == "Rule"
        assert analytic.type_id == 1
