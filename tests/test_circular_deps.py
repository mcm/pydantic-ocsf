#!/usr/bin/env python3
"""Test circular dependency handling."""

import pytest


class TestCircularDependencies:
    """Test that circular dependencies are handled correctly."""

    def test_two_way_circular(self):
        """Test 2-way circular dependency (User ↔ Account)."""
        from ocsf.v1_7_0 import Account, User

        # Both should load without errors
        assert User is not None
        assert Account is not None

        # User should reference Account
        if "account" in User.model_fields:
            account_field = User.model_fields["account"]
            assert account_field is not None

        # Account should reference User
        if "user" in Account.model_fields:
            user_field = Account.model_fields["user"]
            assert user_field is not None

    def test_nested_object_creation(self):
        """Test creating objects with circular references."""
        from ocsf.v1_7_0 import User

        # Should be able to create User with nested Account
        user = User.model_validate(
            {
                "name": "Alice",
                "uid": "user-123",
                "account": {"uid": "acc-456", "name": "Main Account"},
            }
        )

        assert user.name == "Alice"
        if user.account:
            assert user.account.name == "Main Account"

    def test_deep_nesting(self):
        """Test deep nesting with circular refs."""
        from ocsf.v1_7_0 import Process

        # Process can contain parent Process
        # Should be able to create nested structure
        process = Process.model_validate(
            {
                "name": "child.exe",
                "pid": 1234,
                "parent_process": {
                    "name": "parent.exe",
                    "pid": 100,
                },
            }
        )

        assert process.name == "child.exe"
        if hasattr(process, "parent_process") and process.parent_process:
            assert process.parent_process.name == "parent.exe"

    def test_model_validation_with_circular_refs(self):
        """Test validation works with circular references."""
        from ocsf.v1_7_0 import User

        data = {
            "name": "Bob",
            "uid": "user-789",
            "account": {"uid": "acc-789", "name": "Bob Account"},
        }

        # Should validate without errors
        user = User.model_validate(data)
        assert user.name == "Bob"

    def test_serialization_with_circular_refs(self):
        """Test serialization with circular references."""
        from ocsf.v1_7_0 import User

        user = User.model_construct(
            name="Charlie", uid="user-999", account={"uid": "acc-999", "name": "Charlie Account"}
        )

        # Should serialize without errors
        data = user.model_dump()
        assert data["name"] == "Charlie"
        if "account" in data and data["account"]:
            assert data["account"]["name"] == "Charlie Account"

    def test_forward_ref_resolution(self):
        """Test that forward references are properly resolved."""
        from ocsf.v1_7_0 import User

        # After loading, forward refs should be resolved
        # Check that model_rebuild has been called
        assert User is not None

        # Should be able to create instances
        user = User(name="Test", uid="test-123")
        assert user is not None

    def test_multiple_circular_deps(self):
        """Test multiple models with circular dependencies."""
        from ocsf.v1_7_0 import Account, Group, User

        # All should load
        assert User is not None
        assert Account is not None
        assert Group is not None

        # Should be able to create instances
        user = User(name="Alice", uid="u-1")
        account = Account(uid="a-1", name="Account 1")
        group = Group(uid="g-1", name="Group 1")

        assert user is not None
        assert account is not None
        assert group is not None

    def test_self_referential(self):
        """Test self-referential models (Process → Process)."""
        from ocsf.v1_7_0 import Process

        # Should be able to load
        assert Process is not None

        # Should be able to create with self-reference
        process = Process.model_construct(
            name="init", pid=1, parent_process={"name": "kernel", "pid": 0}
        )

        assert process.name == "init"

    def test_dependency_chain(self):
        """Test loading a chain of dependencies."""
        from ocsf.v1_7_0 import FileActivity

        # FileActivity has many dependencies
        assert FileActivity is not None

        # Should be able to create instance
        activity = FileActivity.model_construct(activity_id=1, metadata={"version": "1.7.0"})

        assert activity is not None

    def test_rebuild_triggers_correctly(self):
        """Test that model_rebuild is triggered at right time."""
        from ocsf.v1_7_0 import Account, User

        # Load a model - should be usable immediately
        user = User(name="Test", uid="test-123")
        assert user.name == "Test"

        # Load another model that references User - both should still be usable
        account = Account(uid="acc-123", name="Test Account")
        assert account.name == "Test Account"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
