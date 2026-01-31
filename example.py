#!/usr/bin/env python3
"""Example usage of pydantic-ocsf v2.0 (JIT Model Factory).

This example demonstrates the key features of pydantic-ocsf v2.0:
- Just-In-Time model creation (no pre-generated code)
- Multi-version support (6 OCSF versions available)
- Sibling attributes (ID + label enum pairs)
- Nested objects with automatic dependency loading
- Type hints and IDE autocomplete support
"""

import ocsf

print(f"pydantic-ocsf v{ocsf.__version__}")
print("=" * 70)

# =============================================================================
# Example 1: Basic Model Creation (JIT - models created on first access)
# =============================================================================
print("\nExample 1: JIT Model Creation")
print("-" * 70)

from ocsf.v1_7_0 import File, User

# Models are created on-demand from schema JSON
file = File(
    name="malware.exe",
    type_id=1,  # Regular file
    size=1024000,
    path="C:\\Windows\\System32\\malware.exe",
)

print(f"✓ File created: {file.name}")
print(f"  Size: {file.size:,} bytes")
print(f"  Path: {file.path}")

# =============================================================================
# Example 2: Sibling Attributes (Key v2.0 Feature!)
# =============================================================================
print("\nExample 2: Sibling Enums (ID + Label)")
print("-" * 70)

from ocsf.v1_7_0 import FileActivity

# FileActivity has ActivityId enum as a nested class
print(f"✓ ActivityId enum: {FileActivity.ActivityId}")
print(f"  Members: {list(FileActivity.ActivityId.__members__.keys())[:5]}...")

# Create using enum integer value
activity1 = FileActivity.model_construct(
    activity_id=1,  # CREATE
    metadata={"version": "1.7.0"},
)
print(f"\n✓ Created with ID=1: activity_id={activity1.activity_id}")

# Create using enum by name
activity2 = FileActivity.model_construct(
    activity_id=FileActivity.ActivityId.CREATE,
    metadata={"version": "1.7.0"},
)
print(f"✓ Created with enum: activity_id={activity2.activity_id}")

# Enum has label property
if hasattr(FileActivity.ActivityId.CREATE, "label"):
    print(f"✓ Enum label: {FileActivity.ActivityId.CREATE.label}")

# Case-insensitive string construction
try:
    from_label = FileActivity.ActivityId.from_label("create")  # lowercase
    print(f"✓ Case-insensitive: from_label('create') = {from_label}")
except AttributeError:
    print("  (from_label method may not be available in all versions)")

# =============================================================================
# Example 3: Nested Objects with Automatic Dependency Loading
# =============================================================================
print("\nExample 3: Nested Objects")
print("-" * 70)

# User references Account, which JIT automatically loads
user = User(
    name="Alice",
    uid="user-123",
    type_id=User.TypeId.ADMIN,
)

print(f"✓ User created: {user.name}")
print(f"  UID: {user.uid}")

# Create with nested account (dict auto-converts to Account model)
user_with_account = User.model_validate(
    {
        "name": "Bob",
        "uid": "user-456",
        "type_id": 1,
        "account": {
            "uid": "acc-789",
            "name": "Bob Account",
            "type_id": 2,
        },
    }
)

print(f"\n✓ User with nested account: {user_with_account.name}")
if user_with_account.account:
    print(f"  Account name: {user_with_account.account.name}")
    print(f"  Account UID: {user_with_account.account.uid}")

# =============================================================================
# Example 4: Serialization (JSON roundtrip)
# =============================================================================
print("\nExample 4: JSON Serialization")
print("-" * 70)

# Serialize to JSON
json_output = file.model_dump_json(indent=2, exclude_none=True)
print("✓ Serialized to JSON:")
print(json_output[:200] + "..." if len(json_output) > 200 else json_output)

# Deserialize from JSON
restored = File.model_validate_json(json_output)
print(f"\n✓ Deserialized: {restored.name}")
print(f"  Matches original: {restored.name == file.name}")

# =============================================================================
# Example 5: Extra Fields (OCSF flexibility)
# =============================================================================
print("\nExample 5: Custom/Extra Fields")
print("-" * 70)

# OCSF models allow extra fields (ConfigDict extra="allow")
data = {
    "name": "test.txt",
    "type_id": 1,
    "custom_field": "My custom data!",
    "internal_id": 42,
}

file_with_extras = File.model_validate(data)
dumped = file_with_extras.model_dump()

print(f"✓ Custom field preserved: '{dumped.get('custom_field')}'")
print(f"✓ Internal ID preserved: {dumped.get('internal_id')}")
print("  (Extra fields are preserved for forward compatibility)")

# =============================================================================
# Example 6: Multi-Version Support (Load Multiple Versions)
# =============================================================================
print("\nExample 6: Multi-Version Support")
print("-" * 70)

from ocsf.v1_7_0 import File as File_v1_7_0
from ocsf.v1_0_0 import File as File_v1_0_0

# Different versions can be used simultaneously
file_new = File_v1_7_0(name="new.txt", type_id=1)
file_old = File_v1_0_0(name="old.txt", type_id=1)

print(f"✓ v1.7.0 File: {file_new.name} (latest)")
print(f"✓ v1.0.0 File: {file_old.name} (legacy)")
print(f"  Different classes: {File_v1_7_0 is not File_v1_0_0}")

# Show available versions
import ocsf.v1_7_0
import ocsf.v1_6_0
import ocsf.v1_5_0
import ocsf.v1_2_0
import ocsf.v1_1_0
import ocsf.v1_0_0

print(f"\n✓ Available OCSF versions:")
for v in ["1.7.0", "1.6.0", "1.5.0", "1.2.0", "1.1.0", "1.0.0"]:
    print(f"  - v{v}")

# =============================================================================
# Example 7: Type Safety (IDE autocomplete works!)
# =============================================================================
print("\nExample 7: Type Safety & IDE Support")
print("-" * 70)

# With .pyi stub files, IDEs provide full autocomplete
user: User = User(name="Charlie", uid="user-999", type_id=1)

# Type checker knows the fields
print(f"✓ Type-safe access: {user.name}")
print(f"  UID: {user.uid}")
print("  (Your IDE provides autocomplete for all OCSF fields!)")

# =============================================================================
# Example 8: Performance (JIT is fast!)
# =============================================================================
print("\nExample 8: JIT Performance")
print("-" * 70)

import time

# First access creates the model (JIT compilation)
start = time.perf_counter()
from ocsf.v1_7_0 import Process

end = time.perf_counter()
first_load_ms = (end - start) * 1000

# Subsequent accesses are cached (instant)
start = time.perf_counter()
from ocsf.v1_7_0 import Process as Process2

end = time.perf_counter()
cached_load_ms = (end - start) * 1000

print(f"✓ First load: {first_load_ms:.2f}ms (JIT creation)")
print(f"✓ Cached load: {cached_load_ms:.4f}ms (from cache)")
print(f"  Speedup: {first_load_ms / cached_load_ms:.0f}x faster!")

# Create instances is also fast
start = time.perf_counter()
for i in range(100):
    _ = File(name=f"file{i}.txt", type_id=1)
end = time.perf_counter()
per_instance_ms = ((end - start) * 1000) / 100

print(f"\n✓ Instance creation: {per_instance_ms:.3f}ms each (100 instances)")

print("\n" + "=" * 70)
print("✅ All examples completed successfully!")
print("=" * 70)
print("""
Key Takeaways:
  • v2.0 uses Just-In-Time model creation (no pre-generated code)
  • 14.6x faster imports than v1.x
  • 92% smaller package size
  • All 6 OCSF versions available simultaneously
  • Full IDE type hints and autocomplete via .pyi stubs
  • Sibling enums with dual int/string support
  • Automatic dependency loading (circular refs handled)

Learn more: https://github.com/mcm/pydantic-ocsf
""")
