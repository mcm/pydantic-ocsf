# Generator Architecture Guide

This document is for AI assistants (like Claude Code) working on the OCSF Pydantic model generator. It explains the architecture, critical patterns, and common pitfalls.

## Overview

The generator creates Pydantic v2 models from OCSF JSON schemas. It handles:
- **Schema Fetching**: Downloads OCSF schemas from GitHub
- **Type Detection**: Identifies object references vs primitives
- **Circular Imports**: Resolves circular dependencies between models
- **Template Rendering**: Generates Python code via Jinja2 templates
- **Code Formatting**: Applies ruff formatting and linting

## Architecture

```
generator/
├── schema_fetcher.py     # Downloads OCSF schemas from GitHub
├── schema_parser.py      # Parses JSON schema into typed structures
├── schema_types.py       # Type definitions for parsed schema
├── model_generator.py    # Orchestrates code generation
├── utils.py              # Type mapping and naming utilities
└── templates/            # Jinja2 templates for code generation
    ├── enum.py.jinja2
    ├── object.py.jinja2
    ├── event.py.jinja2
    └── init.py.jinja2
```

## Critical Pattern: Circular Import Resolution

### The Problem

OCSF has circular dependencies:
```
User → LdapPerson → User
Process → File → Process
```

Python doesn't allow circular imports at module level.

### The Solution (DO NOT BREAK THIS!)

We use a three-part strategy:

#### 1. `from __future__ import annotations`
Makes all annotations strings, delaying evaluation:
```python
from __future__ import annotations

class User:
    manager: LdapPerson  # String at runtime, not evaluated
```

#### 2. TYPE_CHECKING Imports
Imports only happen during type checking, not runtime:
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ocsf.v1_7_0.objects.user import User
```

This avoids the circular import because:
- `TYPE_CHECKING` is `False` at runtime
- Imports never execute during module loading
- But type checkers (mypy, pyright) still see the imports

#### 3. Deferred Model Rebuilding
After all modules load, we rebuild models with correct namespace:
```python
# In version-level __init__.py after all imports
def _rebuild_models() -> None:
    _globals = sys.modules[__name__].__dict__
    User.model_rebuild(_types_namespace=_globals)
    LdapPerson.model_rebuild(_types_namespace=_globals)
    # ... all other models
```

The `_types_namespace` parameter tells Pydantic where to find the referenced types. Without it, Pydantic can't resolve forward references.

### How It Works

1. **Import Phase**: All modules import with TYPE_CHECKING blocks, no circular imports occur
2. **Version __init__.py**: Imports all models via `from ocsf.v1_7_0.objects import *`
3. **Rebuild Phase**: Calls `model_rebuild(_types_namespace=_globals)` on each model
4. **Resolution**: Pydantic resolves string annotations using the provided namespace

## Schema Parsing Flow

### 1. Fetch Schema (`schema_fetcher.py`)

```python
def fetch_schema(version: str, cache_dir: Path | None = None) -> dict[str, Any]:
    # Downloads from https://github.com/ocsf/ocsf-schema/releases/
    # Caches locally to avoid repeated downloads
```

### 2. Parse Schema (`schema_parser.py`)

```python
def parse_schema(version: str, cache_dir: Path | None = None) -> ParsedSchema:
    raw_schema = fetch_schema(version, cache_dir)
    dictionary = raw_schema.get("dictionary")

    # CRITICAL: Build object registry for type detection
    available_objects = set(raw_schema.get("objects", {}).keys())

    # Parse with object registry
    for name, obj_data in raw_schema.get("objects", {}).items():
        parsed.objects[name] = SchemaObject.from_dict(
            name, obj_data, dictionary, available_objects
        )
```

**Why `available_objects` is Critical:**

The OCSF schema represents object references as:
```json
{
  "actor": {
    "type": "actor",  // Object name, not "object_t"
    "description": "..."
  }
}
```

Without the registry, the parser can't distinguish:
- `"type": "string_t"` → primitive type
- `"type": "actor"` → object reference

The registry enables detection in `SchemaAttribute.from_dict()`:
```python
if available_objects and type_value in available_objects:
    object_type_value = type_value  # "actor"
    type_value = "object_t"  # Normalize for downstream code
```

### 3. Type Mapping (`utils.py`)

```python
def ocsf_type_to_python(ocsf_type: str, object_type: str | None = None) -> str:
    # Maps OCSF types to Python type annotations
    if ocsf_type == "object_t" and object_type:
        return snake_to_pascal(object_type)  # "actor" → "Actor"
    # ... handle primitives, arrays, etc.
```

### 4. Code Generation (`model_generator.py`)

```python
class ModelGenerator:
    def generate(self, output_dir: Path) -> None:
        # 1. Generate enums (no dependencies)
        self._generate_enums(...)

        # 2. Generate objects (may have circular deps)
        self._generate_objects(...)

        # 3. Generate events (reference objects)
        self._generate_events(...)

        # 4. Generate __init__.py with rebuild logic
        self._generate_init_files(...)
```

## Template System

### Object Template (`templates/object.py.jinja2`)

Key sections:
```jinja2
from __future__ import annotations  {# Critical for forward refs #}

from typing import TYPE_CHECKING, Any

{% if imports %}
if TYPE_CHECKING:
{% for import_line in imports %}
    {{ import_line }}
{% endfor %}
{% endif %}

class {{ class_name }}(OCSFBaseModel):
    {% for attr in attributes %}
    {{ attr.field_name }}: {{ attr.type_annotation }} = Field(...)
    {% endfor %}
```

### Init Template (`templates/init.py.jinja2`)

Key sections:
```jinja2
{% if rebuild_models %}
def _rebuild_models() -> None:
    import sys
    _globals = sys.modules[__name__].__dict__
    {% for model_info in rebuild_models %}
    {{ model_info.name }}.model_rebuild(_types_namespace=_globals)
    {% endfor %}

if __name__ != "__main__":
    _rebuild_models()
{% endif %}
```

**Important**: Only the version-level `__init__.py` gets the rebuild logic. The enums, objects, and events `__init__.py` files don't need it.

## Common Tasks

### Adding a New OCSF Field Type

1. Update `utils.py:ocsf_type_to_python()`:
```python
def ocsf_type_to_python(ocsf_type: str, ...) -> str:
    type_map = {
        # ... existing types
        "new_type_t": "NewPythonType",
    }
```

2. If it's a complex type, update `SchemaAttribute.from_dict()` in `schema_types.py`

3. Regenerate and test:
```bash
uv run python scripts/generate.py
uv run pytest tests/
```

### Modifying Template Output

1. Edit the appropriate template in `generator/templates/`
2. Remember: Changes affect ALL generated files
3. Test thoroughly with circular dependency cases:
```bash
# Check User/LdapPerson can import
uv run python -c "from ocsf.v1_7_0.objects import User, LdapPerson"
```

### Debugging Type Resolution Issues

If you see `PydanticUndefinedAnnotation` errors:

1. **Check TYPE_CHECKING imports**: Verify imports are under `if TYPE_CHECKING:`
2. **Check rebuild logic**: Ensure `_types_namespace=_globals` is passed
3. **Check object registry**: Verify `available_objects` is built and passed through parsing
4. **Test import order**:
```python
# This should work:
from ocsf.v1_7_0 import User, LdapPerson

# This might not (model not rebuilt yet):
from ocsf.v1_7_0.objects.user import User
```

## Performance Considerations

### Generation Time
- Parsing: ~1 second
- Code generation: ~2 seconds
- Formatting (ruff): ~5 seconds
- **Total**: ~8 seconds for full regeneration

### Import Time
- First import of version package: ~1-2 seconds (model rebuild)
- Individual model import: <50ms
- The rebuild happens once per Python process

### Memory Usage
- Parsed schema: ~10MB
- Generated code: ~50MB per version
- Runtime (all models loaded): ~100MB

## Pitfalls to Avoid

### ❌ DON'T: Remove TYPE_CHECKING
```python
# This causes circular imports!
from ocsf.v1_7_0.objects.user import User
```

### ✅ DO: Keep TYPE_CHECKING
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ocsf.v1_7_0.objects.user import User
```

### ❌ DON'T: Call model_rebuild() without namespace
```python
User.model_rebuild()  # Can't find referenced types!
```

### ✅ DO: Pass namespace to model_rebuild()
```python
_globals = sys.modules[__name__].__dict__
User.model_rebuild(_types_namespace=_globals)
```

### ❌ DON'T: Forget `from __future__ import annotations`
```python
# Without this, annotations are evaluated immediately
class User:
    manager: LdapPerson  # NameError: LdapPerson not defined
```

### ✅ DO: Always use future annotations
```python
from __future__ import annotations

class User:
    manager: LdapPerson  # String annotation, evaluated later
```

### ❌ DON'T: Modify generated files manually
All generated files are overwritten on regeneration. Make changes in templates.

### ✅ DO: Update templates and regenerate
```bash
# Edit template
vim generator/templates/object.py.jinja2

# Regenerate
uv run python scripts/generate.py
```

## Testing Your Changes

### Unit Tests
```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test
uv run pytest tests/test_serialization.py -v

# With coverage
uv run pytest tests/ --cov=src/ocsf --cov-report=html
```

### Integration Tests
```bash
# Test circular imports
uv run python -c "
from ocsf.v1_7_0.objects import User, LdapPerson
from ocsf.v1_7_0.events import ApiActivity
print('Success!')
"

# Test type annotations
uv run python -c "
from ocsf.v1_7_0.events import ApiActivity
print('actor:', ApiActivity.__annotations__['actor'])
"
```

### Verification Checklist
After making changes:
- [ ] All tests pass: `uv run pytest tests/ -v`
- [ ] No circular import errors
- [ ] Type annotations are correct (not `Any`)
- [ ] Ruff linting passes: `uv run ruff check src/`
- [ ] Generated code is formatted: `uv run ruff format src/`

## Version Scheme

The package uses a date-based version scheme:
```
{ocsf_version}.{generation_date}
```

Example: `1.7.0.20260129` means OCSF v1.7.0 generated on 2026-01-29

This is set in `scripts/generate.py:get_package_version()`

## Code Style

### Python Version
Target: Python 3.9+

**Important**: The generated code uses `X | Y` union syntax (Python 3.10+ feature), but it works on Python 3.9 because all generated files include `from __future__ import annotations`, which makes annotations strings. Pydantic v2 can parse these string annotations on Python 3.9.

### Type Hints
Use modern syntax:
```python
# Good (Python 3.10+)
def foo(items: list[str]) -> dict[str, int]:
    ...

# Avoid (old style)
from typing import List, Dict
def foo(items: List[str]) -> Dict[str, int]:
    ...
```

### Naming Conventions
- **Classes**: PascalCase (`ApiActivity`, `HttpRequest`)
- **Functions**: snake_case (`parse_schema`, `ocsf_type_to_python`)
- **Constants**: UPPER_SNAKE_CASE (`TYPE_CHECKING`)
- **Private**: Leading underscore (`_rebuild_models`, `_globals`)

## Helpful Commands

```bash
# Regenerate all models
uv run python scripts/generate.py

# Format generator code
uv run ruff format generator/ scripts/

# Lint generator code
uv run ruff check generator/ scripts/

# Check types with mypy
uv run mypy generator/ --strict

# Profile generation time
time uv run python scripts/generate.py

# Count Any usage (should be ~5)
grep -r "Any = Field" src/ocsf/v1_7_0/ | wc -l
```

## Getting Help

### OCSF Schema Questions
- Schema docs: https://schema.ocsf.io/
- Schema repo: https://github.com/ocsf/ocsf-schema
- Browse raw schema: https://github.com/ocsf/ocsf-schema/tree/main/objects

### Pydantic Questions
- Pydantic docs: https://docs.pydantic.dev/
- Forward references: https://docs.pydantic.dev/latest/concepts/postponed_annotations/
- model_rebuild(): https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_rebuild

### Project-Specific Issues
- Review git history for similar changes
- Check closed issues in the repo
- Read the plan file at `/home/coder/.claude/plans/` for recent architectural decisions

## Summary

The generator's complexity comes from one core challenge: **circular imports**. Everything else is straightforward template-based code generation.

The circular import solution has three parts:
1. `from __future__ import annotations` - delays annotation evaluation
2. `TYPE_CHECKING` blocks - avoids runtime imports
3. Deferred `model_rebuild(_types_namespace=_globals)` - resolves forward references

**Never break these three parts.** They work together as a system.

When in doubt, check the generated `src/ocsf/v1_7_0/__init__.py` file - it contains the rebuild logic that makes everything work.
