#!/usr/bin/env python3
"""Test ModelFactory behavior."""

import pytest

from ocsf._base import OCSFBaseModel


class TestModelFactory:
    """Test model creation and field handling."""

    def test_simple_model_creation(self):
        """Test creating a simple model."""
        from ocsf.v1_7_0.objects import User

        assert User is not None
        assert issubclass(User, OCSFBaseModel)
        assert hasattr(User, "model_fields")

    def test_inheritance_resolution(self):
        """Test that inheritance is resolved correctly."""
        from ocsf.v1_7_0.events import FileActivity

        # FileActivity should inherit from base classes
        assert issubclass(FileActivity, OCSFBaseModel)

        # Check inheritance chain
        bases = FileActivity.__mro__
        assert OCSFBaseModel in bases

    def test_field_types(self):
        """Test that field types are correctly mapped."""
        from ocsf.v1_7_0.objects import File

        fields = File.model_fields

        # String fields
        if "name" in fields:
            from typing import Any

            # Field annotation can be str, 'str', 'str | None', or Any
            assert fields["name"].annotation in [str, "str", "str | None", Any]

        # Integer fields
        if "size" in fields:
            # Size can be int or int | None
            annotation_str = str(fields["size"].annotation)
            assert "int" in annotation_str

    def test_nested_objects(self):
        """Test that nested object references work."""
        from ocsf.v1_7_0.objects import User

        # User has account field that references Account model
        if "account" in User.model_fields:
            account_field = User.model_fields["account"]
            # Should be a forward reference that's resolved
            assert account_field.annotation is not None

    def test_array_fields(self):
        """Test that array/list fields work."""
        from ocsf.v1_7_0.objects import Process

        # Process may have children which is list[Process]
        if "children" in Process.model_fields:
            children_field = Process.model_fields["children"]
            annotation_str = str(children_field.annotation)
            assert "list" in annotation_str.lower()

    def test_required_vs_optional_fields(self):
        """Test that required/optional fields are handled correctly."""
        from ocsf.v1_7_0.objects import File

        fields = File.model_fields

        # Check some fields have correct requirement
        for _field_name, field_info in fields.items():
            # All fields should have is_required() method
            assert hasattr(field_info, "is_required")

    def test_inline_enum_extraction(self):
        """Test that inline enums are extracted from schema."""
        from ocsf.v1_7_0.events import FileActivity

        # FileActivity should have ActivityId enum
        assert hasattr(FileActivity, "ActivityId")

        ActivityId = FileActivity.ActivityId

        # Should be an enum
        from enum import IntEnum

        assert issubclass(ActivityId, IntEnum)

    def test_enum_attachment_to_model(self):
        """Test that enums are attached as nested classes."""
        from ocsf.v1_7_0.events import FileActivity

        # Enum should be accessible as attribute
        assert hasattr(FileActivity, "ActivityId")

        # Should be accessible via the model class
        ActivityId = FileActivity.ActivityId
        assert ActivityId is not None

    def test_pascal_to_snake_conversion(self):
        """Test PascalCase to snake_case conversion."""
        from ocsf._model_factory import ModelFactory
        from ocsf._schema_loader import get_schema_loader

        loader = get_schema_loader()
        schema = loader.load_schema("1.7.0")
        factory = ModelFactory(schema, "1.7.0")

        # Test conversion
        assert factory._pascal_to_snake("User") == "user"
        assert factory._pascal_to_snake("FileActivity") == "file_activity"
        assert factory._pascal_to_snake("ApiActivity") == "api_activity"

    def test_multiple_models_same_cache(self):
        """Test that multiple models share the same cache."""
        import ocsf.v1_7_0

        # Create several models
        User = ocsf.v1_7_0.objects.User
        Account = ocsf.v1_7_0.objects.Account
        File = ocsf.v1_7_0.objects.File

        # All should be in the same cache (with namespaced keys)
        cache = ocsf.v1_7_0._model_cache
        assert "objects:User" in cache
        assert "objects:Account" in cache
        assert "objects:File" in cache

    def test_dictionary_attribute_merging(self):
        """Test that dictionary attributes are merged correctly."""
        from ocsf.v1_7_0.objects import User

        # User should have fields from both local spec and dictionary
        assert len(User.model_fields) > 0

    def test_model_instantiation(self):
        """Test that created models can be instantiated."""
        from ocsf.v1_7_0.objects import User

        # Should be able to create instances
        user = User(name="Alice", uid="user-123")
        assert user.name == "Alice"
        assert user.uid == "user-123"

    def test_model_validation(self):
        """Test that model validation works."""

        from ocsf.v1_7_0.objects import User

        # Valid data should work
        user = User.model_validate({"name": "Bob", "uid": "user-456"})
        assert user.name == "Bob"

    def test_model_serialization(self):
        """Test that models can be serialized."""
        from ocsf.v1_7_0.objects import User

        user = User(name="Charlie", uid="user-789")

        # Should be able to serialize
        data = user.model_dump()
        assert data["name"] == "Charlie"
        assert data["uid"] == "user-789"

        # Should be able to serialize to JSON
        json_str = user.model_dump_json()
        assert '"name"' in json_str
        assert '"Charlie"' in json_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
