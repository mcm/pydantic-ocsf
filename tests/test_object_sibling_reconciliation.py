"""Test sibling reconciliation in objects."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from ocsf.v1_7_0.objects import Account


class TestObjectSiblingReconciliation:
    """Test sibling attribute reconciliation in objects."""

    def test_object_nested_enum_access(self):
        """Test that objects have nested enums."""
        # Account has type_id/type as sibling pair
        assert hasattr(Account, "TypeId")
        assert Account.TypeId.LDAP_ACCOUNT == 1
        assert Account.TypeId.WINDOWS_ACCOUNT == 2

    def test_object_only_id_extrapolates_label(self):
        """Test that providing only ID extrapolates the label in objects."""
        data = {
            "name": "alice",
            "type_id": 1,
        }
        account = Account.model_validate(data)
        assert account.type_id == Account.TypeId.LDAP_ACCOUNT
        assert account.type == "LDAP Account"

    def test_object_only_label_extrapolates_id(self):
        """Test that providing only label extrapolates the ID in objects."""
        data = {
            "name": "alice",
            "type": "LDAP Account",
        }
        account = Account.model_validate(data)
        assert account.type_id == Account.TypeId.LDAP_ACCOUNT
        assert account.type == "LDAP Account"

    def test_object_both_present_matching(self):
        """Test both ID and label present with matching values in objects."""
        data = {
            "name": "alice",
            "type_id": 1,
            "type": "LDAP Account",
        }
        account = Account.model_validate(data)
        assert account.type_id == Account.TypeId.LDAP_ACCOUNT
        assert account.type == "LDAP Account"

    def test_object_both_present_mismatched_raises(self):
        """Test that mismatched ID and label raise ValidationError in objects."""
        data = {
            "name": "alice",
            "type_id": 1,  # LDAP_ACCOUNT
            "type": "Windows Account",  # Mismatch!
        }
        with pytest.raises(ValidationError) as exc_info:
            Account.model_validate(data)
        error_msg = str(exc_info.value)
        assert "does not match" in error_msg

    def test_object_case_insensitive(self):
        """Test that label lookup is case-insensitive in objects."""
        data = {
            "name": "alice",
            "type": "ldap account",  # lowercase
        }
        account = Account.model_validate(data)
        assert account.type_id == Account.TypeId.LDAP_ACCOUNT
        assert account.type == "LDAP Account"  # Canonical casing

    def test_object_string_construction(self):
        """Test that nested enums support string construction."""
        # From exact label
        enum_val = Account.TypeId("LDAP Account")
        assert enum_val == Account.TypeId.LDAP_ACCOUNT
        assert enum_val.label == "LDAP Account"

        # Case insensitive
        enum_val = Account.TypeId("ldap account")
        assert enum_val == Account.TypeId.LDAP_ACCOUNT

    def test_object_enum_label_property(self):
        """Test that nested enums have label property."""
        enum_val = Account.TypeId.LDAP_ACCOUNT
        assert enum_val.label == "LDAP Account"
