# Justfile for pydantic-ocsf
# Run 'just --list' to see all available commands

# Default recipe - show available commands
default:
    @just --list

# Install development dependencies
install:
    uv sync --extra dev

# Install all dependencies including generator
install-all:
    uv sync --all-extras

# Run all checks (format check, lint, type check, tests)
check: lint format-check typecheck test

# Run tests with coverage
test python="3.12":
    uv run --python {{python}} pytest tests/ -v --cov=ocsf --cov-report=xml --cov-report=term

# Run tests with verbose output
test-verbose python="3.12":
    uv run --python {{python}} pytest tests/ -vv --cov=ocsf --cov-report=xml --cov-report=term

# Check code formatting without making changes
format-check:
    uv run --python 3.12 ruff format --check src/ generator/ tests/

# Format code (fix formatting issues)
format:
    uv run --python 3.12 ruff format src/ generator/ tests/

# Lint code with ruff
lint:
    uv run --python 3.12 ruff check src/ generator/ tests/

# Lint and auto-fix issues where possible
lint-fix:
    uv run --python 3.12 ruff check --fix src/ generator/ tests/

# Type check with mypy
typecheck:
    uv run --python 3.12 mypy src/ocsf/ --ignore-missing-imports

# Fetch OCSF schema (default version 1.7.0)
fetch-schema version="1.7.0":
    python -m generator.schema_fetcher {{version}}

# Generate models for a specific OCSF version
generate-models version="1.7.0":
    #!/usr/bin/env python3
    from pathlib import Path
    from generator.schema_parser import parse_schema
    from generator.model_generator import generate_models
    schema = parse_schema('{{version}}', cache_dir=Path('.schema_cache'))
    generate_models(schema, Path('src/ocsf'))
    print('✓ Model generation successful')

# Clean build artifacts and caches
clean:
    rm -rf build/ dist/ *.egg-info
    rm -rf .pytest_cache .mypy_cache .ruff_cache
    rm -rf htmlcov/ .coverage coverage.xml
    find . -type d -name __pycache__ -exec rm -rf {} +

# Build distribution packages
build:
    pip install --upgrade build
    python -m build

# Run a quick development check (format, lint, test)
dev-check: format lint-fix test
