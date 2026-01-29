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

```bash
# Install all dependencies including dev tools
uv sync

# Activate the virtual environment (optional, uv run works without this)
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

### Verify Installation

```bash
# Run tests to ensure everything works
uv run pytest tests/ -v

# Check that generation works
uv run python scripts/generate.py
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
uv run ruff format .

# Check formatting without changes
uv run ruff format --check .
```

#### Linting

```bash
# Lint all code
uv run ruff check .

# Auto-fix issues where possible
uv run ruff check --fix .
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
# Run all tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_serialization.py -v

# Run with coverage report
uv run pytest tests/ --cov=src/ocsf --cov-report=html

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
   # Format code
   uv run ruff format .

   # Run linter
   uv run ruff check .

   # Run tests
   uv run pytest tests/ -v

   # Check coverage
   uv run pytest tests/ --cov=src/ocsf --cov-report=term-missing
   ```

4. **Regenerate models if you changed the generator**
   ```bash
   uv run python scripts/generate.py

   # Verify generated code works
   uv run pytest tests/ -v
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
├── src/ocsf/              # Generated OCSF models (DO NOT EDIT MANUALLY)
│   ├── __init__.py
│   ├── _base.py           # Base model class
│   └── v1_7_0/            # OCSF version 1.7.0
│       ├── events/        # Event classes
│       ├── objects/       # Object classes
│       └── enums/         # Enum classes
├── generator/             # Code generation system
│   ├── schema_fetcher.py  # Downloads OCSF schemas
│   ├── schema_parser.py   # Parses JSON schemas
│   ├── schema_types.py    # Schema type definitions
│   ├── model_generator.py # Generates Python code
│   ├── utils.py           # Helper functions
│   └── templates/         # Jinja2 templates
├── scripts/               # Utility scripts
│   └── generate.py        # Main generation script
├── tests/                 # Test suite
│   ├── test_imports.py
│   ├── test_serialization.py
│   └── generator/         # Generator-specific tests
├── pyproject.toml         # Project configuration
└── README.md              # Project documentation
```

## Common Tasks

### Regenerating Models

```bash
# Regenerate all OCSF versions
uv run python scripts/generate.py

# Generate specific version (TODO: add version flag support)
# Currently generates all versions
```

### Adding a New OCSF Version

1. Check available versions at https://github.com/ocsf/ocsf-schema/releases
2. Update `scripts/generate.py` to include the new version
3. Generate models: `uv run python scripts/generate.py`
4. Test the new version: `uv run pytest tests/ -v`

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
# Profile generation time
time uv run python scripts/generate.py

# Profile with cProfile
uv run python -m cProfile -o profile.stats scripts/generate.py

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

1. **Update version in `pyproject.toml`** to match the release version (e.g., `1.7.0.20260129`)
2. **Update CHANGELOG.md** with release notes
3. **Commit changes**: `git commit -am "chore: prepare release 1.7.0.20260129"`
4. **Create release tag**: `git tag v1.7.0.20260129` (note: tag must match pyproject.toml version)
5. **Push changes and tag**: `git push && git push --tags`
6. GitHub Actions will:
   - Validate the tag matches `pyproject.toml` version
   - Build and publish to PyPI
   - Create a GitHub release

**Important**: The git tag version (without `v` prefix) must exactly match the version in `pyproject.toml`, or the workflow will fail.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

## Questions?

If you have questions not covered here, please open a GitHub Discussion or contact the maintainers.

Thank you for contributing! 🎉
