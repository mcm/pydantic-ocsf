"""Import hook for transparent JIT model creation.

This module installs a Python import hook that intercepts imports of
ocsf.v* modules and returns OCSFVersionModule instances that create
models on-demand.
"""

from __future__ import annotations

import importlib.abc
import importlib.machinery
import re
import sys
from collections.abc import Sequence
from types import ModuleType

from ocsf._exceptions import VersionNotFoundError
from ocsf._schema_loader import get_schema_loader


class OCSFImporter(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """Import hook for OCSF JIT modules.

    Intercepts imports of:
    - ocsf (root package)
    - ocsf.v1_7_0 (version module)
    """

    def find_spec(
        self,
        fullname: str,
        path: Sequence[str] | None,
        target: ModuleType | None = None,
    ) -> importlib.machinery.ModuleSpec | None:
        """Check if this is an OCSF module we should handle.

        Args:
            fullname: Full module name (e.g., "ocsf.v1_7_0", "ocsf.v1_7_0.objects")
            path: Parent module's __path__ attribute
            target: Target module (unused)

        Returns:
            ModuleSpec if we should handle this import, None otherwise
        """
        parts = fullname.split(".")

        # Handle: ocsf, ocsf.v1_7_0, ocsf.v1_7_0.objects, etc.
        if len(parts) >= 1 and parts[0] == "ocsf":
            if len(parts) == 1:
                # Just 'ocsf' - let normal import handle it
                return None
            elif len(parts) == 2 and parts[1].startswith("v"):
                # ocsf.v1_7_0 - mark as package (has submodules)
                return importlib.machinery.ModuleSpec(fullname, self, is_package=True)
            elif len(parts) == 3 and parts[1].startswith("v") and parts[2] in ("objects", "events"):
                # ocsf.v1_7_0.objects or ocsf.v1_7_0.events
                return importlib.machinery.ModuleSpec(fullname, self, is_package=False)

        return None

    def create_module(self, spec: importlib.machinery.ModuleSpec) -> ModuleType | None:
        """Create the module object.

        Args:
            spec: Module specification

        Returns:
            Created module instance

        Raises:
            ImportError: If the version format is invalid or not found
        """
        from ocsf._namespace_module import OCSFNamespaceModule
        from ocsf._version_module import OCSFVersionModule

        fullname = spec.name
        parts = fullname.split(".")

        if len(parts) == 2:
            # ocsf.v1_7_0
            version_name = parts[1]
            m = re.match(r"v(\d+)_(\d+)_(\d+)", version_name)
            if not m:
                raise ImportError(f"Invalid OCSF version format: {version_name}")

            version = ".".join(m.groups())
            if version_name.endswith("_dev"):
                version = f"{version}-dev"

            # Check if version exists
            loader = get_schema_loader()
            available = loader.get_available_versions()
            if version not in available:
                raise VersionNotFoundError(version, available)

            # Create version module
            module = OCSFVersionModule(fullname, version)
            return module

        elif len(parts) == 3:
            # ocsf.v1_7_0.objects or ocsf.v1_7_0.events
            parent_name = ".".join(parts[:2])
            namespace_type = parts[2]

            # Ensure parent module is loaded first
            if parent_name not in sys.modules:
                # Trigger parent import
                parent_spec = self.find_spec(parent_name, None, None)
                if parent_spec and parent_spec.loader:
                    parent_module = parent_spec.loader.create_module(parent_spec)
                    if parent_module:
                        sys.modules[parent_name] = parent_module
                        parent_spec.loader.exec_module(parent_module)

            parent_module = sys.modules.get(parent_name)
            if parent_module is None:
                raise ImportError(f"Cannot import {fullname}: parent module not found")

            # Type assertion: we know parent_module is OCSFVersionModule
            if not isinstance(parent_module, OCSFVersionModule):
                raise ImportError(
                    f"Cannot import {fullname}: parent module is not an OCSFVersionModule"
                )

            namespace_module = OCSFNamespaceModule(fullname, parent_module, namespace_type)
            return namespace_module

        raise ImportError(f"Cannot import {fullname}")

    def exec_module(self, module: ModuleType) -> None:
        """Execute module and register in sys.modules.

        Args:
            module: Module to execute
        """
        # Ensure the module is in sys.modules
        sys.modules[module.__name__] = module


def install_hook() -> None:
    """Install the OCSF import hook.

    This should be called once when the ocsf package is imported.
    It's safe to call multiple times (idempotent).
    """
    # Check if already installed
    for finder in sys.meta_path:
        if isinstance(finder, OCSFImporter):
            return

    # Install at the beginning of meta_path
    sys.meta_path.insert(0, OCSFImporter())
