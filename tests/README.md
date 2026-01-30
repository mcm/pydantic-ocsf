# Testing Strategy

## Philosophy

This project tests **generator behavior**, not generated code coverage. We focus on:

1. **Generator correctness**: Does the generator produce valid Python/Pydantic code?
2. **Output behavior**: Do generated models handle OCSF features correctly?
3. **Edge cases**: Sibling reconciliation, type_uid calculation, circular imports

We **do not** test:
- Pydantic functionality (already tested by Pydantic)
- Every generated model (validated by testing one representative version)
- Old OCSF versions (v1_0_0-v1_6_0 use same generator, tested via v1_7_0)

## Coverage Targets

- **Generator code** (`generator/`): 80%+ (critical business logic)
- **Base code** (`src/ocsf/_*.py`): 90%+ (used by all versions)
- **Generated code** (`src/ocsf/v1_7_0/`): 60%+ (representative sampling)
- **Old versions** (`v1_0_0`-`v1_6_0`): Excluded from coverage

## Test Categories

### 1. Generator Tests (`test_generator.py`)
Tests the code generation logic itself.

**What we test:**
- Type mapping utilities (`ocsf_type_to_python`, `snake_to_pascal`)
- Naming conventions (`label_to_enum_name`, `make_valid_identifier`)
- Schema parsing logic (object registry, sibling detection)
- Schema structure validation

**Why it matters:**
These functions are the core business logic of the generator. Bugs here affect all generated code.

### 2. Generator Output Tests (`test_generator_output.py`)
Validates the structure of generated code.

**What we test:**
- Future annotations present in all files
- TYPE_CHECKING imports used correctly
- Model rebuild logic in version __init__.py
- Generated code is syntactically valid Python
- Models inherit from correct base classes
- No circular import errors

**Why it matters:**
Ensures the generator produces structurally correct code that can be imported and used.

### 3. Output Behavior Tests
Tests that generated models behave correctly with OCSF data.

#### `test_sibling_reconciliation.py`
- activity_id ↔ activity_name synchronization
- ID extrapolates label, label extrapolates ID
- Mismatch detection
- OTHER enum handling

#### `test_sibling_enum.py`
- SiblingEnum base class functionality
- Case-insensitive label matching
- Label property correctness
- IntEnum behavior preservation

#### `test_type_uid_auto_calculation.py`
- type_uid = class_uid × 100 + activity_id
- Auto-calculation when only activity_id provided
- Validation when both provided
- Mismatch detection

#### `test_object_sibling_reconciliation.py`
- Object-level sibling handling
- Nested object sibling reconciliation

#### `test_serialization.py`
- JSON round-tripping
- Unmapped field preservation
- exclude_none behavior

#### `test_circular_imports.py`
- Import resolution for circular dependencies
- Model rebuild correctness

**Why it matters:**
These are the complex, OCSF-specific behaviors that users rely on. Simple validation doesn't test these.

### 4. Complex Object Validation Tests (`test_complex_object_validation.py`)
Tests deeply nested and complex object scenarios.

**What we test:**
- Nested process hierarchies (parent_process chains)
- Unmapped fields in nested structures
- Arrays of objects
- Optional nested objects
- Serialization round-trips of complex data

**Why it matters:**
Real-world OCSF data has deeply nested structures. We need to ensure the generator handles these correctly.

### 5. Snapshot Tests (`test_generator_snapshots.py`)
Regression tests for generator output structure.

**What we test:**
- Key objects have expected structure (Actor, User, File)
- Events have required OCSF fields (class_uid, metadata, etc.)
- Consistency across all events
- Critical validators are present

**Why it matters:**
Prevents accidental regressions in generator output when making changes.

## Running Tests

### All tests with coverage
```bash
just test
```

Or manually:
```bash
pytest tests/ -v --cov=ocsf.v1_7_0 --cov=generator --cov=src/ocsf/_base.py --cov=src/ocsf/_sibling_enum.py
```

### Specific test file
```bash
pytest tests/test_sibling_reconciliation.py -v
```

### Generator tests only
```bash
pytest tests/test_generator.py -v
```

### With HTML coverage report
```bash
pytest tests/ --cov=ocsf.v1_7_0 --cov=generator --cov-report=html
open htmlcov/index.html
```

### Fast tests (skip slow schema fetching)
```bash
pytest tests/ -v -m "not slow"
```

## Coverage Configuration

Coverage is configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=ocsf.v1_7_0 --cov=generator ..."

[tool.coverage.run]
omit = [
    "src/ocsf/v1_0_0/*",  # Old versions excluded
    "src/ocsf/v1_1_0/*",
    # ... other old versions
]
```

**Why exclude old versions?**
- They use the same generator code
- Testing v1_7_0 validates the generator for all versions
- Including them dilutes coverage metrics without adding value

## Adding New Tests

### When adding a generator feature:

1. **Write generator unit test first** (`test_generator.py`)
   ```python
   def test_new_type_mapping():
       assert ocsf_type_to_python("new_type_t") == "NewType"
   ```

2. **Regenerate models**
   ```bash
   just generate
   ```

3. **Add output behavior test** (if complex behavior)
   ```python
   def test_new_feature_behavior():
       event = FileActivity.model_validate(data)
       assert event.new_field == expected_value
   ```

4. **Verify coverage didn't regress**
   ```bash
   pytest tests/ --cov=generator --cov=ocsf.v1_7_0
   ```

### When adding an OCSF feature test:

1. **Identify the behavior to test** (e.g., new enum reconciliation)

2. **Create fixture data** (minimal valid OCSF event)
   ```python
   @pytest.fixture
   def base_event_data(self):
       return {
           "time": 1706000000000,
           "activity_id": 1,
           # ... required fields
       }
   ```

3. **Write test cases** (happy path, edge cases, errors)
   ```python
   def test_new_enum_reconciliation(self, base_event_data):
       data = {**base_event_data, "new_id": 1, "new_name": "Value"}
       event = FileActivity.model_validate(data)
       assert event.new_id == 1
       assert event.new_name == "Value"
   ```

4. **Test error conditions**
   ```python
   def test_new_enum_mismatch_raises(self, base_event_data):
       data = {**base_event_data, "new_id": 1, "new_name": "Wrong"}
       with pytest.raises(ValidationError):
           FileActivity.model_validate(data)
   ```

## Common Testing Patterns

### Fixture for base event data
```python
@pytest.fixture
def base_event_data(self):
    """Minimal valid event data."""
    return {
        "time": 1706000000000,
        "activity_id": 1,
        "severity_id": 4,
        "actor": {"user": {"name": "test", "type_id": 0}},
        "metadata": {
            "version": "1.7.0",
            "product": {"name": "Test", "vendor_name": "Test"}
        }
    }
```

### Testing validation errors
```python
def test_invalid_data_raises(self):
    with pytest.raises(ValidationError) as exc_info:
        FileActivity.model_validate(invalid_data)

    error_msg = str(exc_info.value)
    assert "expected error text" in error_msg
```

### Testing round-trip serialization
```python
def test_roundtrip(self):
    event1 = FileActivity.model_validate(data)
    json_str = event1.model_dump_json()
    event2 = FileActivity.model_validate_json(json_str)

    assert event1.field == event2.field
```

### Testing unmapped fields
```python
def test_unmapped_preserved(self):
    data = {..., "custom_field": "custom_value"}
    event = FileActivity.model_validate(data)
    dumped = event.model_dump()

    assert dumped["custom_field"] == "custom_value"
```

## What NOT to Test

### ❌ Don't test Pydantic functionality
```python
# BAD - This tests Pydantic, not our code
def test_model_has_model_dump():
    assert hasattr(FileActivity, "model_dump")
```

### ❌ Don't test every generated model
```python
# BAD - Testing all 100+ events is redundant
def test_every_event_class():
    for event_class in all_events:
        assert hasattr(event_class, "class_uid")
```

Instead, test a representative sample in snapshot tests.

### ❌ Don't test obvious Python behavior
```python
# BAD - Testing that Python works
def test_can_create_instance():
    event = FileActivity(...)
    assert event is not None
```

### ✅ DO test OCSF-specific behavior
```python
# GOOD - Testing our generator's logic
def test_activity_name_extrapolated_from_id():
    data = {..., "activity_id": 1}  # Only ID, no name
    event = FileActivity.model_validate(data)
    assert event.activity_name == "Create"  # Extrapolated!
```

## Debugging Test Failures

### ImportError or PydanticUndefinedAnnotation
- Check TYPE_CHECKING imports are correct
- Verify model_rebuild() is called with _types_namespace
- Ensure `from __future__ import annotations` is present

### ValidationError in tests
- Check fixture data has all required fields
- Verify enum values are valid for that OCSF version
- Check sibling pairs are consistent (id matches name)

### Coverage dropped unexpectedly
- Run `pytest --cov --cov-report=html` and check htmlcov/
- Verify no new untested code in generator/
- Check if new generated code needs behavioral tests

## CI/CD Integration

Tests run automatically on:
- Every push to main
- Every pull request
- Scheduled nightly builds

**Required checks:**
- All tests pass
- Coverage ≥ 70% for generator code
- Coverage ≥ 60% for v1_7_0 generated code
- No ruff linting errors
- No mypy type errors

## Performance

**Test execution time:**
- Generator tests: ~2s
- Output validation tests: ~5s
- Behavior tests: ~10s
- Total: ~20s

**Coverage calculation adds:** ~3s

**Tips for faster iteration:**
- Run specific test file during development
- Use `-k` flag to run specific tests: `pytest -k "test_sibling"`
- Skip slow tests: `pytest -m "not slow"`

## Questions?

- Check existing tests for similar patterns
- Review generator documentation in `generator/CLAUDE.md`
- Look at recent git commits for examples
- Ask in team chat

## Summary

**Test what matters:**
- Generator correctness ✓
- OCSF-specific behavior ✓
- Complex edge cases ✓

**Don't test:**
- Pydantic internals ✗
- Every generated file ✗
- Obvious Python behavior ✗

**Coverage is about quality, not quantity.** 60-70% coverage with meaningful tests is better than 100% coverage with shallow tests.
