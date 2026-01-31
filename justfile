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
    uv run --python 3.12 ruff format --check src/ tests/ scripts/

# Format code (fix formatting issues)
format:
    uv run --python 3.12 ruff format src/ tests/ scripts/

# Lint code with ruff
lint:
    uv run --python 3.12 ruff check src/ tests/ scripts/

# Lint and auto-fix issues where possible
lint-fix:
    uv run --python 3.12 ruff check --fix src/ tests/ scripts/

# Type check with mypy
typecheck:
    uv run --python 3.12 mypy src/ocsf/ --ignore-missing-imports

# Download OCSF schemas (v1.7.0)
download-schemas:
    python3 scripts/download_schemas.py

# Regenerate type stub files from schemas
regenerate-stubs:
    python3 scripts/regenerate_stubs.py

# Download schemas and regenerate stubs (full rebuild)
rebuild: download-schemas regenerate-stubs

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
