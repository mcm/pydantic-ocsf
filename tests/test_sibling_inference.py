"""Tests for sibling attribute field inference."""

import pytest

from ocsf._utils import infer_sibling_label_field


class TestSiblingLabelFieldInference:
    """Test suite for infer_sibling_label_field() utility."""

    def test_standard_pattern(self):
        """Test standard _id field patterns."""
        assert infer_sibling_label_field("activity_id") == "activity"
        assert infer_sibling_label_field("severity_id") == "severity"
        assert infer_sibling_label_field("status_id") == "status"
        assert infer_sibling_label_field("disposition_id") == "disposition"
        assert infer_sibling_label_field("risk_level_id") == "risk_level"

    def test_reserved_keyword_type(self):
        """Test that 'type' keyword gets underscore suffix."""
        assert infer_sibling_label_field("type_id") == "type_"

    def test_reserved_keyword_class(self):
        """Test that 'class' keyword gets underscore suffix."""
        assert infer_sibling_label_field("class_id") == "class_"

    def test_reserved_keyword_import(self):
        """Test that 'import' keyword gets underscore suffix."""
        assert infer_sibling_label_field("import_id") == "import_"

    def test_reserved_keyword_from(self):
        """Test that 'from' keyword gets underscore suffix."""
        assert infer_sibling_label_field("from_id") == "from_"

    def test_invalid_field_no_id_suffix(self):
        """Test that fields not ending in _id raise ValueError."""
        with pytest.raises(ValueError, match="Expected field ending in '_id'"):
            infer_sibling_label_field("activity")

        with pytest.raises(ValueError, match="Expected field ending in '_id'"):
            infer_sibling_label_field("severity")

    def test_invalid_field_empty(self):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="Expected field ending in '_id'"):
            infer_sibling_label_field("")

    def test_edge_case_underscore_in_base(self):
        """Test fields with underscores in base name."""
        assert infer_sibling_label_field("share_type_id") == "share_type"
        assert infer_sibling_label_field("confidence_id") == "confidence"
        assert infer_sibling_label_field("auth_protocol_id") == "auth_protocol"

    def test_all_known_sibling_patterns(self):
        """Test all known OCSF sibling patterns from PRD."""
        known_patterns = {
            "activity_id": "activity",
            "severity_id": "severity",
            "status_id": "status",
            "type_id": "type_",
            "disposition_id": "disposition",
            "risk_level_id": "risk_level",
            "confidence_id": "confidence",
            "state_id": "state",
        }

        for id_field, expected_label in known_patterns.items():
            assert infer_sibling_label_field(id_field) == expected_label, f"Failed for {id_field}"
