# Using OCSF Pydantic Models

This document describes how to use the generated OCSF (Open Cybersecurity Schema Framework) Pydantic models for working with cybersecurity event data.

## Overview

The `ocsf` package provides type-safe Pydantic models for all OCSF schema versions. These models enable:

- **Type Safety**: Full IDE autocomplete and type checking for all OCSF fields
- **Validation**: Automatic validation of event data against the OCSF schema
- **Serialization**: Easy conversion between Python objects and JSON
- **Forward Compatibility**: Support for unmapped/custom fields via Pydantic's extra fields

## Installation

```bash
pip install pydantic-ocsf
```

## Important: Namespace Organization

**As of v2.0.0**, OCSF models are organized into namespaces to avoid name collisions:

```python
# Import objects from the objects namespace
from ocsf.v1_7_0.objects import User, Account, File, Process

# Import events from the events namespace
from ocsf.v1_7_0.events import FileActivity, ApiActivity

# Old style NO LONGER WORKS:
# from ocsf.v1_7_0 import User, FileActivity  # ❌ Raises AttributeError
```

## Quick Start

### Creating OCSF Events

```python
from ocsf.v1_7_0.events import ApiActivity
from ocsf.v1_7_0.objects import Actor, Api, Metadata, Product

# Create an API activity event
event = ApiActivity(
    actor=Actor(
        user={'name': 'alice@example.com', 'uid': 'user-123'}
    ),
    api=Api(
        operation='CreateBucket',
        service={'name': 'S3'}
    ),
    metadata=Metadata(
        version='1.7.0',
        product=Product(name='AWS CloudTrail')
    )
)

# Serialize to JSON
json_str = event.model_dump_json()

# Deserialize from JSON
restored = ApiActivity.model_validate_json(json_str)
```

### Working with Objects

```python
from ocsf.v1_7_0.objects import File, Process, User

# Create file object
file = File(
    name='malware.exe',
    path='/tmp/malware.exe',
    type_id=1,
    size=1024
)

# Create process object
process = Process(
    name='cmd.exe',
    pid=1234,
    file=file,
    user=User(name='admin')
)

# Access nested fields with full type safety
print(f"Process {process.name} is running {process.file.name}")
```

### Using Enums

```python
from ocsf.v1_7_0.events import ApiActivity

# Enums are attached to their respective models
event = ApiActivity(
    activity_id=ApiActivity.ActivityId.CREATE,
    severity_id=ApiActivity.SeverityId.INFORMATIONAL,
    status_id=ApiActivity.StatusId.SUCCESS,
    # ... other fields
)

# Enums serialize as integers
data = event.model_dump()
assert isinstance(data['activity_id'], int)
```

### Handling Name Collisions

Some names exist in both objects and events namespaces. Use aliases to differentiate:

```python
from ocsf.v1_7_0.objects import Finding as FindingObject
from ocsf.v1_7_0.events import Finding as FindingEvent
from ocsf.v1_7_0.objects import Application as AppObject
from ocsf.v1_7_0.events import Application as AppEvent

# These are different classes with different fields
finding_obj = FindingObject(title="Security Issue", uid="finding-123")
finding_evt = FindingEvent(class_uid=2004, category_uid=2, ...)
```

## Type System

### Forward References and TYPE_CHECKING

The generated models use Python's `TYPE_CHECKING` pattern to handle circular dependencies:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ocsf.v1_7_0.objects.user import User
```

This means:
- Type annotations are strings at runtime (via `from __future__ import annotations`)
- Circular imports are avoided (imports only happen during type checking)
- Models are automatically rebuilt after all imports complete

**You don't need to do anything special** - just import and use the models normally!

### Optional vs Required Fields

```python
# Required fields use ellipsis (...)
class_uid: Literal[3] = Field(...)

# Optional fields use None as default
status_id: StatusId | None = Field(default=None)
```

### Union Types (Python 3.10+ Syntax)

```python
# Modern union syntax
user: User | None = Field(default=None)

# List of objects
observables: list[Observable] | None = Field(default=None)
```

## Working with Data

### Loading from Dictionary

```python
data = {
    'class_uid': 3,
    'category_uid': 6,
    'actor': {
        'user': {'name': 'alice'}
    },
    'api': {
        'operation': 'ListBuckets'
    },
    'metadata': {
        'version': '1.7.0',
        'product': {'name': 'CloudTrail'}
    }
}

event = ApiActivity.model_validate(data)
```

### Handling Extra Fields

OCSF models preserve unmapped fields:

```python
data = {
    'class_uid': 3,
    'actor': {...},
    'api': {...},
    'metadata': {...},
    'custom_field': 'custom_value',  # Not in schema
    'internal_id': 12345              # Also not in schema
}

event = ApiActivity.model_validate(data)
dumped = event.model_dump()

assert dumped['custom_field'] == 'custom_value'
assert dumped['internal_id'] == 12345
```

### Excluding None Values

```python
# Create event with many optional fields
event = ApiActivity(
    actor=Actor(user={'name': 'alice'}),
    api=Api(operation='Read'),
    metadata=Metadata(version='1.7.0', product=Product(name='Test'))
)

# Exclude None values from output
data = event.model_dump(exclude_none=True)
# Only fields with actual values are included
```

## Version Support

The package includes multiple OCSF versions (v1.0.0 through v1.7.0):

```python
# Use specific version with namespaces
from ocsf.v1_7_0.events import ApiActivity as ApiActivity_v1_7_0
from ocsf.v1_3_0.events import ApiActivity as ApiActivity_v1_3_0

# Access namespace modules from top-level
from ocsf import objects, events

user = objects.User(name="Alice", uid="123")  # Uses latest v1.7.0
activity = events.FileActivity(...)  # Uses latest v1.7.0
```

## Advanced Usage

### Custom Validation

```python
from pydantic import field_validator

class MyApiActivity(ApiActivity):
    @field_validator('api')
    def validate_api_operation(cls, v):
        if v.operation not in ['Read', 'Write', 'Delete']:
            raise ValueError('Invalid operation')
        return v
```

### Model Configuration

```python
# Export with specific settings
json_str = event.model_dump_json(
    exclude_none=True,
    by_alias=True,
    indent=2
)
```

### Working with Metadata

All OCSF events have class and category identifiers:

```python
event = ApiActivity(...)

print(f"Class UID: {event.class_uid}")      # Always 3 for ApiActivity
print(f"Category UID: {event.category_uid}")  # Category identifier
```

## Common Patterns

### Creating Events from Log Data

```python
def parse_cloudtrail_event(log_entry: dict) -> ApiActivity:
    """Convert CloudTrail log to OCSF ApiActivity."""
    return ApiActivity(
        time=log_entry['eventTime'],
        actor=Actor(
            user={
                'name': log_entry['userIdentity']['userName'],
                'uid': log_entry['userIdentity']['arn']
            }
        ),
        api=Api(
            operation=log_entry['eventName'],
            service={'name': log_entry['eventSource']}
        ),
        metadata=Metadata(
            version='1.7.0',
            product=Product(
                name='AWS CloudTrail',
                vendor_name='Amazon'
            )
        )
    )
```

### Batch Processing

```python
from ocsf.v1_7_0.events import ApiActivity

def process_events(json_logs: list[str]) -> list[ApiActivity]:
    """Parse and validate multiple events."""
    events = []
    for log in json_logs:
        try:
            event = ApiActivity.model_validate_json(log)
            events.append(event)
        except ValidationError as e:
            print(f"Invalid event: {e}")
    return events
```

### Type-Safe Event Processing

```python
from typing import TypeGuard
from ocsf.v1_7_0.events import ApiActivity, Authentication

def is_api_activity(event: object) -> TypeGuard[ApiActivity]:
    """Type guard for API activity events."""
    return isinstance(event, ApiActivity)

def process_event(event: ApiActivity | Authentication) -> None:
    """Process events with type safety."""
    if is_api_activity(event):
        # IDE knows event is ApiActivity here
        print(f"API operation: {event.api.operation}")
    else:
        # IDE knows event is Authentication here
        print(f"Auth method: {event.auth_protocol}")
```

## Troubleshooting

### Import Errors

If you encounter import errors, ensure all imports complete before using the models:

```python
# Good: Import at module level
from ocsf.v1_7_0.events import ApiActivity
from ocsf.v1_7_0.objects import Actor, Api

def create_event():
    return ApiActivity(...)
```

```python
# Avoid: Lazy imports can cause issues
def create_event():
    from ocsf.v1_7_0.events import ApiActivity  # May not be rebuilt yet
    return ApiActivity(...)
```

### Type Resolution Errors

If you see "Type is not fully defined" errors:
1. Ensure you're importing from the version-level package: `from ocsf.v1_7_0 import ...`
2. The models auto-rebuild on import, so this should be automatic
3. If issues persist, file a bug report

### Performance Considerations

- **First Import**: The initial import rebuilds ~500 models, taking 1-2 seconds
- **Subsequent Imports**: Cached after first import
- **Memory**: Each version's models consume ~50MB RAM
- **Tip**: Import only the models you need: `from ocsf.v1_7_0.events import ApiActivity`

## Best Practices

1. **Use Type Hints**: Leverage the type system for better IDE support
   ```python
   def process_event(event: ApiActivity) -> dict:
       ...
   ```

2. **Validate Early**: Use `model_validate()` at system boundaries
   ```python
   event = ApiActivity.model_validate(untrusted_data)
   ```

3. **Handle Validation Errors**: Always catch `ValidationError`
   ```python
   from pydantic import ValidationError

   try:
       event = ApiActivity.model_validate(data)
   except ValidationError as e:
       print(f"Invalid data: {e}")
   ```

4. **Version Pin**: Pin to specific OCSF versions in production
   ```python
   from ocsf.v1_7_0.events import ApiActivity  # Explicit version
   ```

5. **Preserve Unknown Fields**: The models automatically preserve extra fields, so your custom extensions are safe

## Resources

- **OCSF Schema Documentation**: https://schema.ocsf.io/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **Project Repository**: https://github.com/yourusername/pydantic-ocsf
- **Issue Tracker**: https://github.com/yourusername/pydantic-ocsf/issues

## Examples Repository

See the `examples/` directory for complete working examples:
- AWS CloudTrail event parsing
- Okta authentication logs
- Network flow data
- File activity monitoring
- Custom event extensions
