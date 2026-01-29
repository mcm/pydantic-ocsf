#!/usr/bin/env python3
"""Example usage of pydantic-ocsf library."""

# Import from latest version (v1.7.0) via top-level imports
from ocsf import File, StatusId, __version__

print(f"pydantic-ocsf v{__version__}\n")

# Example 1: Create a File object
print("Example 1: Creating a File object")
print("-" * 50)
file = File(
    name="malware.exe",
    type_id=1,  # Regular file
    size=1024000,
    path="C:\\Windows\\System32\\malware.exe",
)

print(f"File name: {file.name}")
print(f"File size: {file.size} bytes")
print(f"File path: {file.path}")

# Example 2: Serialize to JSON
print("\nExample 2: Serialize to JSON")
print("-" * 50)
json_output = file.model_dump_json(indent=2, exclude_none=True)
print(json_output)

# Example 3: Deserialize from JSON
print("\nExample 3: Deserialize from JSON")
print("-" * 50)
restored_file = File.model_validate_json(json_output)
print(f"Restored file name: {restored_file.name}")
print(f"Matches original: {restored_file.name == file.name}")

# Example 4: Working with enums
print("\nExample 4: Working with enums")
print("-" * 50)
print(f"StatusId.VALUE_1 = {StatusId.VALUE_1}")
print(f"StatusId.VALUE_2 = {StatusId.VALUE_2}")
print(f"StatusId.VALUE_3 = {StatusId.VALUE_3}")

# Example 5: Extra fields (OCSF allows additional fields)
print("\nExample 5: Extra fields support")
print("-" * 50)
data = {
    "name": "test.txt",
    "type_id": 1,
    "custom_field": "This is a custom field!",
    "another_custom": 42,
}

file_with_extras = File.model_validate(data)
dumped = file_with_extras.model_dump()

print(f"Original custom field: {data['custom_field']}")
print(f"Preserved in model: {dumped['custom_field']}")

# Example 6: Working with different OCSF versions
print("\nExample 6: Multiple OCSF versions")
print("-" * 50)
from ocsf.v1_7_0 import File as File_v1_7
from ocsf.v1_6_0 import File as File_v1_6
from ocsf.v1_5_0 import File as File_v1_5
from ocsf.v1_2_0 import File as File_v1_2
from ocsf.v1_1_0 import File as File_v1_1
from ocsf.v1_0_0 import File as File_v1_0

print(f"File from v1.7.0 (latest): {File_v1_7.__module__}")
print(f"File from v1.6.0: {File_v1_6.__module__}")
print(f"File from v1.5.0: {File_v1_5.__module__}")
print(f"File from v1.2.0: {File_v1_2.__module__}")
print(f"File from v1.1.0: {File_v1_1.__module__}")
print(f"File from v1.0.0: {File_v1_0.__module__}")

print("\n" + "=" * 50)
print("✅ All examples completed successfully!")
