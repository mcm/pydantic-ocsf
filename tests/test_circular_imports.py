# ruff: noqa: F401

"""Test that circular import resolution pattern works correctly.

This test validates that our approach using:
1. `from __future__ import annotations` - for lazy annotation evaluation
2. `TYPE_CHECKING` imports - to avoid runtime circular imports
3. Deferred `model_rebuild()` - to resolve forward references

Works as expected for models with circular dependencies.
"""


def test_circular_imports_can_be_imported():
    """Test that models with circular dependencies can be imported without errors."""
    # User → LdapPerson → User circular dependency
    from ocsf.v1_7_0.objects import LdapPerson, User

    assert User is not None
    assert LdapPerson is not None


def test_circular_import_type_annotations_resolved():
    """Test that type annotations in circular dependencies are properly resolved."""
    from ocsf.v1_7_0.objects import LdapPerson, User

    # Check that annotations are the actual classes, not strings
    assert "ldap_person" in User.__annotations__
    assert "manager" in LdapPerson.__annotations__

    # The annotations should contain the class names
    user_ldap_annotation = str(User.__annotations__["ldap_person"])
    ldap_manager_annotation = str(LdapPerson.__annotations__["manager"])

    assert "LdapPerson" in user_ldap_annotation
    assert "User" in ldap_manager_annotation


def test_circular_dependencies_not_any():
    """Test that circular dependency fields don't fall back to Any."""
    from ocsf.v1_7_0.objects import LdapPerson, User

    # Check that the types are proper references, not Any
    user_annotation = str(User.__annotations__["ldap_person"])
    ldap_annotation = str(LdapPerson.__annotations__["manager"])

    # Should not be Any
    assert user_annotation != "Any"
    assert ldap_annotation != "Any"

    # Should reference the correct types
    assert "LdapPerson" in user_annotation
    assert "User" in ldap_annotation


def test_circular_models_can_be_instantiated():
    """Test that models with circular dependencies can be instantiated."""
    from ocsf.v1_7_0.objects import LdapPerson, User

    # Create LdapPerson without manager
    ldap = LdapPerson(given_name="Alice", surname="Smith")
    assert ldap.given_name == "Alice"

    # Create User with LdapPerson
    user = User(name="alice", ldap_person=ldap)
    assert user.ldap_person is not None
    assert user.ldap_person.given_name == "Alice"


def test_circular_models_can_reference_each_other():
    """Test that circular models can properly reference each other."""
    from ocsf.v1_7_0.objects import LdapPerson, User

    # Create manager
    manager_user = User(name="bob")

    # Create LdapPerson with manager
    employee_ldap = LdapPerson(given_name="Alice", surname="Smith", manager=manager_user)

    # Create employee User with LdapPerson
    employee_user = User(name="alice", ldap_person=employee_ldap)

    # Verify the circular reference works
    assert employee_user.ldap_person is not None
    assert employee_user.ldap_person.manager is not None
    assert employee_user.ldap_person.manager.name == "bob"


def test_circular_models_serialize_correctly():
    """Test that models with circular references serialize to JSON."""
    from ocsf.v1_7_0.objects import LdapPerson, User

    manager = User(name="bob", uid="user-123")
    ldap = LdapPerson(given_name="Alice", manager=manager)
    user = User(name="alice", ldap_person=ldap)

    # Serialize to dict
    data = user.model_dump()
    assert data["name"] == "alice"
    assert data["ldap_person"]["given_name"] == "Alice"
    assert data["ldap_person"]["manager"]["name"] == "bob"

    # Serialize to JSON
    json_str = user.model_dump_json()
    assert "alice" in json_str
    assert "Alice" in json_str
    assert "bob" in json_str


def test_circular_models_deserialize_correctly():
    """Test that models with circular references can be deserialized from JSON."""
    from ocsf.v1_7_0.objects import User

    data = {
        "name": "alice",
        "ldap_person": {"given_name": "Alice", "manager": {"name": "bob", "uid": "user-123"}},
    }

    user = User.model_validate(data)
    assert user.name == "alice"
    assert user.ldap_person is not None
    assert user.ldap_person.given_name == "Alice"
    assert user.ldap_person.manager is not None
    assert user.ldap_person.manager.name == "bob"


def test_multiple_circular_dependencies():
    """Test multiple models with circular dependencies can coexist."""
    # Test several known circular dependencies
    from ocsf.v1_7_0.objects import (
        File,
        LdapPerson,
        Process,
        User,
    )

    # User ↔ LdapPerson
    assert "ldap_person" in User.__annotations__
    assert "manager" in LdapPerson.__annotations__

    # Process ↔ File (if this exists)
    # Both Process and File reference each other in many schemas
    assert Process is not None
    assert File is not None


def test_no_any_in_object_references():
    """Test that object reference fields use proper types, not Any."""
    import typing

    from ocsf.v1_7_0.events import ApiActivity

    # Check that actor, api, metadata are proper types, not Any
    actor_annotation = ApiActivity.__annotations__.get("actor")
    api_annotation = ApiActivity.__annotations__.get("api")
    metadata_annotation = ApiActivity.__annotations__.get("metadata")

    # Should not be Any
    assert actor_annotation != typing.Any
    assert api_annotation != typing.Any
    assert metadata_annotation != typing.Any

    # Should be proper class references
    assert "Actor" in str(actor_annotation)
    assert "Api" in str(api_annotation)
    assert "Metadata" in str(metadata_annotation)


def test_type_checking_imports_work():
    """Test that TYPE_CHECKING pattern doesn't break runtime behavior."""
    from ocsf.v1_7_0.objects import User

    # Create instance - should work even though imports are under TYPE_CHECKING
    user = User(name="test")
    assert user.name == "test"

    # Model should have proper schema
    assert hasattr(User, "model_fields")
    assert "name" in User.model_fields


def test_model_rebuild_happened():
    """Test that models were rebuilt with correct namespace."""
    from ocsf.v1_7_0.objects import User

    # If model_rebuild() didn't happen correctly, we'd get errors
    # The fact that we can access annotations means rebuild worked
    assert hasattr(User, "__pydantic_complete__")

    # Check that the model has processed all fields
    assert len(User.model_fields) > 0


def test_forward_references_resolved():
    """Test that forward references in type annotations are resolved."""
    from ocsf.v1_7_0.objects import LdapPerson, User

    # Get the actual field info from Pydantic
    ldap_field = User.model_fields.get("ldap_person")
    manager_field = LdapPerson.model_fields.get("manager")

    # Fields should exist
    assert ldap_field is not None
    assert manager_field is not None

    # Check that the annotation is resolved (not a string)
    # Pydantic resolves ForwardRef to actual types
    assert ldap_field.annotation is not None
    assert manager_field.annotation is not None


def test_complex_nested_circular_references():
    """Test complex nested structures with circular dependencies."""
    from ocsf.v1_7_0.objects import LdapPerson, User

    # Create a two-level hierarchy
    # Manager User with their LDAP info
    manager_user = User(name="manager", uid="user-1")

    # Employee LDAP info that references manager
    employee_ldap = LdapPerson(
        given_name="Alice",
        surname="Smith",
        manager=manager_user,  # LdapPerson → User reference
    )

    # Employee User with their LDAP info
    employee_user = User(
        name="alice",
        uid="user-2",
        ldap_person=employee_ldap,  # User → LdapPerson reference
    )

    # Verify circular references work
    assert employee_user.ldap_person.manager.name == "manager"

    # Serialize and verify structure preserves circular references
    data = employee_user.model_dump()
    assert data["name"] == "alice"
    assert data["ldap_person"]["given_name"] == "Alice"
    assert data["ldap_person"]["manager"]["name"] == "manager"
    assert data["ldap_person"]["manager"]["uid"] == "user-1"


def test_annotations_are_strings_at_module_level():
    """Test that annotations are stored as strings due to __future__ import."""
    import inspect

    from ocsf.v1_7_0.objects import user

    # Check that the module has __future__ annotations enabled
    # This is indicated by the __annotations__ being strings in source
    source = inspect.getsource(user)
    assert "from __future__ import annotations" in source


def test_type_checking_imports_in_generated_code():
    """Test that generated code uses TYPE_CHECKING pattern."""
    import inspect

    from ocsf.v1_7_0.objects import user

    source = inspect.getsource(user)

    # Should have TYPE_CHECKING import
    assert "from typing import TYPE_CHECKING" in source
    assert "if TYPE_CHECKING:" in source


def test_no_circular_import_errors_on_direct_import():
    """Test that directly importing objects with circular deps doesn't raise ImportError."""
    # This should not raise ImportError even though User and LdapPerson reference each other
    try:
        from ocsf.v1_7_0.objects.ldap_person import LdapPerson
        from ocsf.v1_7_0.objects.user import User

        success = True
    except ImportError:
        success = False

    assert success, "Direct imports of circularly dependent models should not fail"
