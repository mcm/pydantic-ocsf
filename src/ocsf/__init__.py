"""Pydantic models for the Open Cybersecurity Schema Framework (OCSF).

This package provides type-safe, validated models for OCSF security events.

Example:
    from ocsf import FileActivity, File, SeverityId

    event = FileActivity(
        time=1706000000000,
        activity_id=1,
        severity_id=SeverityId.INFORMATIONAL,
        file=File(name="test.txt"),
    )

The default imports are from OCSF 1.7.0 (latest). For other versions:
    from ocsf.v1_7_0 import FileActivity  # OCSF 1.7.0
    from ocsf.v1_6_0 import FileActivity  # OCSF 1.6.0
    from ocsf.v1_5_0 import FileActivity  # OCSF 1.5.0
    from ocsf.v1_2_0 import FileActivity  # OCSF 1.2.0
    from ocsf.v1_1_0 import FileActivity  # OCSF 1.1.0
    from ocsf.v1_0_0 import FileActivity  # OCSF 1.0.0
"""

from __future__ import annotations

from typing import Any

from ocsf._base import OCSFBaseModel as OCSFBaseModel

__version__ = "1.7.0.20260130"

# Lazy import delegation to latest version (1.7.0)
# This avoids importing everything at module load time


def __getattr__(name: str) -> Any:
    """Lazy import symbols from the latest OCSF version."""
    # Delegate to the latest version module
    import importlib

    try:
        module = importlib.import_module("ocsf.v1_7_0")
        return getattr(module, name)
    except AttributeError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None


def __dir__() -> list[str]:
    """Support for dir() and autocomplete."""
    import importlib

    module = importlib.import_module("ocsf.v1_7_0")
    return sorted(["OCSFBaseModel", "__version__"] + list(getattr(module, "__all__", [])))
