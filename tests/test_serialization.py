"""Test serialization round-trips."""

from ocsf.v1_7_0.enums.status_id import StatusId
from ocsf.v1_7_0.objects.file import File


def test_object_to_json_and_back():
    """Test that objects serialize to JSON and back."""
    file_obj = File(
        name="test.txt",
        type_id=1,
    )

    # Serialize
    json_str = file_obj.model_dump_json()

    # Deserialize
    restored = File.model_validate_json(json_str)

    assert restored.name == file_obj.name
    assert restored.type_id == file_obj.type_id


def test_enum_serializes_as_int():
    """Test that enums serialize as integers."""
    # Create object with enum
    file_obj = File(
        name="test.txt",
        type_id=StatusId.APPLICABLE,  # Value 1
    )

    data = file_obj.model_dump()
    # Enum should be serialized as integer
    assert isinstance(data["type_id"], int)
    assert data["type_id"] == 1


def test_extra_fields_preserved():
    """Test that unmapped fields are preserved."""
    data = {
        "name": "test.txt",
        "type_id": 1,
        "custom_field": "custom_value",
    }

    file_obj = File.model_validate(data)
    dumped = file_obj.model_dump()

    assert dumped["custom_field"] == "custom_value"


def test_optional_fields():
    """Test that optional fields work correctly."""
    # Create with only required fields
    file_obj = File(
        name="test.txt",
        type_id=1,
    )

    assert file_obj.name == "test.txt"
    assert file_obj.type_id == 1

    # Optional fields should be None
    assert file_obj.path is None


def test_model_dump_excludes_none():
    """Test that None values can be excluded from serialization."""
    file_obj = File(
        name="test.txt",
        type_id=1,
    )

    # Dump without None values
    data = file_obj.model_dump(exclude_none=True)

    assert "name" in data
    assert "type_id" in data
    assert "path" not in data  # Should be excluded because it's None
