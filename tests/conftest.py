#!/usr/bin/env python3
"""Pytest configuration and fixtures."""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def pytest_configure(config):
    """Configure pytest."""
    # Install import hook
    # Hook is automatically installed on import


def pytest_collection_modifyitems(config, items):
    """Modify test collection."""
    # Add markers if needed
    pass
