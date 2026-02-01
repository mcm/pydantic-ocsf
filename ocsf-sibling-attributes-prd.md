# Product Requirements Document: OCSF Sibling Attribute Handling

## A Feature for pydantic-ocsf Enabling Developer-Friendly Enum Usage for OCSF Sibling Attributes

**Version:** 1.0  
**Last Updated:** January 2026  
**Status:** Approved for Implementation

---

## 1. Executive Summary

### 1.1 Overview

OCSF Sibling Attribute Handling is a feature for pydantic-ocsf that provides developer-friendly enums for OCSF's sibling attribute pattern. OCSF frequently pairs a numeric ID field (`foo_id`) with a string label field (`foo`), where the ID is required but developers typically work with human-readable labels. This feature generates context-specific enums as nested classes that allow developers to use meaningful names while maintaining type safety and proper validation.

### 1.2 Problem Statement

Developers working with OCSF face friction when creating events:

- **Magic numbers**: Required ID fields like `activity_id=1` provide no context about what the value means
- **Context sensitivity**: The same attribute name (e.g., `ActivityId`) has different valid values depending on the event class
- **Manual lookup**: Developers must consult OCSF documentation to find the correct numeric ID for a label
- **No type safety**: Using generic integers allows invalid values to pass type checking
- **IDE blindness**: Without proper enums, IDE autocomplete cannot suggest valid values

### 1.3 Solution

Generate context-specific enum classes nested within each event class for sibling attributes that:

- Use human-readable member names matching OCSF labels
- Support construction from both numeric ID and string label
- Provide full IDE autocomplete with valid options per event class
- Integrate seamlessly with Pydantic validation
- Handle the `Other` (99) case with custom labels per OCSF specification
- Automatically reconcile sibling pairs during parsing

### 1.4 Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Enum naming | `{EventClass}.{AttributeName}` (nested) | Clean API: `FileActivity.ActivityId.CREATE` |
| Base class | Custom `IntEnum` subclass | Integer serialization + string lookup |
| String lookup | Constructor accepts string | Matches desired API: `SeverityId("medium")` |
| Mismatch handling | `ValidationError` | No safe way to be lenient |
| Case sensitivity | Lenient parse, strict output | User-friendly input, canonical output |
| Unknown ID values | `ValidationError` | IDs must be in enum |
| Unknown string values | Map to `Other` (99) | Per OCSF spec, preserve custom label |
| Serialization | Always include both fields | Complete output |
| Scope | `_id` + base name siblings only | `_uid`/`_name` pairs out of scope |

---

## 2. User Stories and Requirements

### 2.1 Target Users

| Persona | Description | Primary Use Case |
|---------|-------------|------------------|
| Security Engineer | Builds security data pipelines | Creating events with correct activity/severity IDs |
| Application Developer | Integrates OCSF into applications | Producing compliant events without memorizing IDs |
| Data Engineer | Processes security telemetry | Validating and transforming events with confidence |

### 2.2 Core User Stories

**US-1: Create Events with Human-Readable Labels**

As an application developer, I want to specify activity IDs using meaningful names so that I don't have to memorize numeric values.

```python
from ocsf.v1_7.events import IncidentFinding

# Clean, readable API
event = IncidentFinding(
    activity_id=IncidentFinding.ActivityId.CREATE,
    ...
)
```

**US-2: Use String Labels When Known**

As a security engineer, I want to construct enum values from string labels so that I can use values from configuration files or user input.

```python
from ocsf.v1_7.events import IncidentFinding

# String-based construction
event = IncidentFinding(
    severity_id=IncidentFinding.SeverityId("medium"),
    ...
)
```

**US-3: Get IDE Autocomplete for Valid Values**

As a developer, I want my IDE to show only the valid activity IDs for the specific event class I'm working with so that I can discover valid options without consulting documentation.

```python
from ocsf.v1_7.events import FileActivity

event = FileActivity(
    activity_id=FileActivity.ActivityId.  # IDE shows: CREATE, READ, UPDATE, DELETE, etc.
)
```

**US-4: Prevent Invalid Combinations**

As a data engineer, I want type checking to catch when I use an activity ID from the wrong event class so that I catch errors before runtime.

```python
from ocsf.v1_7.events import FileActivity, IncidentFinding

# Type checker error: IncidentFinding.ActivityId is not FileActivity.ActivityId
event = FileActivity(
    activity_id=IncidentFinding.ActivityId.CREATE  # Wrong enum type!
)
```

**US-5: Parse Events with Flexible Input**

As a data engineer, I want to parse events that may have only `foo_id` or only `foo` and have the other value extrapolated automatically.

```python
from ocsf.v1_7.events import FileActivity

# Only ID provided - label extrapolated
event1 = FileActivity.model_validate({"activity_id": 1, ...})
assert event1.activity == "Create"

# Only label provided - ID extrapolated  
event2 = FileActivity.model_validate({"activity": "Create", ...})
assert event2.activity_id == FileActivity.ActivityId.CREATE
```

**US-6: Handle Custom "Other" Values**

As a security engineer, I want to use custom activity labels when the standard enum values don't apply, mapping to `Other` (99) per OCSF specification.

```python
from ocsf.v1_7.events import FileActivity

# Custom label maps to Other (99)
event = FileActivity.model_validate({
    "activity": "Custom Scan Operation",
    ...
})
assert event.activity_id == 99
assert event.activity == "Custom Scan Operation"
```

**US-7: Validate Sibling Consistency**

As a data engineer, I want parsing to fail if both `foo_id` and `foo` are provided but don't match, so that I catch data quality issues.

```python
from ocsf.v1_7.events import FileActivity
from pydantic import ValidationError

# Mismatched siblings - should fail
try:
    event = FileActivity.model_validate({
        "activity_id": 1,      # CREATE
        "activity": "Delete",  # Doesn't match!
        ...
    })
except ValidationError as e:
    print("Caught mismatch:", e)
```

### 2.3 Requirements Summary

| ID | Requirement | Priority |
|----|-------------|----------|
| R1 | Generate context-specific enums as nested classes for all `_id` sibling pairs | Must Have |
| R2 | Support construction from numeric ID | Must Have |
| R3 | Support construction from string label (case-insensitive) | Must Have |
| R4 | Provide `.label` property for human-readable string | Must Have |
| R5 | Validate sibling consistency when both fields present | Must Have |
| R6 | Extrapolate missing sibling field during parsing | Must Have |
| R7 | Map unknown string labels to `Other` (99) | Must Have |
| R8 | Reject unknown numeric ID values | Must Have |
| R9 | Always serialize both `foo_id` and `foo` fields | Must Have |
| R10 | Use canonical label casing on output | Must Have |
| R11 | Generate comprehensive docstrings | Should Have |

---

## 3. Functional Specifications

### 3.1 Sibling Attribute Identification

OCSF sibling attributes follow the `_id` + base name pattern:

- A numeric field ending in `_id` (e.g., `activity_id`, `severity_id`, `status_id`)
- A corresponding string field with the same base name (e.g., `activity`, `severity`, `status`)
- The `_id` field has an associated enum definition in the OCSF schema
- Standard values include `0` for `Unknown` and `99` for `Other`

**Important Schema Note:**

In the OCSF schema source, only the `_id` field is explicitly defined. The sibling string field (e.g., `activity` for `activity_id`) must be **inferred** by the code generator—it is not listed as a separate field in the schema. During implementation, the generator must:

1. Identify fields ending in `_id` that have enum definitions
2. Derive the sibling field name by stripping the `_id` suffix (with special handling for `activity_id` → `activity_name`)
3. Generate both the enum and the sibling string field in the Pydantic model

This inference step should be validated during Phase 1 discovery by examining the actual OCSF schema structure.

**In-Scope Sibling Pairs:**

| ID Field | String Field | Description |
|----------|--------------|-------------|
| `activity_id` | `activity` | What action occurred |
| `severity_id` | `severity` | Event severity level |
| `status_id` | `status` | Outcome status |
| `type_id` | `type` | Object/event subtype |
| `disposition_id` | `disposition` | Finding disposition |
| `risk_level_id` | `risk_level` | Risk assessment level |

**Out of Scope:**

- `_uid` / `_name` pairs (e.g., `class_uid` / `class_name`) - these are classification attributes with fixed values per event class

**Special Case - activity_id:**

Per OCSF FAQ, `activity_id` uses `activity_name` as its sibling (not `activity`). The code generation must handle this naming exception.

### 3.2 Enum Structure

**Nested Class Pattern:**

```python
class FileActivity(BaseEvent):
    """File Activity events report when a process performs an action on a file."""
    
    class ActivityId(IntEnum):
        """Activity identifier for File Activity events."""
        UNKNOWN = 0
        CREATE = 1
        READ = 2
        UPDATE = 3
        DELETE = 4
        # ... more values
        OTHER = 99
        
        @property
        def label(self) -> str:
            """Return the canonical human-readable label."""
            ...
        
        @classmethod
        def from_label(cls, label: str) -> Self:
            """Create enum from string label (case-insensitive)."""
            ...
    
    class SeverityId(IntEnum):
        """Severity identifier for File Activity events."""
        UNKNOWN = 0
        INFORMATIONAL = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4
        CRITICAL = 5
        FATAL = 6
        OTHER = 99
        
        # ... same pattern
    
    # Fields using the nested enums
    activity_id: ActivityId
    activity: str | None = None
    severity_id: SeverityId
    severity: str | None = None
```

### 3.3 Construction Patterns

**From Enum Member (Primary):**

```python
activity_id = FileActivity.ActivityId.CREATE
```

**From Numeric Value:**

```python
activity_id = FileActivity.ActivityId(1)  # Returns CREATE
```

**From String Label (Case-Insensitive):**

```python
activity_id = FileActivity.ActivityId("Create")   # Returns CREATE
activity_id = FileActivity.ActivityId("create")   # Returns CREATE
activity_id = FileActivity.ActivityId("CREATE")   # Returns CREATE
```

**Unknown String (Maps to Other):**

```python
# Unknown labels map to OTHER (99)
activity_id = FileActivity.ActivityId("Custom Action")  # Returns OTHER
```

### 3.4 Validation Behavior

**Parsing Logic (model_validator):**

```python
@model_validator(mode='before')
@classmethod
def _reconcile_siblings(cls, data: dict) -> dict:
    """Reconcile sibling attribute pairs during parsing."""
    siblings = [
        ('activity_id', 'activity', cls.ActivityId),
        ('severity_id', 'severity', cls.SeverityId),
        # ... other pairs
    ]
    
    for id_field, label_field, enum_cls in siblings:
        id_val = data.get(id_field)
        label_val = data.get(label_field)
        
        has_id = id_val is not None
        has_label = label_val is not None
        
        if has_id and has_label:
            # Both present: validate consistency
            enum_val = enum_cls(id_val)  # Raises if invalid ID
            expected_label = enum_val.label
            
            # Special case: OTHER allows any label
            if enum_val != enum_cls.OTHER:
                if expected_label.lower() != str(label_val).lower():
                    raise ValueError(
                        f"{id_field}={id_val} ({expected_label}) "
                        f"does not match {label_field}={label_val!r}"
                    )
            # Use canonical label casing on output
            data[label_field] = label_val  # Preserve custom label for OTHER
            
        elif has_id:
            # Only ID: extrapolate label
            enum_val = enum_cls(id_val)  # Raises if invalid ID
            data[label_field] = enum_val.label
            
        elif has_label:
            # Only label: extrapolate ID
            try:
                enum_val = enum_cls.from_label(label_val)
                data[id_field] = enum_val.value
                data[label_field] = enum_val.label  # Canonical casing
            except ValueError:
                # Unknown label -> map to OTHER, preserve original label
                data[id_field] = enum_cls.OTHER.value
                # Keep original label as-is
    
    return data
```

**Validation Matrix:**

| `foo_id` | `foo` | Result |
|----------|-------|--------|
| Valid ID | Matching label | ✓ Both kept, label uses canonical casing |
| Valid ID | Mismatched label | ✗ `ValidationError` |
| Valid ID (OTHER=99) | Any label | ✓ Both kept, custom label preserved |
| Valid ID | Missing | ✓ Label extrapolated from enum |
| Missing | Known label | ✓ ID extrapolated from enum |
| Missing | Unknown label | ✓ ID=99 (OTHER), custom label preserved |
| Invalid ID | Any | ✗ `ValidationError` |
| Missing | Missing | ✓ if optional, ✗ if required |

### 3.5 Serialization Behavior

**Always Include Both Fields:**

```python
event = FileActivity(
    time=1706000000000,
    activity_id=FileActivity.ActivityId.CREATE,
    severity_id=FileActivity.SeverityId.HIGH,
    file=File(name="test.txt"),
)

print(event.model_dump_json(indent=2))
```

Output:
```json
{
  "time": 1706000000000,
  "class_uid": 1001,
  "category_uid": 1,
  "activity_id": 1,
  "activity": "Create",
  "severity_id": 4,
  "severity": "High",
  "file": {
    "name": "test.txt"
  }
}
```

**Custom Label with OTHER:**

```python
event = FileActivity.model_validate({
    "time": 1706000000000,
    "activity": "Custom Scan",  # Unknown -> OTHER
    "severity_id": 4,
    "file": {"name": "test.txt"},
})

print(event.model_dump())
# activity_id: 99, activity: "Custom Scan"
```

### 3.6 Error Messages

**Invalid Numeric ID:**

```python
FileActivity.ActivityId(999)
# ValueError: 999 is not a valid FileActivity.ActivityId
```

**Sibling Mismatch:**

```python
FileActivity.model_validate({
    "activity_id": 1,       # CREATE
    "activity": "Delete",   # Mismatch!
    ...
})
# ValidationError: activity_id=1 (Create) does not match activity='Delete'
```

---

## 4. Technical Specifications

### 4.1 Technology Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Enum Base | `IntEnum` subclass | Native integer behavior + enum features |
| String Lookup | Custom `__new__` + `from_label` | Elegant construction, handles OTHER case |
| Label Storage | Class attribute dict | Fast O(1) lookup |
| Code Generation | Jinja2 templates | Consistent with existing pipeline |
| Validation | Pydantic v2 `model_validator` | Native framework integration |

### 4.2 Enum Implementation

```python
from enum import IntEnum
from typing import Self, ClassVar

class SiblingEnum(IntEnum):
    """Base class for OCSF sibling enums with string label support."""
    
    _labels: ClassVar[dict[int, str]]
    
    @property
    def label(self) -> str:
        """Return the canonical human-readable label for this value."""
        return self._labels.get(self.value, str(self.value))
    
    @classmethod
    def from_label(cls, label: str) -> Self:
        """Create enum from string label (case-insensitive).
        
        Unknown labels raise ValueError (caller handles OTHER mapping).
        """
        normalized = label.lower()
        for value, lbl in cls._labels.items():
            if lbl.lower() == normalized:
                return cls(value)
        raise ValueError(f"Unknown {cls.__name__} label: {label!r}")
    
    def __new__(cls, value: int | str) -> Self:
        """Allow construction from int or string label.
        
        Unknown string labels map to OTHER (99).
        """
        if isinstance(value, str):
            try:
                return cls.from_label(value)
            except ValueError:
                # Unknown label -> return OTHER, let validator preserve label
                if hasattr(cls, 'OTHER'):
                    obj = int.__new__(cls, 99)
                    obj._value_ = 99
                    return obj
                raise
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj
```

### 4.3 Generated Nested Enum Example

```python
class FileActivity(BaseEvent):
    """File Activity events report when a process performs an action on a file.
    
    OCSF Class UID: 1001
    Category: System Activity
    
    See: https://schema.ocsf.io/1.7.0/classes/file_activity
    """
    
    class ActivityId(SiblingEnum):
        """Activity identifier for File Activity events.
        
        Indicates what file operation occurred.
        """
        UNKNOWN = 0
        CREATE = 1
        READ = 2
        UPDATE = 3
        DELETE = 4
        RENAME = 5
        SET_ATTRIBUTES = 6
        SET_SECURITY = 7
        GET_ATTRIBUTES = 8
        GET_SECURITY = 9
        ENCRYPT = 10
        DECRYPT = 11
        MOUNT = 12
        UNMOUNT = 13
        OPEN = 14
        OTHER = 99
        
        _labels: ClassVar[dict[int, str]] = {
            0: "Unknown",
            1: "Create",
            2: "Read",
            3: "Update",
            4: "Delete",
            5: "Rename",
            6: "Set Attributes",
            7: "Set Security",
            8: "Get Attributes",
            9: "Get Security",
            10: "Encrypt",
            11: "Decrypt",
            12: "Mount",
            13: "Unmount",
            14: "Open",
            99: "Other",
        }
    
    class SeverityId(SiblingEnum):
        """Severity identifier for File Activity events."""
        UNKNOWN = 0
        INFORMATIONAL = 1
        LOW = 2
        MEDIUM = 3
        HIGH = 4
        CRITICAL = 5
        FATAL = 6
        OTHER = 99
        
        _labels: ClassVar[dict[int, str]] = {
            0: "Unknown",
            1: "Informational",
            2: "Low",
            3: "Medium",
            4: "High",
            5: "Critical",
            6: "Fatal",
            99: "Other",
        }
    
    # Model fields
    activity_id: ActivityId = Field(..., description="The activity type identifier.")
    activity: str = Field(..., description="The activity name.")
    severity_id: SeverityId = Field(..., description="The severity identifier.")
    severity: str = Field(..., description="The severity level.")
    
    @model_validator(mode='before')
    @classmethod
    def _reconcile_siblings(cls, data: dict) -> dict:
        """Reconcile sibling attribute pairs during parsing."""
        # Implementation as specified in 3.4
        ...
```

### 4.4 Code Generation Templates

**Template Structure:**

```
templates/
├── sibling_enum.py.jinja2      # Nested enum class template
├── sibling_validator.py.jinja2 # Pydantic validator template
└── event_class.py.jinja2       # Updated to include nested enums
```

**Enum Template (`sibling_enum.py.jinja2`):**

```jinja2
class {{ enum_name }}(SiblingEnum):
    """{{ description }}
    
    OCSF Attribute: {{ attribute_name }}
    """
{% for member in members %}
    {{ member.name }} = {{ member.value }}
{% endfor %}
    
    _labels: ClassVar[dict[int, str]] = {
{% for member in members %}
        {{ member.value }}: "{{ member.label }}",
{% endfor %}
    }
```

### 4.5 Package Structure

```
ocsf/
├── __init__.py
├── _sibling_enum.py            # SiblingEnum base class
├── v1_7/
│   ├── __init__.py
│   ├── events/
│   │   ├── __init__.py
│   │   ├── base.py             # BaseEvent with common enums
│   │   ├── file_activity.py    # FileActivity with nested ActivityId, SeverityId, etc.
│   │   ├── process_activity.py
│   │   └── ...
│   └── objects/
│       └── ...
```

### 4.6 Import Pattern

```python
# Primary usage - everything from event class
from ocsf.v1_7.events import FileActivity

event = FileActivity(
    time=1706000000000,
    activity_id=FileActivity.ActivityId.CREATE,
    severity_id=FileActivity.SeverityId.HIGH,
    file={"name": "test.txt"},
)

# Type hints use the nested class
def process_file_event(
    activity: FileActivity.ActivityId,
    severity: FileActivity.SeverityId,
) -> None:
    ...
```

### 4.7 Memory and Performance

| Aspect | Approach | Impact |
|--------|----------|--------|
| Enum class size | Standard IntEnum + labels dict | ~500 bytes per enum class |
| Label lookup (by ID) | Dict lookup O(1) | <1μs |
| Label lookup (by string) | Linear scan | <10μs for typical sizes |
| Sibling validation | Single pass in validator | <50μs per event |
| Import time | Nested classes loaded with event | Minimal additional overhead |

---

## 5. API Design and Developer Experience

### 5.1 Design Principles

1. **Intuitive**: `FileActivity.ActivityId.CREATE` reads naturally
2. **Discoverable**: IDE autocomplete shows valid options for each event class
3. **Forgiving**: Case-insensitive input, strict output
4. **Safe**: Type checking catches wrong enum usage
5. **Complete**: Always outputs both ID and label

### 5.2 Usage Examples

**Creating an Event (Enum):**

```python
from ocsf.v1_7.events import FileActivity

event = FileActivity(
    time=1706000000000,
    activity_id=FileActivity.ActivityId.CREATE,
    severity_id=FileActivity.SeverityId.HIGH,
    file={"name": "document.pdf", "path": "/home/user/document.pdf"},
)
```

**Creating an Event (String Labels):**

```python
event = FileActivity(
    time=1706000000000,
    activity_id=FileActivity.ActivityId("create"),  # case-insensitive
    severity_id=FileActivity.SeverityId("high"),
    file={"name": "document.pdf"},
)
```

**Parsing JSON:**

```python
import json
from ocsf.v1_7.events import FileActivity

raw = '{"time": 1706000000000, "activity_id": 1, "severity_id": 4, "file": {"name": "test.txt"}}'
event = FileActivity.model_validate_json(raw)

print(event.activity_id)      # FileActivity.ActivityId.CREATE
print(event.activity)         # "Create" (extrapolated)
print(event.severity_id)      # FileActivity.SeverityId.HIGH  
print(event.severity)         # "High" (extrapolated)
```

**Handling Custom Activities:**

```python
# Input with unknown activity label
data = {
    "time": 1706000000000,
    "activity": "Quarantine File",  # Not a standard activity
    "severity_id": 4,
    "file": {"name": "malware.exe"},
}

event = FileActivity.model_validate(data)
print(event.activity_id)  # 99 (OTHER)
print(event.activity)     # "Quarantine File" (preserved)
```

**Type-Safe Function Signatures:**

```python
from ocsf.v1_7.events import FileActivity, ProcessActivity

def handle_file_activity(activity: FileActivity.ActivityId) -> str:
    match activity:
        case FileActivity.ActivityId.CREATE:
            return "File created"
        case FileActivity.ActivityId.DELETE:
            return "File deleted"
        case _:
            return f"Other activity: {activity.label}"

# Type error: ProcessActivity.ActivityId is not FileActivity.ActivityId
handle_file_activity(ProcessActivity.ActivityId.LAUNCH)  # ← IDE/mypy catches this
```

---

## 6. Performance Metrics and Success Criteria

### 6.1 Performance Targets

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Enum construction (from int) | <1μs | pytest-benchmark |
| Enum construction (from string) | <10μs | pytest-benchmark |
| Sibling reconciliation | <50μs per event | pytest-benchmark |
| Event creation with enums | <10% overhead vs raw int | Comparative benchmark |
| Overall validation throughput | ≥10,000 events/second | Throughput benchmark |

### 6.2 Quality Metrics

| Metric | Target |
|--------|--------|
| Sibling pair coverage | 100% of `_id` patterns in OCSF |
| Enum value accuracy | 100% match to OCSF schema |
| Label accuracy | 100% match to OCSF captions |
| Test coverage | ≥90% line coverage |
| Type coverage | 100% public API typed |

### 6.3 Success Criteria

| Criterion | Measure |
|-----------|---------|
| API usability | `EventClass.EnumName.MEMBER` pattern works |
| IDE support | Autocomplete shows nested enum members in VS Code, PyCharm |
| Type safety | mypy catches cross-event-class enum misuse |
| Parsing flexibility | Events parse with only ID or only label |
| OCSF compliance | OTHER (99) handling matches spec |
| Output completeness | Both ID and label always serialized |

---

## 7. Implementation Plan

### 7.1 Phase 1: Foundation (Days 1-2)

**Objectives:**

- Implement `SiblingEnum` base class
- Design schema parser for sibling detection
- Identify all `_id` sibling pairs in OCSF 1.7.0
- **Validate sibling inference approach against actual schema structure**

**Deliverables:**

- `ocsf/_sibling_enum.py` with base class
- Schema analysis documenting all sibling pairs
- **Documentation of schema structure confirming sibling fields are inferred (not explicit)**
- Unit tests for `SiblingEnum` behavior

**Discovery Tasks:**

- Examine OCSF schema JSON to confirm that sibling string fields are not explicitly defined
- Document the exact inference rules needed (e.g., `foo_id` → `foo`, `activity_id` → `activity_name`)
- Identify any edge cases or exceptions to the standard pattern

### 7.2 Phase 2: Code Generation (Days 3-5)

**Objectives:**

- Create Jinja2 templates for nested enums
- Update event class templates to include nested enums
- Generate all enums for OCSF 1.7.0

**Deliverables:**

- `sibling_enum.py.jinja2` template
- Updated `event_class.py.jinja2` template
- Generated event classes with nested enums

### 7.3 Phase 3: Validation Integration (Days 6-7)

**Objectives:**

- Implement sibling reconciliation validator
- Handle OTHER (99) case correctly
- Ensure serialization includes both fields

**Deliverables:**

- Validator template/implementation
- Integration tests for all validation scenarios
- Serialization tests

### 7.4 Phase 4: Testing and Documentation (Days 8-10)

**Objectives:**

- Comprehensive testing of all generated enums
- Update documentation with new API
- Performance validation

**Deliverables:**

- Full test suite for enum fidelity
- Updated README with nested enum examples
- Performance benchmark results
- Release preparation

### 7.5 Task Breakdown

| Day | Tasks |
|-----|-------|
| 1 | Implement SiblingEnum base class with tests; **examine OCSF schema to validate sibling inference assumptions** |
| 2 | Schema analysis: identify all _id sibling pairs, handle activity_name special case, **document inference rules** |
| 3 | Create nested enum Jinja2 template |
| 4 | Update event class template to include nested enums and inferred sibling fields |
| 5 | Generate all enums, verify completeness |
| 6 | Implement sibling reconciliation validator |
| 7 | Handle OTHER case, serialization behavior |
| 8 | Write fidelity tests, validation scenario tests |
| 9 | Documentation, usage examples |
| 10 | Performance testing, release prep |

---

## 8. Risks and Mitigation Strategies

### 8.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Nested class + IntEnum interaction issues | Medium | High | Prototype early, test with mypy/pyright |
| activity_id/activity_name special case | Low | Medium | Explicit handling in generator |
| Performance overhead from validation | Low | Medium | Early benchmarking, optimize hot paths |
| Circular import with nested classes | Low | Medium | Careful module structure |
| Sibling inference assumptions incorrect | Medium | High | Validate against schema in Phase 1 discovery before building generator |

### 8.2 Compatibility Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Type checker compatibility | Medium | Medium | Test with mypy and pyright |
| Pydantic nested class serialization | Low | High | Test early, use model_serializer if needed |
| IDE autocomplete for nested classes | Low | Medium | Test in VS Code and PyCharm |

### 8.3 OCSF Schema Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Schema updates change enum values | Medium | Low | Regeneration on update |
| New sibling patterns in future versions | Low | Medium | Extensible generator design |
| Inconsistent OTHER (99) usage | Low | Low | Default to spec behavior |

---

## 9. Testing and Quality Assurance

### 9.1 Test Categories

**SiblingEnum Base Class Tests:**

```python
def test_construction_from_int():
    assert FileActivity.ActivityId(1) == FileActivity.ActivityId.CREATE

def test_construction_from_string():
    assert FileActivity.ActivityId("Create") == FileActivity.ActivityId.CREATE

def test_construction_case_insensitive():
    assert FileActivity.ActivityId("create") == FileActivity.ActivityId.CREATE
    assert FileActivity.ActivityId("CREATE") == FileActivity.ActivityId.CREATE

def test_unknown_string_returns_other():
    result = FileActivity.ActivityId("Custom Action")
    assert result == FileActivity.ActivityId.OTHER

def test_invalid_int_raises():
    with pytest.raises(ValueError):
        FileActivity.ActivityId(9999)

def test_label_property():
    assert FileActivity.ActivityId.CREATE.label == "Create"
```

**Sibling Reconciliation Tests:**

```python
def test_both_present_matching():
    event = FileActivity.model_validate({
        "time": 1706000000000,
        "activity_id": 1,
        "activity": "Create",
        "severity_id": 1,
        "file": {"name": "test.txt"},
    })
    assert event.activity_id == FileActivity.ActivityId.CREATE
    assert event.activity == "Create"

def test_both_present_mismatched_raises():
    with pytest.raises(ValidationError) as exc:
        FileActivity.model_validate({
            "time": 1706000000000,
            "activity_id": 1,
            "activity": "Delete",
            "severity_id": 1,
            "file": {"name": "test.txt"},
        })
    assert "does not match" in str(exc.value)

def test_only_id_extrapolates_label():
    event = FileActivity.model_validate({
        "time": 1706000000000,
        "activity_id": 1,
        "severity_id": 1,
        "file": {"name": "test.txt"},
    })
    assert event.activity == "Create"

def test_only_label_extrapolates_id():
    event = FileActivity.model_validate({
        "time": 1706000000000,
        "activity": "Create",
        "severity_id": 1,
        "file": {"name": "test.txt"},
    })
    assert event.activity_id == FileActivity.ActivityId.CREATE

def test_unknown_label_maps_to_other():
    event = FileActivity.model_validate({
        "time": 1706000000000,
        "activity": "Custom Scan",
        "severity_id": 1,
        "file": {"name": "test.txt"},
    })
    assert event.activity_id == 99
    assert event.activity == "Custom Scan"

def test_other_with_custom_label_preserved():
    event = FileActivity.model_validate({
        "time": 1706000000000,
        "activity_id": 99,
        "activity": "My Custom Activity",
        "severity_id": 1,
        "file": {"name": "test.txt"},
    })
    assert event.activity_id == 99
    assert event.activity == "My Custom Activity"
```

**Serialization Tests:**

```python
def test_serialization_includes_both_fields():
    event = FileActivity(
        time=1706000000000,
        activity_id=FileActivity.ActivityId.CREATE,
        severity_id=FileActivity.SeverityId.HIGH,
        file={"name": "test.txt"},
    )
    data = event.model_dump()
    assert data["activity_id"] == 1
    assert data["activity"] == "Create"
    assert isinstance(data["activity_id"], int)

def test_json_roundtrip():
    original = FileActivity(
        time=1706000000000,
        activity_id=FileActivity.ActivityId.CREATE,
        severity_id=FileActivity.SeverityId.HIGH,
        file={"name": "test.txt"},
    )
    json_str = original.model_dump_json()
    restored = FileActivity.model_validate_json(json_str)
    assert restored.activity_id == original.activity_id
    assert restored.activity == original.activity
```

**Type Checking Tests:**

```python
# tests/test_types.py - run with mypy
from ocsf.v1_7.events import FileActivity, ProcessActivity

def test_correct_enum_type() -> None:
    # Should pass type checking
    activity: FileActivity.ActivityId = FileActivity.ActivityId.CREATE
    
def test_wrong_enum_type() -> None:
    # Should fail type checking (verified manually or with mypy plugin)
    activity: FileActivity.ActivityId = ProcessActivity.ActivityId.LAUNCH  # type: ignore
```

### 9.2 Quality Gates

No release without:

- 100% of `_id` sibling pairs have corresponding nested enums
- All enum values match schema exactly
- All construction patterns work (int, string, enum member)
- Sibling reconciliation works for all scenarios
- OTHER (99) handling matches OCSF spec
- Serialization always includes both fields
- No type errors in strict mode
- Performance within targets

---

## 10. Maintenance and Future Considerations

### 10.1 OCSF Version Update Process

When OCSF releases a new version:

1. Fetch updated schema
2. Run sibling detection to identify new/changed pairs
3. Regenerate nested enums with updated values
4. Run fidelity tests to verify correctness
5. Update documentation if enum members changed
6. Release new library version

### 10.2 Handling Schema Changes

| Change Type | Impact | Handling |
|-------------|--------|----------|
| New enum value added | Low | Regenerate, non-breaking |
| Enum value removed | Medium | Regenerate, document in changelog |
| Label text changed | Low | Regenerate, case-insensitive lookup handles most cases |
| New sibling pair added | Low | Generator picks up automatically |

### 10.3 Future Enhancements

**Out of Scope for v1.0:**

- `_uid`/`_name` sibling handling
- Custom enum values beyond OTHER
- Enum value deprecation warnings
- CLI tools for enum lookup

**Potential Future Work:**

- Support for extension-defined enum values
- Warnings for deprecated enum values
- Generated documentation for all enums
- Enum migration utilities between OCSF versions

---

## 11. Appendix

### 11.1 Glossary

| Term | Definition |
|------|------------|
| Sibling Attributes | OCSF pattern pairing a `_id` numeric field with a corresponding string label field |
| Nested Enum | Enum class defined inside an event class for context-specific values |
| OTHER | Standard OCSF enum value (99) used when no standard value applies, allowing custom labels |
| Canonical Label | The official OCSF label text with correct casing |

### 11.2 OCSF FAQ Reference

From the OCSF FAQ on sibling attributes:

> `_id` is the convention for OCSF enumerated attributes. These attributes can be integer data types, or string data types, although OCSF favors integer data types with string labels. Every integer enum attribute SHOULD have standard values of `0` for `Unknown` and `99` for `Other`. Every enum attribute SHOULD have a string sibling attribute of the same name but without the `_id` suffix. When the logged value is not mappable within the enum listed values, `Other` can be set and a source specific label can populate the sibling attribute.

### 11.3 Complete Validation Truth Table

| `foo_id` Input | `foo` Input | Valid? | `foo_id` Output | `foo` Output |
|----------------|-------------|--------|-----------------|--------------|
| 1 | "Create" | ✓ | 1 | "Create" |
| 1 | "create" | ✓ | 1 | "Create" |
| 1 | "Delete" | ✗ | - | - |
| 1 | None | ✓ | 1 | "Create" |
| 99 | "Custom" | ✓ | 99 | "Custom" |
| 99 | None | ✓ | 99 | "Other" |
| None | "Create" | ✓ | 1 | "Create" |
| None | "Custom" | ✓ | 99 | "Custom" |
| 999 | Any | ✗ | - | - |
| None | None | * | - | - |

\* Depends on whether field is required

---

**Document Status:** Approved for Implementation

**Next Steps:**

1. Begin Phase 1: Implement SiblingEnum base class
2. Analyze OCSF schema for all sibling pairs
3. Prototype nested enum generation with FileActivity
