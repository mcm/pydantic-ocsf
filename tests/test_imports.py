"""Test that all import patterns work correctly."""


def test_import_base_model():
    """Test importing base model."""
    from ocsf import OCSFBaseModel

    assert OCSFBaseModel is not None


def test_import_from_version():
    """Test importing event classes with nested enums."""
    from ocsf.v1_7_0.events import FileActivity

    # Test nested enum access (only for inline enums)
    assert FileActivity.ActivityId.CREATE == 1


def test_import_from_top_level():
    """Test importing from top-level."""
    from ocsf import FileActivity

    # Nested enums are accessible from the event class
    assert FileActivity.ActivityId.CREATE == 1


def test_version_submodules_exist():
    """Test that all version submodules exist."""
    import ocsf.v1_0_0
    import ocsf.v1_1_0
    import ocsf.v1_2_0
    import ocsf.v1_5_0
    import ocsf.v1_6_0
    import ocsf.v1_7_0

    assert ocsf.v1_7_0 is not None
    assert ocsf.v1_6_0 is not None
    assert ocsf.v1_5_0 is not None
    assert ocsf.v1_2_0 is not None
    assert ocsf.v1_1_0 is not None
    assert ocsf.v1_0_0 is not None
