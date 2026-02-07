"""Test reserved keyword field aliases."""

from ocsf.v1_7_0.objects import Analytic


def test_reserved_keyword_serialization() -> None:
    """Test that reserved keyword fields serialize with their original names."""
    # Create an Analytic with type_id (which has a sibling field 'type' that's a reserved keyword)
    analytic = Analytic(
        type_id=1,  # Rule
        name="Test Analytic",
        uid="analytic-123",
    )

    # Default serialization (uses aliases due to serialize_by_alias=True config)
    data_default = analytic.model_dump(exclude_none=True)
    print("Serialized (default - uses aliases):")
    print(f"  Keys: {sorted(data_default.keys())}")
    assert "type" in data_default, "Should have 'type' by default (serialize_by_alias=True)"
    assert "type_" not in data_default, "Should NOT have 'type_' by default"

    # Serialize with by_alias=False (Python field names)
    data_no_alias = analytic.model_dump(by_alias=False, exclude_none=True)
    print("\nSerialized with by_alias=False:")
    print(f"  Keys: {sorted(data_no_alias.keys())}")
    assert "type_" in data_no_alias, "Should have 'type_' when by_alias=False"
    assert "type" not in data_no_alias, "Should NOT have 'type' when by_alias=False"

    # Serialize with by_alias=True (explicit, same as default)
    data_with_alias = analytic.model_dump(by_alias=True, exclude_none=True)
    print("\nSerialized with by_alias=True:")
    print(f"  Keys: {sorted(data_with_alias.keys())}")
    assert "type" in data_with_alias, "Should have 'type' when by_alias=True"
    assert "type_" not in data_with_alias, "Should NOT have 'type_' when by_alias=True"

    print("\n✅ Reserved keyword fields serialize correctly!")
    print("   type_ (Python) → type (OCSF) [by default]")


def test_reserved_keyword_deserialization() -> None:
    """Test that reserved keyword fields can be deserialized from either name."""
    # Deserialize from original OCSF name ('type')
    data_ocsf = {
        "type_id": 1,
        "type": "Rule",
        "name": "Test",
        "uid": "123",
    }
    analytic1 = Analytic.model_validate(data_ocsf)
    assert analytic1.type_ == "Rule", "Should deserialize from 'type'"

    # Deserialize from Python name ('type_')
    data_python = {
        "type_id": 1,
        "type_": "Rule",
        "name": "Test",
        "uid": "123",
    }
    analytic2 = Analytic.model_validate(data_python)
    assert analytic2.type_ == "Rule", "Should deserialize from 'type_'"

    print("✅ Reserved keyword fields deserialize from both names!")


if __name__ == "__main__":
    test_reserved_keyword_serialization()
    test_reserved_keyword_deserialization()
    print("\n✅ All reserved keyword tests passed!")
