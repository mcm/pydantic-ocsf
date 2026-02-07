# GitHub Actions Workflows

This document explains the CI/CD workflows configured for this project.

## Tools Used

- **[uv](https://github.com/astral-sh/uv)**: Modern Python package manager for fast dependency installation
- **[just](https://github.com/casey/just)**: Command runner for common development tasks
- **Python 3.9-3.14**: Full support matrix across multiple platforms

## Test Workflow (`test.yml`)

Runs on every push and pull request to ensure code quality.

### Jobs

#### 1. **test** - Multi-platform Test Matrix

Tests the package across multiple platforms and Python versions to ensure compatibility.

- **Platforms**: Ubuntu, macOS, Windows
- **Python versions**: 3.9, 3.10, 3.11, 3.12, 3.13, 3.14
- **Steps**:
  1. Install uv and just
  2. Install package with dev and generator dependencies: `uv pip install -e ".[dev,generator]"`
  3. Download OCSF schemas and regenerate stubs: `just rebuild`
  4. Run pytest with coverage: `uv run pytest tests/ -v --cov=ocsf`
  5. Upload coverage to Codecov (Ubuntu + Python 3.12 only)

**Why download schemas?**
Schemas are generated during build, not committed to git. The workflow must download them before testing.

#### 2. **lint** - Code Quality Checks

Ensures code meets quality standards.

- **Platform**: Ubuntu
- **Python version**: 3.12
- **Checks**:
  - `just format-check` - Verify code formatting with ruff
  - `just lint` - Linting with ruff
  - `just typecheck` - Type checking with mypy

All commands use the justfile for consistency with local development.

#### 3. **verify-generation** - Schema Generation Verification

Verifies that schemas can be downloaded and stubs regenerated.

- **Platform**: Ubuntu
- **Python version**: 3.12
- **Tests**:
  - Install all dependencies: `just install-all`
  - Download schemas and regenerate stubs: `just rebuild`
  - Ensures the generation pipeline works correctly

### Triggers

- Push to `main`, `master`, or `develop` branches
- Pull requests to `main` or `master`
- Manual dispatch via GitHub UI (`workflow_dispatch`)

---

## Publish Workflow (`publish.yml`)

Handles building and publishing releases to PyPI.

### Jobs

#### 1. **build** - Build Distribution

Creates wheel and source distribution packages.

- **Steps**:
  1. Install uv and just
  2. Validate that git tag version matches `pyproject.toml` version
  3. Install build dependencies (hatch, twine) and generator extras
  4. Download schemas and regenerate stubs: `just rebuild`
  5. Build distribution with hatch: `uvx hatch build`
  6. Validate distribution: `uvx twine check dist/*`
  7. Upload artifacts for publishing

**Critical**: Schemas must be downloaded before building, otherwise the published package won't include schema files and will be broken.

#### 2. **publish-to-pypi** - Publish to Production PyPI

Publishes the built distribution to PyPI.

- **Trigger**: Only on version tags (e.g., `v2.0.0`)
- **Authentication**: Uses trusted publishing (OIDC) - no manual tokens required
- **Environment**: Requires `pypi` environment configured in GitHub repository settings

#### 3. **create-github-release** - Create GitHub Release

Creates a GitHub release with distribution artifacts.

- **Steps**:
  1. Download distribution packages from build job
  2. Create release with `gh release create`
  3. Attach wheel and source distribution to release
  4. Link to CHANGELOG.md for release notes

### Triggers

- Push tags matching `v*.*.*` pattern (e.g., `v2.0.0`, `v2.1.0`)
- Tag must match version in `pyproject.toml` or workflow will fail

---

## Version Tag Format

This project uses [Semantic Versioning](https://semver.org/) starting with v2.0.0:

**Format**: `vMAJOR.MINOR.PATCH`

**Examples:**
- `v2.0.0` - Major release with breaking changes
- `v2.1.0` - Minor release with new features (backward compatible)
- `v2.0.1` - Patch release with bug fixes

### Creating a Release

```bash
# 1. Update version in pyproject.toml
# Edit: version = "2.1.0"

# 2. Update CHANGELOG.md with release notes

# 3. Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "chore: prepare release v2.1.0"

# 4. Create and push tag (must match pyproject.toml version)
git tag v2.1.0
git push origin main
git push origin v2.1.0
```

The workflow will automatically:
- Validate the tag matches `pyproject.toml`
- Download schemas and generate stubs
- Build the distribution
- Publish to PyPI
- Create a GitHub release

---

## Required GitHub Secrets & Configuration

### Secrets

**CODECOV_TOKEN** (optional)
- For uploading test coverage
- Get from https://codecov.io after setting up your repository
- Add to: Settings → Secrets and variables → Actions

### Environments

**pypi** (required for publishing)
1. Go to repository Settings → Environments
2. Create environment named `pypi`
3. Configure PyPI trusted publishing:
   - Visit https://pypi.org/manage/account/publishing/
   - Add your GitHub repository (owner/repo)
   - Set environment name: `pypi`
   - Workflow: `.github/workflows/publish.yml`
   - No token needed - uses OIDC authentication

---

## Local Testing

Before pushing, run the same checks locally using the justfile:

```bash
# Install dependencies (including generator tools)
just install-all

# Download schemas and regenerate stubs
just rebuild

# Run all checks (format, lint, typecheck, tests)
just check

# Or run individually:
just format        # Format code with ruff
just lint          # Lint with ruff
just typecheck     # Type check with mypy
just test          # Run tests with coverage
```

### Manual Commands (without just)

If you prefer not to use just:

```bash
# Install dependencies
uv sync --extra dev --extra generator

# Download schemas and regenerate stubs
uv run python scripts/download_schemas.py
uv run python scripts/regenerate_stubs.py

# Run tests
uv run pytest tests/ -v --cov=ocsf

# Check formatting
uv run ruff format --check src/ tests/ scripts/

# Lint
uv run ruff check src/ tests/ scripts/

# Type check
uv run mypy src/ocsf/ scripts/ --ignore-missing-imports
```

---

## Justfile Commands Reference

Quick reference for all available just commands:

| Command | Description |
|---------|-------------|
| `just install` | Install development dependencies |
| `just install-all` | Install all dependencies including generator |
| `just test` | Run tests with coverage |
| `just lint` | Lint code with ruff |
| `just format` | Format code with ruff |
| `just format-check` | Check formatting without changes |
| `just typecheck` | Type check with mypy |
| `just check` | Run all checks (lint, format-check, typecheck, test) |
| `just download-schemas` | Download OCSF schemas |
| `just regenerate-stubs` | Regenerate type stub files |
| `just rebuild` | Download schemas and regenerate stubs |
| `just clean` | Clean build artifacts and caches |
| `just build` | Build distribution packages |

Run `just --list` to see all available commands.

---

## Troubleshooting

### Tests fail with "OCSF version not found"

**Cause**: Schemas haven't been downloaded.

**Solution**: Run `just rebuild` to download schemas and regenerate stubs.

### Version tag mismatch error in workflow

**Cause**: Git tag version doesn't match `pyproject.toml` version.

**Solution**: Ensure the tag (without `v` prefix) exactly matches the version in `pyproject.toml`:
- Tag: `v2.0.0` → pyproject.toml: `version = "2.0.0"`

### Import errors in tests

**Cause**: Package not installed in editable mode or schemas missing.

**Solution**:
```bash
uv pip install -e ".[dev,generator]"
just rebuild
```

### Build fails with missing schema files

**Cause**: Schemas not downloaded before building.

**Solution**: Always run `just rebuild` before `just build`.

---

## CI/CD Best Practices

1. **Always run `just check` before pushing** - catches issues locally before CI
2. **Let CI download schemas** - don't commit schema files to git
3. **Use justfile commands** - ensures consistency between local and CI
4. **Test across Python versions locally** - use `uv run --python 3.9 pytest` to test specific versions
5. **Keep workflows in sync with justfile** - update both when changing build process

---

## Questions?

- **Issues**: https://github.com/mcm/pydantic-ocsf/issues
- **Discussions**: https://github.com/mcm/pydantic-ocsf/discussions
- **Documentation**: See README.md and CONTRIBUTING.md
