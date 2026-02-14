# Changelog

All notable changes to this project will be documented in this file.

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
