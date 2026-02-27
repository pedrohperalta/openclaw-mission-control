# TypeScript Style Guide

Based on existing project conventions detected from ESLint config, Prettier, and `AGENTS.md`.

## Formatting

- **Formatter**: Prettier
- **Linter**: ESLint
- **Target**: TypeScript 5, ES2022+

Run checks:

```bash
make frontend-lint          # eslint
make frontend-typecheck     # tsc --noEmit
make frontend-format-check  # prettier --check
```

## Naming Conventions

| Element          | Convention     | Example                      |
| ---------------- | -------------- | ---------------------------- |
| Components       | `PascalCase`   | `TaskBoard`, `DashboardSidebar` |
| Variables        | `camelCase`    | `boardId`, `isAdmin`         |
| Functions        | `camelCase`    | `useOrganizationMembership()`|
| Constants        | `camelCase`    | `statusLabel`                |
| Types/Interfaces | `PascalCase`   | `BoardRead`, `ApiError`      |
| Files (components)| `PascalCase`  | `TaskCard.tsx`               |
| Files (utilities)| `kebab-case`   | `api-base.ts`, `list-delete.ts` |
| Unused destructured vars | `_prefix` | `const [_unused, setter] = ...` |

## Component Architecture

### Hierarchy (Atomic Design)

```
components/
  atoms/        -- Smallest reusable pieces (BrandMark, StatusPill)
  molecules/    -- Compound components (TaskCard, DependencyBanner)
  organisms/    -- Complex features (DashboardSidebar, TaskBoard)
  templates/    -- Page-level layouts (DashboardShell)
  ui/           -- Radix-based primitives (Button, Dialog, Input)
  providers/    -- Context providers (AuthProvider, QueryProvider)
  tables/       -- Data table components (DataTable)
  charts/       -- Chart components (MetricSparkline)
```

### Domain Components

Feature-specific components are grouped by domain:

```
components/
  boards/       -- BoardsTable
  agents/       -- AgentsTable
  board-groups/ -- BoardGroupsTable
  tags/         -- TagsTable, TagForm
  gateways/     -- GatewaysTable, GatewayForm
  skills/       -- MarketplaceSkillsTable, SkillInstallDialog
  activity/     -- ActivityFeed
  organization/ -- MembersInvitesTable, BoardAccessTable
```

## State Management

### Server State: TanStack React Query

- Primary state management for all API data
- 15-second stale time, 5-minute garbage collection
- Auto-refetch on window focus
- No retry on mutations

### URL State: Search Params

- Table sorting, filters, and pagination encoded in URL
- Enables shareable links and browser back/forward

### Local State: React useState

- UI-only state (modals, form state, loading indicators)

### Real-time: SSE Streams

- Server-Sent Events for live activity
- Exponential backoff reconnection (via `backoff.ts`)

## API Client

### Generated Client (Orval)

- Auto-generated from backend OpenAPI schema
- **Never edit** files in `src/api/generated/` directly
- Regenerate with: `npm run api:gen`
- Config: `orval.config.ts`

### Custom Mutator (`src/api/mutator.ts`)

- Handles base URL, auth token injection, error parsing
- Supports local and Clerk auth modes

### Hook Usage Pattern

```tsx
import { useListBoardsApiV1BoardsGet } from "@/api/generated/boards/boards";
import { ApiError } from "@/api/mutator";

function BoardsList() {
  const { data, isLoading } = useListBoardsApiV1BoardsGet<BoardListResponse, ApiError>();
  // ...
}
```

## Auth Patterns

- `useAuth()` -- works in both Clerk and local modes
- `useUser()` -- returns user profile
- `SignedIn` / `SignedOut` -- conditional rendering components
- Auth mode determined by `NEXT_PUBLIC_AUTH_MODE` env var

## File Organization

### Pages (`src/app/`)

- Next.js App Router convention
- `page.tsx` for route content
- `layout.tsx` for shared layouts
- `"use client"` directive for client components

### Utilities (`src/lib/`)

- Pure functions and custom hooks
- `utils.ts` for general helpers (cn/clsx)
- `api-base.ts` for API URL resolution
- `use-*.ts` for custom hooks

## Testing

- **Unit tests**: Vitest + Testing Library
- **E2E tests**: Cypress
- Run: `npm test` (unit), `npm run e2e` (end-to-end)
- Add tests when behavior changes

## Common Patterns

### Optimistic Updates

```tsx
const deleteMutation = useDeleteBoardMutation({
  onMutate: async (boardId) => {
    // Cancel outgoing queries, snapshot, and optimistically update
  },
  onError: (err, boardId, context) => {
    // Rollback on error
  },
});
```

### URL-based Sorting

```tsx
const { sortField, sortOrder, toggleSort } = useUrlSorting();
```

### Conditional Admin UI

```tsx
const { isAdmin } = useOrganizationMembership(isSignedIn);
if (!isAdmin) return <AdminOnlyNotice />;
```
