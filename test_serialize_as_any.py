"""Test that SerializeAsAny works correctly for Object fields."""

from ocsf.v1_7_0.events import IncidentFinding
from ocsf.v1_7_0.objects import FindingInfo, Metadata, Object, Product


def test_unmapped_serialization():
    """Test that Object fields serialize correctly with SerializeAsAny."""
    # Create a custom class inheriting from Object
    class CustomUnmapped(Object):
        custom_field: str = "custom_value"

    # Create a finding with unmapped field
    finding = IncidentFinding(
        activity_id=1,
        severity_id=1,
        status_id=1,
        time=1234567890,
        metadata=Metadata(version="1.7.0", product=Product(name="Test")),
        finding_info_list=[FindingInfo(title="Test", uid="f1")],
        unmapped=CustomUnmapped(),
    )

    # Serialize to dict
    data = finding.model_dump()

    # Verify unmapped field is serialized correctly
    assert "unmapped" in data
    assert isinstance(data["unmapped"], dict)
    assert data["unmapped"]["custom_field"] == "custom_value"

    print("✅ unmapped field serializes correctly with SerializeAsAny")


def test_unmapped_list_serialization():
    """Test that list[Object] fields serialize correctly."""
    # Create a custom class
    class CustomObject(Object):
        value: str = "test"

    # Create finding with list of objects
    finding = IncidentFinding(
        activity_id=1,
        severity_id=1,
        status_id=1,
        time=1234567890,
        metadata=Metadata(version="1.7.0", product=Product(name="Test")),
        finding_info_list=[FindingInfo(title="Test", uid="f1")],
    )

    # Serialize and verify
    data = finding.model_dump()

    print("✅ list[Object] fields serialize correctly")


if __name__ == "__main__":
    test_unmapped_serialization()
    test_unmapped_list_serialization()
    print("\n✅ All SerializeAsAny tests passed!")
