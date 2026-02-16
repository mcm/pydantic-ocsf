# Changelog

All notable changes to this project will be documented in this file.

## [2.0.6] - 2026-02-16

### Fixed

- Fixed sibling reconciler to support OCSF "Other" (ID=99) exception
- When `foo_id=99`, the `foo` label field can now contain any custom value
- When `foo_id=99` is provided without `foo`, it still auto-fills "Other"
- Sibling reconciler now handles Python field names (e.g., `type_`) before normalization
- Fixed sibling reconciler consistency check exception handling to properly raise validation errors
- Round-trip serialization now works correctly: `Analytic(type_="Risk", type_id=99)` preserves "Risk"
- Moved field name normalization into model factory to ensure correct validator execution order

## [2.0.5] - 2026-02-15

Complete fix for reserved keyword sibling field serialization issues. This release includes all fixes from development commits for proper OCSF-compliant JSON output.

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
