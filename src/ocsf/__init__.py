"""Pydantic models for the Open Cybersecurity Schema Framework (OCSF).

This package provides type-safe, validated models for OCSF security events
based on OCSF schema version 1.7.0.

Quick Start:
    from ocsf import FileActivity, File, User

    event = FileActivity(
        activity_id=FileActivity.ActivityId.CREATE,
        file=File(name="test.txt", type_id=1),
        metadata={"version": "1.7.0"}
    )

Import Patterns:
    # Primary (recommended):
    from ocsf import FileActivity, File, User

    # Backward compatible (explicit version):
    from ocsf.v1_7_0 import FileActivity

For detailed usage, see documentation at https://github.com/mcm/pydantic-ocsf
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ocsf._base import OCSFBaseModel as OCSFBaseModel
from ocsf._import_hook import install_hook
from ocsf._schema_loader import get_schema_loader

# Install the JIT import hook
install_hook()

__version__ = "2.0.2"


if TYPE_CHECKING:
    from ocsf.v1_7_0 import events as events, objects as objects  # noqa: I001

# Lazy import delegation to latest version (1.7.0)
# This avoids importing everything at module load time


def __getattr__(name: str) -> Any:
    """Lazy import symbols from the latest OCSF version."""
    # Delegate to the latest version module
    import importlib

    # Handle namespace module access
    if name in ("objects", "events"):
        module = importlib.import_module("ocsf.v1_7_0")
        return getattr(module, name)

    # For backward compatibility during transition, allow direct imports
    # but they must come from namespace modules
    try:
        module = importlib.import_module("ocsf.v1_7_0")
        return getattr(module, name)
    except AttributeError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None


def __dir__() -> list[str]:
    """Support for dir() and autocomplete."""
    return sorted(["OCSFBaseModel", "__version__"] + available_versions())

    # import importlib

    # module = importlib.import_module("ocsf.v1_7_0")
    # return sorted(["OCSFBaseModel", "__version__"] + dir(module))


def available_versions() -> list[str]:
    loader = get_schema_loader()
    return loader.get_available_versions()
