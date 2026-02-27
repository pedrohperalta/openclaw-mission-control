# Workflow

## TDD Policy

**Moderate** -- Tests are encouraged and expected for behavior changes, but implementation is not blocked if tests aren't written first. Critical paths and complex logic should always have test coverage.

- Backend: pytest with coverage enforcement on scoped modules (100% on selected modules via `make backend-coverage`)
- Frontend: Vitest + Testing Library for unit/component tests, Cypress for E2E

## Commit Strategy

**Conventional Commits** -- All commits must follow the Conventional Commits specification.

Prefixes:

- `feat:` -- new feature
- `fix:` -- bug fix
- `docs:` -- documentation changes
- `test:` -- test additions or changes
- `chore:` -- maintenance, dependency updates
- `refactor:` -- code restructuring without behavior change

Examples:

```
feat: add webhook retry configuration
fix: resolve CORS issue with gateway endpoints
docs: update deployment guide for Traefik setup
test(core): add coverage for error handling middleware
```

## Code Review Policy

**Required for all changes.** Every pull request needs at least one review before merge.

PR expectations (from CONTRIBUTING.md):

- Small and focused scope
- Clear description of what changed and why
- Tests added/updated when behavior changes
- Docs updated when contributor-facing or operator-facing behavior changes
- `make check` passing (lint + typecheck + tests + coverage + build)

## Verification Checkpoints

**At track completion only.** Manual verification is required when an entire feature track is complete. Individual tasks and phases proceed without manual checkpoints.

## Task Lifecycle

1. **Pending** -- Task created, not yet started
2. **In Progress** -- Actively being worked on
3. **Review** -- Implementation done, awaiting verification
4. **Done** -- Verified and complete

## Quality Gates

Before any PR is merged:

```bash
make check    # Runs: lint + typecheck + tests + coverage + frontend build
```

Individual checks:

```bash
make backend-lint          # flake8
make backend-typecheck     # mypy (strict)
make backend-test          # pytest
make backend-coverage      # 100% on scoped modules
make frontend-lint         # eslint
make frontend-typecheck    # tsc
make frontend-test         # vitest
make frontend-build        # next build
make docs-check            # markdown lint + link check
```

## Branch Strategy

- Feature branches created from `master`
- One migration per PR (enforced by CI)
- Squash merge preferred for clean history
