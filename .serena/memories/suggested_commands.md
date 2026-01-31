# Suggested Commands for pydantic-ocsf

## Package Manager: uv
All commands use `uv` for dependency management.

## Development Setup
```bash
# Install development dependencies
just install

# Install all dependencies including generator
just install-all
```

## Testing
```bash
# Run tests with coverage (default Python 3.12)
just test

# Run tests with specific Python version
just test python="3.11"

# Run tests with verbose output
just test-verbose

# Run tests manually with pytest
uv run --python 3.12 pytest tests/ -v --cov=ocsf
```

## Code Quality
```bash
# Run all checks (format, lint, type check, tests)
just check

# Format code (auto-fix)
just format

# Check formatting without fixing
just format-check

# Lint with ruff
just lint

# Lint with auto-fix
just lint-fix

# Type check with mypy
just typecheck

# Quick development check (format + lint-fix + test)
just dev-check
```

## Schema Management
```bash
# Fetch OCSF schema (default v1.7.0)
just fetch-schema

# Fetch specific version
just fetch-schema version="1.6.0"

# Generate models for a version (current approach)
just generate-models version="1.7.0"
```

## Build & Distribution
```bash
# Clean build artifacts and caches
just clean

# Build distribution packages
just build
```

## Git Operations
```bash
# Standard git commands
git status
git add <files>
git commit -m "message"
git push
```

## File Operations
```bash
# Linux standard commands
ls -la
find . -name "*.py"
grep -r "pattern" src/
cat <file>
```

## System Information
- **OS**: Linux
- **Shell**: bash
- **Package Manager**: uv (Python-specific), apt (system-level, but use Homebrew for persistence)