# Changelog

All notable changes to this project will be documented in this file.

## [2.0.4] - 2026-02-15

### Fixed

- Fixed reserved keyword sibling fields to serialize with correct aliases
- The `type_` field (sibling of `type_id`) now correctly serializes as `type` instead of `type_`
- Removed `populate_by_name=True` from OCSFBaseModel to prevent duplicate field generation
- Fixed sibling reconciler to use OCSF field names (aliases) instead of Python field names
- Eliminates duplicate fields in serialization output (e.g., both `type` and `type_` appearing)
- Affects 61 models with reserved keyword fields
- Ensures OCSF-compliant JSON output for all reserved keyword sibling fields

## [2.0.3] - 2026-02-14

### Fixed

- Fixed sibling field inference to respect the `sibling` attribute in OCSF dictionary definitions
- Resolved duplicate field generation where both `activity` and `activity_name` were created
- Events now correctly use schema-defined sibling field names (e.g., `activity_name` instead of inferred `activity`)

## [2.0.0] - 2026-02-06

### Changed

- Schema JSON files are now bundled, and models are generated on-the-fly from the schema

## [1.x.x] - Previous Versions

Previous versions were statically generated in advance from the scheam files.
