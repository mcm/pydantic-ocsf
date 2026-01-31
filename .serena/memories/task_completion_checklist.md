# Task Completion Checklist

When completing any task in pydantic-ocsf, ensure:

## Code Quality
- [ ] Code follows style conventions (see code_style_conventions.md)
- [ ] All public APIs have docstrings (Google style)
- [ ] Type hints use Python 3.9+ built-in generics
- [ ] No ruff errors: `just lint`
- [ ] No format issues: `just format-check`
- [ ] No type errors: `just typecheck`

## Testing
- [ ] New code has test coverage
- [ ] All tests pass: `just test`
- [ ] Test coverage maintained (>90% preferred)
- [ ] Performance benchmarks pass (if applicable)

## Documentation
- [ ] README.md updated if public API changed
- [ ] CHANGELOG.md updated with changes
- [ ] Docstrings added/updated
- [ ] Comments explain "why" not "what"

## Before Committing
```bash
# Run full check suite
just check

# Verify coverage
just test

# Clean artifacts
just clean
```

## Git Workflow
```bash
# Stage changes
git add <files>

# Commit with descriptive message
git commit -m "feat: add JIT model factory

- Implement import hook for transparent JIT
- Add OCSFVersionModule with on-demand model creation
- Add model caching for 133x speedup on cache hits"

# Push to remote
git push
```

## Performance Considerations
For the JIT rewrite, ensure:
- [ ] Single model creation <15ms
- [ ] Cached access <0.1ms
- [ ] 25 model import <300ms
- [ ] Cache speedup >100x
- [ ] Memory per version <2MB

## Breaking Changes
If introducing breaking changes:
- [ ] Document in CHANGELOG.md
- [ ] Update migration guide
- [ ] Update README.md examples
- [ ] Bump major version (if semantic versioning)