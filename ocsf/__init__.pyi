"""OCSF Models - Type stubs (auto-generated)."""

from __future__ import annotations

# Namespace modules only - import from .objects or .events
from . import events as events
from . import objects as objects

__version__: str

def available_versions() -> list[str]: ...

__all__ = ["available_versions", "objects", "events", "__version__"]
