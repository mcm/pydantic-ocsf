# Contributing to pydantic-ocsf

Thank you for your interest in contributing to pydantic-ocsf! This document provides guidelines and instructions for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Project Structure](#project-structure)
- [Common Tasks](#common-tasks)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful, inclusive, and considerate in all interactions.

## Getting Started

### Prerequisites

- Python 3.9 or later
- [uv](https://github.com/astral-sh/uv) package manager
- Git

### Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/pydantic-ocsf.git
cd pydantic-ocsf

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/pydantic-ocsf.git
```

## Development Environment

### Install Dependencies

We use [just](https://github.com/casey/just) as a command runner for common tasks. Install it first:

```bash
# macOS
brew install just

# Linux
cargo install just
# or use your package manager

# Windows
cargo install just
# or use scoop: scoop install just
```

Then install project dependencies:

```bash
# Install all dependencies including dev and generator tools
just install-all

# Or just dev dependencies (without generator)
just install

# Activate the virtual environment (optional, uv run works without this)
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

### Verify Installation

```bash
# Download schemas and regenerate stubs
just rebuild

# Run tests to ensure everything works
just test

# Run all checks (format, lint, typecheck, tests)
just check
```

## Coding Standards

### Python Version Support

- **Target**: Python 3.9+
- **Python 3.9**: Requires `from __future__ import annotations` for `X | Y` union syntax
- **Python 3.10+**: Native support for modern type hints (`X | Y` unions, `list[T]`, etc.)

### Type Hints

All code must include type hints. Use modern Python 3.10+ syntax:

```python
# ✅ Good (Python 3.10+)
def process_events(events: list[dict[str, Any]]) -> list[Event]:
    ...

# ❌ Avoid (old style)
from typing import List, Dict, Any
def process_events(events: List[Dict[str, Any]]) -> List[Event]:
    ...
```

**Type Hint Requirements:**
- All function signatures must have type hints
- Use `| None` instead of `Optional[T]`
- Use built-in generics (`list`, `dict`, `set`, `tuple`) instead of `typing` module
- Use `from __future__ import annotations` to enable forward references

### Code Style

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

#### Formatting

```bash
# Format all code
just format

# Check formatting without changes
just format-check
```

#### Linting

```bash
# Lint all code
just lint

# Auto-fix issues where possible
just lint-fix
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `ModelGenerator`, `SchemaParser`)
- **Functions/Methods**: `snake_case` (e.g., `parse_schema`, `generate_models`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_VERSION`, `CACHE_DIR`)
- **Private members**: Leading underscore (e.g., `_internal_method`, `_globals`)
- **Type variables**: `PascalCase` with `T` prefix (e.g., `TModel`, `TValue`)

### Documentation

#### Docstrings

Use Google-style docstrings for all public functions and classes:

```python
def parse_schema(version: str, cache_dir: Path | None = None) -> ParsedSchema:
    """Parse an OCSF schema from JSON format.

    Args:
        version: OCSF schema version (e.g., "1.7.0")
        cache_dir: Optional directory for caching downloaded schemas

    Returns:
        Parsed schema containing objects, events, and enums

    Raises:
        ValueError: If version format is invalid
        HTTPError: If schema download fails
    """
```

#### Comments

- Use comments to explain **why**, not **what**
- Complex algorithms should have explanatory comments
- Mark critical sections with `# CRITICAL:` or `# IMPORTANT:`

```python
# CRITICAL: Object registry enables detection of object references vs primitives
available_objects = set(raw_schema.get("objects", {}).keys())
```

### Import Organization

Organize imports in this order:

```python
# 1. Future imports
from __future__ import annotations

# 2. Standard library
import json
import sys
from pathlib import Path

# 3. Third-party packages
import httpx
from pydantic import Field

# 4. Local imports
from generator.schema_types import SchemaObject
from generator.utils import snake_to_pascal
```

## Testing Requirements

### Running Tests

```bash
# Run all tests with coverage
just test

# Run with verbose output
just test-verbose

# Run specific test file
uv run pytest tests/test_serialization.py -v

# Run with HTML coverage report
uv run pytest tests/ --cov=ocsf --cov-report=html

# Run tests in parallel (faster)
uv run pytest tests/ -n auto
```

### Test Coverage

- **Minimum coverage**: 80% for new code
- **Target coverage**: 90%+
- View coverage report: Open `htmlcov/index.html` after running with `--cov-report=html`

### Writing Tests

#### Test File Organization

```
tests/
├── test_imports.py          # Import and package structure tests
├── test_serialization.py    # Model serialization/deserialization
├── test_validation.py       # Data validation tests
└── generator/
    ├── test_parser.py       # Schema parsing tests
    ├── test_generator.py    # Code generation tests
    └── test_utils.py        # Utility function tests
```

#### Test Naming

```python
# Test functions: test_<functionality>_<scenario>
def test_model_validates_required_fields():
    ...

def test_circular_imports_resolve_correctly():
    ...

# Test classes: Test<Component>
class TestSchemaParser:
    def test_parses_objects(self):
        ...

    def test_handles_missing_fields(self):
        ...
```

#### Test Structure

Use the Arrange-Act-Assert pattern:

```python
def test_enum_serializes_as_int():
    # Arrange
    file_obj = File(
        name="test.txt",
        type_id=StatusId.VALUE_1,
    )

    # Act
    data = file_obj.model_dump()

    # Assert
    assert isinstance(data["type_id"], int)
    assert data["type_id"] == 1
```

#### Fixtures

Use pytest fixtures for reusable test data:

```python
import pytest
from generator.schema_parser import parse_schema

@pytest.fixture
def parsed_schema():
    """Provide a parsed OCSF schema for tests."""
    return parse_schema("1.7.0")

def test_schema_has_objects(parsed_schema):
    assert len(parsed_schema.objects) > 0
```

### Test Types

#### 1. Unit Tests

Test individual functions in isolation:

```python
def test_snake_to_pascal():
    from generator.utils import snake_to_pascal

    assert snake_to_pascal("api_activity") == "ApiActivity"
    assert snake_to_pascal("http_request") == "HttpRequest"
```

#### 2. Integration Tests

Test components working together:

```python
def test_generated_models_import_successfully():
    """Verify circular imports are resolved."""
    from ocsf.v1_7_0.objects import User, LdapPerson

    # Should not raise ImportError
    assert User is not None
    assert LdapPerson is not None
```

#### 3. Validation Tests

Test data validation with real-world scenarios:

```python
def test_api_activity_validates_correctly():
    from ocsf.v1_7_0.events import ApiActivity
    from pydantic import ValidationError

    # Valid data should pass
    valid_data = {
        "class_uid": 3,
        "actor": {"user": {"name": "alice"}},
        "api": {"operation": "Read"},
        "metadata": {
            "version": "1.7.0",
            "product": {"name": "Test"}
        }
    }
    event = ApiActivity.model_validate(valid_data)
    assert event.api.operation == "Read"

    # Invalid data should fail
    invalid_data = {"class_uid": 3}  # Missing required fields
    with pytest.raises(ValidationError):
        ApiActivity.model_validate(invalid_data)
```

## Pull Request Process

### Before Submitting

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following the coding standards
   - Add tests for new functionality
   - Update documentation if needed

3. **Run the full test suite**
   ```bash
   # Run all checks (format, lint, typecheck, tests)
   just check

   # Or run individually:
   just format        # Format code
   just lint          # Run linter
   just typecheck     # Type check
   just test          # Run tests with coverage
   ```

4. **Regenerate models if you changed the generator or schemas**
   ```bash
   # Download schemas and regenerate stubs
   just rebuild

   # Verify generated code works
   just test
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add support for new OCSF field type"
   ```

   **Commit Message Format:**
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `test:` Adding or updating tests
   - `refactor:` Code refactoring
   - `perf:` Performance improvement
   - `chore:` Maintenance tasks

### Submitting the PR

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request on GitHub**
   - Provide a clear title and description
   - Reference any related issues
   - Include screenshots/examples if applicable

3. **PR Description Template**
   ```markdown
   ## Description
   Brief description of the changes

   ## Motivation
   Why are these changes needed?

   ## Changes
   - List of changes
   - Another change

   ## Testing
   - [ ] All tests pass
   - [ ] Added tests for new functionality
   - [ ] Manually tested with sample data

   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Documentation updated
   - [ ] No breaking changes (or documented if necessary)
   ```

### Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged

## Project Structure

```
pydantic-ocsf/
├── src/ocsf/                    # OCSF package source
│   ├── __init__.py              # Package entry point with JIT import hook
│   ├── _base.py                 # Base model class (OCSFBaseModel)
│   ├── _import_hook.py          # JIT import hook for version modules
│   ├── _schema_loader.py        # Schema loading and caching
│   ├── _model_factory.py        # Dynamic model generation
│   ├── _version_module.py       # Version module implementation
│   ├── _namespace_module.py     # Namespace module (objects/events)
│   ├── schemas/                 # OCSF schema JSON files (generated, gitignored)
│   │   ├── v1_0_0.json
│   │   ├── v1_7_0.json
│   │   └── checksums.json
│   └── v1_7_0/                  # Type stubs for v1.7.0 (generated, gitignored)
│       ├── __init__.pyi
│       ├── objects.pyi          # Object type stubs
│       └── events.pyi           # Event type stubs
├── scripts/                     # Build and generation scripts
│   ├── download_schemas.py      # Downloads OCSF schemas from GitHub
│   └── regenerate_stubs.py      # Generates .pyi stub files
├── tests/                       # Test suite
│   ├── test_import_hook.py      # Import mechanism tests
│   ├── test_namespace_separation.py
│   ├── test_model_factory.py
│   ├── test_circular_deps.py
│   └── conftest.py
├── .github/workflows/           # CI/CD workflows
│   ├── test.yml                 # Test workflow
│   └── publish.yml              # PyPI publishing workflow
├── justfile                     # Command runner (build tasks)
├── pyproject.toml               # Project configuration
├── CHANGELOG.md                 # Release notes
├── README.md                    # User documentation
└── CONTRIBUTING.md              # This file
```

**Key Directories:**
- **`src/ocsf/`**: Package source code with JIT model generation system
- **`src/ocsf/schemas/`**: OCSF schema JSON files (generated, not tracked in git)
- **`src/ocsf/v*/`**: Type stub files for IDE autocomplete (generated, not tracked in git)
- **`scripts/`**: Schema download and stub generation scripts
- **`tests/`**: Comprehensive test suite

## Common Tasks

### Regenerating Models

Schemas are downloaded and stubs regenerated using the justfile:

```bash
# Download all OCSF schemas and regenerate stubs
just rebuild

# Or run steps individually:
just download-schemas    # Download schemas to src/ocsf/schemas/
just regenerate-stubs   # Generate .pyi stub files
```

### Adding a New OCSF Version

1. Check available versions at https://github.com/ocsf/ocsf-schema/releases
2. Update `scripts/download_schemas.py` to include the new version in the `VERSIONS` list
3. Download and generate: `just rebuild`
4. Test the new version: `just test`
5. Update documentation to mention the new version

### Debugging Generated Code

```bash
# Check for Any usage (should be minimal)
grep -r "Any = Field" src/ocsf/v1_7_0/ | wc -l

# Check imports for specific model
head -50 src/ocsf/v1_7_0/events/api_activity.py

# Test specific import
uv run python -c "from ocsf.v1_7_0.events import ApiActivity; print('OK')"

# Check type annotations
uv run python -c "
from ocsf.v1_7_0.events import ApiActivity
print('actor:', ApiActivity.__annotations__['actor'])
print('api:', ApiActivity.__annotations__['api'])
"
```

### Updating Dependencies

```bash
# Update all dependencies
uv lock --upgrade

# Update specific package
uv add pydantic@latest

# Re-sync environment
uv sync
```

### Performance Profiling

```bash
# Profile schema download and stub generation time
time just rebuild

# Profile with cProfile (for individual scripts)
uv run python -m cProfile -o profile.stats scripts/download_schemas.py
uv run python -m cProfile -o profile.stats scripts/regenerate_stubs.py

# Analyze profile
uv run python -m pstats profile.stats
```

## Getting Help

### Documentation

- **User Guide**: `CLAUDE.md` in project root
- **Generator Guide**: `generator/CLAUDE.md`
- **API Reference**: Generated from docstrings (TODO: Sphinx setup)

### Communication

- **Issues**: Use GitHub Issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Security**: Email security@example.com for security issues

### Resources

- OCSF Schema: https://schema.ocsf.io/
- Pydantic Docs: https://docs.pydantic.dev/
- Python Type Hints: https://mypy.readthedocs.io/

## Release Process

(For maintainers)

This project uses [Semantic Versioning](https://semver.org/) starting with v2.0.0:
- **Major** (X.0.0): Breaking changes
- **Minor** (2.X.0): New features (backward compatible)
- **Patch** (2.0.X): Bug fixes

### Creating a Release

1. **Update version in `pyproject.toml`**
   ```toml
   version = "2.1.0"  # Example: new minor version
   ```

2. **Update `src/ocsf/__init__.py`**
   ```python
   __version__ = "2.1.0"
   ```

3. **Update CHANGELOG.md** with release notes
   - Add new version section at the top
   - Document breaking changes, new features, bug fixes
   - Follow [Keep a Changelog](https://keepachangelog.com/) format

4. **Commit changes**
   ```bash
   git add pyproject.toml src/ocsf/__init__.py CHANGELOG.md
   git commit -m "chore: prepare release v2.1.0"
   ```

5. **Create and push tag** (must match pyproject.toml version)
   ```bash
   git tag v2.1.0
   git push origin main
   git push origin v2.1.0
   ```

6. **GitHub Actions will automatically:**
   - Validate the tag matches `pyproject.toml` version
   - Download schemas and regenerate stubs
   - Build the distribution
   - Publish to PyPI
   - Create a GitHub release with CHANGELOG excerpt

**Important**: The git tag version (without `v` prefix) must exactly match the version in `pyproject.toml`, or the workflow will fail.

### Version Numbering Guidelines

- **v2.0.x → v2.1.0**: Adding new OCSF schema versions (backward compatible)
- **v2.0.x → v2.0.y**: Bug fixes, stub regeneration, documentation updates
- **v2.x → v3.0.0**: Removing schema versions, API changes, breaking changes

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

## Questions?

If you have questions not covered here, please open a GitHub Discussion or contact the maintainers.

Thank you for contributing! 🎉
