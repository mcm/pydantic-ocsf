"""Custom exceptions for OCSF JIT model factory."""

from __future__ import annotations


class OCSFError(Exception):
    """Base exception for all OCSF errors."""

    pass


class VersionNotFoundError(OCSFError):
    """Raised when a requested OCSF version is not available.

    Attributes:
        version: The version that was requested
        available_versions: List of available versions
    """

    def __init__(self, version: str, available_versions: list[str]) -> None:
        self.version = version
        self.available_versions = available_versions
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """Format error message with suggestions."""
        msg = f"OCSF version {self.version!r} not found."
        if self.available_versions:
            msg += f"\n\nAvailable versions: {', '.join(self.available_versions)}"
        return msg


class ModelNotFoundError(OCSFError):
    """Raised when a requested model is not available in a version.

    Attributes:
        model_name: The model that was requested
        version: The version that was searched
        available_models: List of available models in that version
    """

    def __init__(self, model_name: str, version: str, available_models: list[str]) -> None:
        self.model_name = model_name
        self.version = version
        self.available_models = available_models
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        """Format error message with suggestions."""
        msg = f"Model {self.model_name!r} not found in OCSF version {self.version}."

        # Try to find close matches
        suggestions = self._find_similar_names()
        if suggestions:
            msg += "\n\nDid you mean one of these?\n  " + "\n  ".join(suggestions)
        elif self.available_models:
            msg += f"\n\nAvailable models: {len(self.available_models)} total"

        return msg

    def _find_similar_names(self) -> list[str]:
        """Find similar model names using basic string matching."""
        if not self.available_models:
            return []

        search_lower = self.model_name.lower()
        matches = []

        for name in self.available_models:
            name_lower = name.lower()
            # Exact substring match
            if (
                search_lower in name_lower
                or name_lower in search_lower
                or len(search_lower) >= 3
                and name_lower.startswith(search_lower[:3])
            ):
                matches.append(name)

        return matches[:5]  # Limit to top 5 suggestions


class SchemaError(OCSFError):
    """Raised when schema data is invalid or corrupted.

    Attributes:
        message: Description of the schema error
        version: The version with the invalid schema (optional)
    """

    def __init__(self, message: str, version: str | None = None) -> None:
        self.message = message
        self.version = version
        if version:
            super().__init__(f"Invalid schema for version {version}: {message}")
        else:
            super().__init__(f"Invalid schema: {message}")
