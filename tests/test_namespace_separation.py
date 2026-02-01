"""Tests for namespace separation (objects vs events)."""

import pytest


def test_import_from_objects_namespace():
    """Can import objects from objects namespace."""
    from ocsf.v1_7_0.objects import User, Account, File

    assert User is not None
    assert Account is not None
    assert File is not None


def test_import_from_events_namespace():
    """Can import events from events namespace."""
    from ocsf.v1_7_0.events import FileActivity, ApiActivity

    assert FileActivity is not None
    assert ApiActivity is not None


def test_finding_collision_resolved():
    """Finding exists in both namespaces as different classes."""
    from ocsf.v1_7_0.objects import Finding as FindingObject
    from ocsf.v1_7_0.events import Finding as FindingEvent

    # Different classes
    assert FindingObject is not FindingEvent
    assert FindingObject.__name__ == "Finding"
    assert FindingEvent.__name__ == "Finding"


def test_application_collision_resolved():
    """Application exists in both namespaces as different classes."""
    from ocsf.v1_7_0.objects import Application as AppObject
    from ocsf.v1_7_0.events import Application as AppEvent

    assert AppObject is not AppEvent


def test_wrong_namespace_raises_error():
    """Importing from wrong namespace raises helpful error."""
    with pytest.raises(ImportError, match="cannot import name"):
        from ocsf.v1_7_0.objects import FileActivity  # Event, not object

    with pytest.raises(ImportError, match="cannot import name"):
        from ocsf.v1_7_0.events import User  # Object, not event


def test_old_import_style_raises_error():
    """Old import style no longer works (breaking change)."""
    with pytest.raises(ImportError, match="cannot import name"):
        from ocsf.v1_7_0 import User  # Should fail

    with pytest.raises(ImportError, match="cannot import name"):
        from ocsf.v1_7_0 import FileActivity  # Should fail


def test_version_module_only_exposes_namespaces():
    """Version module only exposes objects and events namespaces."""
    import ocsf.v1_7_0

    assert hasattr(ocsf.v1_7_0, "objects")
    assert hasattr(ocsf.v1_7_0, "events")
    assert "objects" in dir(ocsf.v1_7_0)
    assert "events" in dir(ocsf.v1_7_0)

    # Should NOT expose model names
    assert "User" not in dir(ocsf.v1_7_0)
    assert "FileActivity" not in dir(ocsf.v1_7_0)


def test_namespace_dir():
    """dir() on namespace modules returns only appropriate models."""
    import ocsf.v1_7_0.objects
    import ocsf.v1_7_0.events

    objects_dir = dir(ocsf.v1_7_0.objects)
    events_dir = dir(ocsf.v1_7_0.events)

    assert "User" in objects_dir
    assert "User" not in events_dir

    assert "FileActivity" in events_dir
    assert "FileActivity" not in objects_dir


def test_top_level_namespace_access():
    """Can access namespaces from top-level ocsf package."""
    from ocsf import objects, events

    assert objects is not None
    assert events is not None

    # Can import from them
    User = objects.User
    FileActivity = events.FileActivity

    assert User is not None
    assert FileActivity is not None


def test_shared_model_cache():
    """Models are cached in parent module, accessible via namespaces."""
    from ocsf.v1_7_0.objects import User
    from ocsf.v1_7_0 import _model_cache

    # User should be in the parent's cache with namespaced key
    assert "objects:User" in _model_cache
    assert _model_cache["objects:User"] is User


def test_cross_namespace_references():
    """Events can reference objects (e.g., FileActivity.file: File)."""
    from ocsf.v1_7_0.events import FileActivity
    from ocsf.v1_7_0.objects import File

    # Create an event with a file object
    event = FileActivity.model_construct(
        class_uid=1001,
        category_uid=1,
        metadata={"version": "1.7.0"},
        file=File.model_construct(name="test.txt", type_id=1),
    )

    assert event.file is not None
    assert isinstance(event.file, File)


def test_model_identity_preserved():
    """Same model imported from different paths is identical."""
    from ocsf.v1_7_0.objects import User as User1

    # Import again
    from ocsf.v1_7_0.objects import User as User2

    # Should be the same class
    assert User1 is User2


def test_enum_classes_accessible():
    """Enum classes attached to models are accessible."""
    from ocsf.v1_7_0.events import FileActivity

    # Should have ActivityId enum
    assert hasattr(FileActivity, "ActivityId")
    assert hasattr(FileActivity.ActivityId, "CREATE")


def test_namespace_module_attributes():
    """Namespace modules have correct attributes."""
    import ocsf.v1_7_0.objects
    import ocsf.v1_7_0.events

    # Check module name
    assert ocsf.v1_7_0.objects.__name__ == "ocsf.v1_7_0.objects"
    assert ocsf.v1_7_0.events.__name__ == "ocsf.v1_7_0.events"

    # Check parent reference
    assert hasattr(ocsf.v1_7_0.objects, "_parent")
    assert hasattr(ocsf.v1_7_0.events, "_parent")
