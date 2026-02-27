# Python Style Guide

Based on existing project conventions detected from `.flake8`, `pyproject.toml`, and `AGENTS.md`.

## Formatting

- **Formatter**: Black
- **Import sorting**: isort (Black-compatible profile)
- **Max line length**: 100 characters
- **Target Python**: 3.12+

Run formatting:

```bash
make backend-format        # Apply black + isort
make backend-format-check  # Check only (CI mode)
```

## Linting

- **Linter**: flake8 with `.flake8` config
- **Type checker**: mypy (strict mode)

Run checks:

```bash
make backend-lint       # flake8
make backend-typecheck  # mypy
```

## Naming Conventions

| Element          | Convention     | Example                    |
| ---------------- | -------------- | -------------------------- |
| Variables        | `snake_case`   | `board_id`                 |
| Functions        | `snake_case`   | `get_active_membership()`  |
| Classes          | `PascalCase`   | `AgentLifecycleService`    |
| Constants        | `UPPER_SNAKE`  | `DEFAULT_GATEWAY_FILES`    |
| Modules/files    | `snake_case`   | `board_lifecycle.py`       |
| Private members  | `_snake_case`  | `_build_context()`         |

## Code Organization

### Models (`backend/app/models/`)

- One model per file
- Inherit from `QueryModel` for ORM query interface
- Use `TenantScoped` base for org-scoped tables
- SQLModel with `table=True` for database-backed models

### Schemas (`backend/app/schemas/`)

- One domain per file
- Follow `XyzCreate`, `XyzRead`, `XyzUpdate` naming pattern
- Use Pydantic v2 model validators

### API Routes (`backend/app/api/`)

- One router per domain
- Use FastAPI `Depends()` for auth, session, authorization
- Centralize reusable dependencies in `deps.py`

### Services (`backend/app/services/`)

- Business logic lives here, not in route handlers
- Route handlers should be thin wrappers calling services
- Services receive DB session via dependency injection

## Type Annotations

- All function signatures must have type annotations
- Use `from __future__ import annotations` for forward references
- Use `TYPE_CHECKING` guard for import-only types
- mypy strict mode is enforced

```python
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlmodel.ext.asyncio.session import AsyncSession
```

## Async Patterns

- All database operations use async/await
- Use `AsyncSession` from SQLModel
- Prefer async context managers for resource cleanup

## Testing

- Framework: pytest (async with pytest-asyncio)
- Coverage: 100% on scoped modules (see `make backend-coverage`)
- Test files: `test_*.py` naming in `backend/tests/`
- Add tests when behavior changes

## Import Order

Enforced by isort with Black-compatible profile:

1. Standard library
2. Third-party packages
3. Local application imports

## Common Patterns

### Dependency Injection

```python
@router.get("")
async def list_items(
    session: AsyncSession = Depends(get_session),
    ctx: OrganizationContext = Depends(require_org_admin),
) -> LimitOffsetPage[ItemRead]:
    service = ItemService(session)
    return await service.list_items(ctx=ctx)
```

### Error Handling

- Use FastAPI's `HTTPException` for API errors
- Custom exception types in `services/openclaw/exceptions.py`
- Centralized error handling in `core/error_handling.py`
