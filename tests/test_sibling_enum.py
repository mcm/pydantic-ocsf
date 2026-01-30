"""Unit tests for the SiblingEnum base class."""

from __future__ import annotations

import pytest

from ocsf._sibling_enum import SiblingEnum


class TestSiblingEnum:
    """Test the SiblingEnum base class."""

    @pytest.fixture
    def sample_enum(self):
        """Create a sample enum for testing."""

        class SampleId(SiblingEnum):
            UNKNOWN = 0
            CREATE = 1
            DELETE = 4
            OTHER = 99

            @classmethod
            def _get_label_map(cls) -> dict[int, str]:
                return {
                    0: "Unknown",
                    1: "Create",
                    4: "Delete",
                    99: "Other",
                }

        return SampleId

    def test_construction_from_int(self, sample_enum):
        """Test construction from integer values."""
        assert sample_enum(1) == sample_enum.CREATE
        assert sample_enum(4) == sample_enum.DELETE
        assert sample_enum(0) == sample_enum.UNKNOWN
        assert sample_enum(99) == sample_enum.OTHER

    def test_construction_from_string_exact_case(self, sample_enum):
        """Test construction from string with exact case match."""
        assert sample_enum("Create") == sample_enum.CREATE
        assert sample_enum("Delete") == sample_enum.DELETE
        assert sample_enum("Unknown") == sample_enum.UNKNOWN
        assert sample_enum("Other") == sample_enum.OTHER

    def test_construction_from_string_lowercase(self, sample_enum):
        """Test construction from lowercase strings."""
        assert sample_enum("create") == sample_enum.CREATE
        assert sample_enum("delete") == sample_enum.DELETE
        assert sample_enum("unknown") == sample_enum.UNKNOWN
        assert sample_enum("other") == sample_enum.OTHER

    def test_construction_from_string_uppercase(self, sample_enum):
        """Test construction from uppercase strings."""
        assert sample_enum("CREATE") == sample_enum.CREATE
        assert sample_enum("DELETE") == sample_enum.DELETE
        assert sample_enum("UNKNOWN") == sample_enum.UNKNOWN
        assert sample_enum("OTHER") == sample_enum.OTHER

    def test_unknown_string_raises_valueerror(self, sample_enum):
        """Test that unknown strings raise ValueError (strict construction)."""
        with pytest.raises(ValueError, match="Unknown SampleId label"):
            sample_enum("Custom Action")

    def test_invalid_int_raises_valueerror(self, sample_enum):
        """Test that invalid integer values raise ValueError."""
        with pytest.raises(ValueError):
            sample_enum(9999)

    def test_label_property(self, sample_enum):
        """Test the label property returns canonical strings."""
        assert sample_enum.CREATE.label == "Create"
        assert sample_enum.DELETE.label == "Delete"
        assert sample_enum.UNKNOWN.label == "Unknown"
        assert sample_enum.OTHER.label == "Other"

    def test_label_property_consistency(self, sample_enum):
        """Test label property is consistent regardless of construction method."""
        assert sample_enum(1).label == "Create"
        assert sample_enum("create").label == "Create"
        assert sample_enum.CREATE.label == "Create"

    def test_from_label_case_insensitive(self, sample_enum):
        """Test from_label classmethod with various cases."""
        assert sample_enum.from_label("Create") == sample_enum.CREATE
        assert sample_enum.from_label("create") == sample_enum.CREATE
        assert sample_enum.from_label("CREATE") == sample_enum.CREATE
        assert sample_enum.from_label("CrEaTe") == sample_enum.CREATE

    def test_from_label_unknown_raises(self, sample_enum):
        """Test from_label raises ValueError for unknown labels."""
        with pytest.raises(ValueError, match="Unknown SampleId label"):
            sample_enum.from_label("Nonexistent")

    def test_int_behavior_preserved(self, sample_enum):
        """Verify IntEnum integer behavior is preserved."""
        assert sample_enum.CREATE == 1
        assert sample_enum.CREATE + 3 == 4
        assert int(sample_enum.DELETE) == 4
        assert sample_enum.DELETE * 2 == 8

    def test_comparison_with_int(self, sample_enum):
        """Test that enum values can be compared with integers."""
        assert sample_enum.CREATE == 1
        assert sample_enum.DELETE != 1
        assert sample_enum.DELETE > sample_enum.CREATE
        assert sample_enum.UNKNOWN < sample_enum.OTHER

    def test_enum_member_identity(self, sample_enum):
        """Test that the same enum value always returns the same object."""
        assert sample_enum(1) is sample_enum(1)
        assert sample_enum("Create") is sample_enum(1)
        assert sample_enum.CREATE is sample_enum(1)

    def test_value_attribute(self, sample_enum):
        """Test the value attribute is correctly set."""
        assert sample_enum.CREATE.value == 1
        assert sample_enum.DELETE.value == 4
        assert sample_enum(1).value == 1
        assert sample_enum("Delete").value == 4

    def test_name_attribute(self, sample_enum):
        """Test the name attribute is correctly set."""
        assert sample_enum.CREATE.name == "CREATE"
        assert sample_enum.DELETE.name == "DELETE"
        assert sample_enum(1).name == "CREATE"


class TestSiblingEnumWithoutOther:
    """Test behavior when enum has no OTHER member."""

    @pytest.fixture
    def strict_enum(self):
        """Create an enum without OTHER member."""

        class StrictId(SiblingEnum):
            UNKNOWN = 0
            VALUE_A = 1
            VALUE_B = 2
            # No OTHER!

            @classmethod
            def _get_label_map(cls) -> dict[int, str]:
                return {
                    0: "Unknown",
                    1: "Value A",
                    2: "Value B",
                }

        return StrictId

    def test_unknown_string_raises_without_other(self, strict_enum):
        """Test that unknown strings raise ValueError when no OTHER exists."""
        with pytest.raises(ValueError, match="Unknown StrictId label"):
            strict_enum("Custom Value")

    def test_from_label_unknown_raises_without_other(self, strict_enum):
        """Test from_label raises ValueError for unknown labels when no OTHER."""
        with pytest.raises(ValueError, match="Unknown StrictId label"):
            strict_enum.from_label("Invalid")

    def test_valid_label_map_work_without_other(self, strict_enum):
        """Test that valid labels still work without OTHER."""
        assert strict_enum("Value A") == strict_enum.VALUE_A
        assert strict_enum("Value B") == strict_enum.VALUE_B
        assert strict_enum("value a") == strict_enum.VALUE_A


class TestSiblingEnumEdgeCases:
    """Test edge cases and special scenarios."""

    @pytest.fixture
    def edge_case_enum(self):
        """Create an enum with edge case labels."""

        class EdgeCaseId(SiblingEnum):
            EMPTY_LABEL = 1
            WHITESPACE = 2
            SPECIAL_CHARS = 3
            OTHER = 99

            @classmethod
            def _get_label_map(cls) -> dict[int, str]:
                return {
                    1: "",
                    2: "  Whitespace  ",
                    3: "Special-Chars_123",
                    99: "Other",
                }

        return EdgeCaseId

    def test_empty_string_label(self, edge_case_enum):
        """Test handling of empty string labels."""
        # Empty string in labels should match
        assert edge_case_enum("") == edge_case_enum.EMPTY_LABEL

    def test_whitespace_label_exact_match(self, edge_case_enum):
        """Test whitespace in labels is preserved for exact matching."""
        assert edge_case_enum("  Whitespace  ") == edge_case_enum.WHITESPACE
        assert edge_case_enum("  whitespace  ") == edge_case_enum.WHITESPACE

    def test_special_characters_in_label(self, edge_case_enum):
        """Test labels with special characters."""
        assert edge_case_enum("Special-Chars_123") == edge_case_enum.SPECIAL_CHARS
        assert edge_case_enum("special-chars_123") == edge_case_enum.SPECIAL_CHARS

    def test_label_not_stripped(self, edge_case_enum):
        """Test that whitespace is not automatically stripped."""
        # "Whitespace" without spaces should not match
        with pytest.raises(ValueError):
            edge_case_enum.from_label("Whitespace")


class TestSiblingEnumRealWorldExample:
    """Test with realistic OCSF-style enums."""

    @pytest.fixture
    def activity_enum(self):
        """Create a realistic ActivityId enum."""

        class ActivityId(SiblingEnum):
            UNKNOWN = 0
            CREATE = 1
            READ = 2
            UPDATE = 3
            DELETE = 4
            OTHER = 99

            @classmethod
            def _get_label_map(cls) -> dict[int, str]:
                return {
                    0: "Unknown",
                    1: "Create",
                    2: "Read",
                    3: "Update",
                    4: "Delete",
                    99: "Other",
                }

        return ActivityId

    @pytest.fixture
    def severity_enum(self):
        """Create a realistic SeverityId enum."""

        class SeverityId(SiblingEnum):
            UNKNOWN = 0
            INFORMATIONAL = 1
            LOW = 2
            MEDIUM = 3
            HIGH = 4
            CRITICAL = 5
            FATAL = 6
            OTHER = 99

            @classmethod
            def _get_label_map(cls) -> dict[int, str]:
                return {
                    0: "Unknown",
                    1: "Informational",
                    2: "Low",
                    3: "Medium",
                    4: "High",
                    5: "Critical",
                    6: "Fatal",
                    99: "Other",
                }

        return SeverityId

    def test_activity_enum_crud_operations(self, activity_enum):
        """Test ActivityId with typical CRUD operations."""
        assert activity_enum.CREATE.value == 1
        assert activity_enum.READ.value == 2
        assert activity_enum.UPDATE.value == 3
        assert activity_enum.DELETE.value == 4

        assert activity_enum("Create") == activity_enum.CREATE
        assert activity_enum("read") == activity_enum.READ
        assert activity_enum("UPDATE") == activity_enum.UPDATE

    def test_severity_enum_levels(self, severity_enum):
        """Test SeverityId with typical severity levels."""
        assert severity_enum.INFORMATIONAL.label == "Informational"
        assert severity_enum.HIGH.label == "High"
        assert severity_enum.CRITICAL.label == "Critical"

        assert severity_enum("low") == severity_enum.LOW
        assert severity_enum("Medium") == severity_enum.MEDIUM
        assert severity_enum("FATAL") == severity_enum.FATAL

    def test_custom_activity_raises_valueerror(self, activity_enum):
        """Test custom activity names raise ValueError (strict construction)."""
        with pytest.raises(ValueError, match="Unknown ActivityId label"):
            activity_enum("Quarantine File")

    def test_custom_severity_raises_valueerror(self, severity_enum):
        """Test custom severity labels raise ValueError (strict construction)."""
        with pytest.raises(ValueError, match="Unknown SeverityId label"):
            severity_enum("Custom Severity Level")
