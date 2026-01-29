# GitHub Actions Workflows

This document explains the CI/CD workflows configured for this project.

## Test Workflow (`test.yml`)

Runs on every push and pull request to ensure code quality.

### Jobs

#### 1. **test** - Multi-platform Test Matrix

- **Platforms**: Ubuntu, macOS, Windows
- **Python versions**: 3.10, 3.11, 3.12, 3.13, 3.14
- **Steps**:
  - Install dependencies from `pyproject.toml`
  - Run pytest with coverage
  - Upload coverage to Codecov (Ubuntu + Python 3.12 only)

#### 2. **lint** - Code Quality Checks

- **Platform**: Ubuntu
- **Python version**: 3.12
- **Checks**:
  - `ruff format --check` - Verify code formatting
  - `ruff check` - Linting
  - `mypy` - Type checking

#### 3. **verify-generation** - Generator Verification

- **Platform**: Ubuntu
- **Python version**: 3.12
- **Tests**:
  - Schema fetching from GitHub
  - Model generation (sample test)
  - Ensures the generator works correctly

### Triggers

- Push to `main`, `master`, or `develop` branches
- Pull requests to `main` or `master`
- Manual dispatch via GitHub UI

## Publish Workflow (`publish.yml`)

Handles building and publishing to PyPI.

### Jobs

#### 1. **build** - Build Distribution

- Creates wheel and source distribution
- Validates distribution with `twine check`
- Uploads artifacts for publishing

#### 2. **publish-to-pypi** - Publish to Production PyPI

- **Trigger**: Only on version tags (e.g., `1.7.0.20260129`)
- Uses trusted publishing (OIDC)
- Requires `pypi` environment configured in GitHub

#### 3. **publish-to-testpypi** - Publish to Test PyPI

- **Trigger**: Manual dispatch only
- For testing releases before production
- Requires `testpypi` environment configured

#### 4. **create-github-release** - Create GitHub Release

- Creates a GitHub release with artifacts
- Runs after successful PyPI publish
- Attaches distribution files to release

### Triggers

- Push tags matching `*.*.*.*` (e.g., `1.7.0.20260129`)
- Manual dispatch for TestPyPI

## Version Tag Format

This project uses a special version format: `{ocsf_version}.{generation_date}`

**Example**: `1.7.0.20260129`

- OCSF version: `1.7.0`
- Generated on: January 29, 2026

To create a release:

```bash
# Generate models with current date
python scripts/generate.py

# Get the version from the package
VERSION=$(python -c "import ocsf; print(ocsf.__version__)")

# Create and push tag
git tag $VERSION
git push origin $VERSION
```

## Required GitHub Secrets

For full functionality, configure these in your repository:

1. **CODECOV_TOKEN** (optional)
   - For uploading test coverage
   - Get from https://codecov.io

2. **PyPI Trusted Publishing** (required for publishing)
   - Configure at https://pypi.org/manage/account/publishing/
   - Add GitHub repository and environment name `pypi`
   - No token needed - uses OIDC

3. **TestPyPI Trusted Publishing** (optional)
   - Configure at https://test.pypi.org/manage/account/publishing/
   - Add GitHub repository and environment name `testpypi`

## Local Testing

Before pushing, run the same checks locally:

```bash
# Install dependencies
pip install -e ".[dev,generator]"

# Run tests
pytest tests/ -v --cov=ocsf

# Check formatting
ruff format --check src/ generator/ tests/

# Run linting
ruff check src/ generator/ tests/

# Type checking
mypy src/ocsf/ --ignore-missing-imports

# Test generation
python -m generator.schema_fetcher 1.7.0
```
