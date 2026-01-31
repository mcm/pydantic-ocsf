# pydantic-ocsf Project Overview

## Purpose
Provides Pydantic v2 models for the Open Cybersecurity Schema Framework (OCSF).
Currently uses build-time code generation for all 244 models across 6 OCSF versions.

## Current Status
- **Version**: 1.7.0.20260130
- **Architecture**: Pre-generated models at build time
- **Supported OCSF versions**: 1.0.0, 1.1.0, 1.2.0, 1.5.0, 1.6.0, 1.7.0
- **Problem**: 4.27s import times, 50MB package size per version, single version lock-in

## JIT Rewrite Project
Complete architectural rewrite to use Just-In-Time (JIT) model creation:
- **Goal**: 14.6x faster imports (4,270ms → 292ms), multi-version support, 80% smaller package
- **Status**: POC validated in `TRANSPARENT_JIT_VALIDATED.md`
- **Approach**: Import hooks + on-demand model creation from schema JSON

## Tech Stack
- **Python**: 3.9+ (supports 3.9, 3.10, 3.11, 3.12, 3.13, 3.14)
- **Validation**: Pydantic v2.x (>=2.5, <3.0)
- **Build**: Hatchling
- **Testing**: pytest, pytest-cov
- **Type Checking**: mypy, pyright
- **Linting**: ruff
- **Package Manager**: uv

## Directory Structure
```
src/ocsf/
├── __init__.py          # Package init with lazy import
├── _base.py             # OCSFBaseModel base class
├── _sibling_enum.py     # SiblingEnum for ID/label pairs
├── v1_0_0/ through v1_7_0/  # Pre-generated version modules (to be replaced)
└── py.typed            # PEP 561 marker

generator/
├── schema_fetcher.py    # Downloads OCSF schemas
├── schema_parser.py     # Parses schema JSON
├── model_generator.py   # Generates Python models (current approach)
└── templates/           # Jinja2 templates for generation

tests/                   # Test suite
scripts/                 # Utility scripts
```

## Key Design Decisions
1. **Import Hook System**: Transparent JIT with zero API changes
2. **Sibling Attributes**: Nested enum classes for _id/label pairs (e.g., `FileActivity.ActivityId.CREATE`)
3. **Multi-Version**: Support multiple OCSF versions in same Python process
4. **Schema Storage**: Downloaded during build, bundled as JSON (not committed to git)
5. **Type Hints**: Pre-generated .pyi stub files for type checkers