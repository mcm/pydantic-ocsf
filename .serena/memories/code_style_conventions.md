# Code Style and Conventions for pydantic-ocsf

## Python Version
- **Target**: Python 3.9+ (must support 3.9, 3.10, 3.11, 3.12, 3.13, 3.14)
- **Type Hints**: Use Python 3.9+ built-in generic types (list, dict, set, tuple)
- **Union Types**: Use `|` syntax for Python 3.10+ where appropriate, but support 3.9

## Type Hints (Python 3.12 Best Practices)
Per project CLAUDE.md, use built-in generic types:
```python
# Preferred
def process(names: list[str]) -> dict[str, int]:
    return {name: len(name) for name in names}

# Avoid (old style)
from typing import List, Dict
def process(names: List[str]) -> Dict[str, int]:
    ...
```

## Import Organization
```python
from __future__ import annotations  # Always first

# Standard library imports
import sys
from pathlib import Path

# Third-party imports
from pydantic import BaseModel, Field

# Local imports
from ocsf._base import OCSFBaseModel
```

## Docstrings
- **Format**: Google style
- **Required**: All public classes, functions, methods
- **Example**:
```python
def create_model(name: str, definition: dict) -> type[BaseModel]:
    """Create a Pydantic model from OCSF schema definition.
    
    Args:
        name: The model class name
        definition: OCSF schema definition dictionary
    
    Returns:
        A Pydantic model class
    
    Raises:
        ValueError: If definition is invalid
    """
```

## Naming Conventions
- **Classes**: PascalCase (`FileActivity`, `SiblingEnum`)
- **Functions/Methods**: snake_case (`create_model`, `load_schema`)
- **Constants**: UPPER_SNAKE_CASE (`TYPE_MAP`, `VERSION_PATTERN`)
- **Private**: Prefix with `_` (`_model_cache`, `_load_schema`)

## Pydantic Patterns
- Use `create_model()` for dynamic model creation
- Use `model_rebuild()` for forward reference resolution
- Use `model_validator(mode='before')` for pre-validation logic
- Configure with `ConfigDict` (not `Config` class)

## Error Handling
- Custom exceptions in `_exceptions.py`
- Helpful error messages with suggestions
- Include available options in error messages

## Logging
```python
import logging
logger = logging.getLogger("ocsf")
logger.debug(f"Creating model {name}")  # Use f-strings
```

## Ruff Configuration
- **Line length**: 100 characters
- **Target**: Python 3.9
- **Selected rules**: ANN, E, F, I, UP, B, SIM, S
- **Ignored**: ANN401 (Any is acceptable), E501 (line length handled by formatter), S101 (assert is fine)

## Mypy Configuration
- **Strict mode**: Enabled
- **Python version**: 3.9
- **Warn unused ignores**: True

## Testing Conventions
- Use pytest fixtures in `conftest.py`
- Test file names: `test_<module>.py`
- Test class names: `TestClassName`
- Test method names: `test_descriptive_name`
- Use markers: `@pytest.mark.benchmark` for performance tests

## Module Organization
- Public API in `__init__.py`
- Implementation in private modules (`_import_hook.py`, `_factory.py`)
- Base classes in `_base.py`
- Exceptions in `_exceptions.py`
- Mark package as typed with `py.typed` file