# Tech Stack

## Languages

| Language   | Version | Usage          |
| ---------- | ------- | -------------- |
| Python     | 3.12+   | Backend API    |
| TypeScript | 5.x     | Frontend UI    |

## Frontend

| Technology         | Version  | Purpose                             |
| ------------------ | -------- | ----------------------------------- |
| Next.js            | 16.x     | React framework (App Router)        |
| React              | 19.x     | UI library                          |
| TanStack Query     | 5.x      | Server state management             |
| TanStack Table     | 8.x      | Headless data tables                |
| Tailwind CSS       | 4.x      | Utility-first styling               |
| Radix UI           | latest   | Accessible UI primitives            |
| Recharts           | 3.x      | Charts and visualizations           |
| Orval              | 8.x      | OpenAPI-to-React-Query code gen     |
| Clerk              | 6.x      | Authentication (optional)           |
| Lucide React       | latest   | Icon library                        |

## Backend

| Technology         | Version  | Purpose                             |
| ------------------ | -------- | ----------------------------------- |
| FastAPI            | 0.131.x  | Web framework                       |
| SQLModel           | latest   | ORM (SQLAlchemy + Pydantic)         |
| SQLAlchemy         | 2.x      | Async database engine               |
| Alembic            | latest   | Database migrations                 |
| Pydantic Settings  | latest   | Configuration management            |
| psycopg            | 3.x      | PostgreSQL async driver             |
| Jinja2             | latest   | Agent workspace template rendering  |
| RQ (Redis Queue)   | latest   | Background job processing           |
| uv                 | latest   | Python package manager              |

## Data Stores

| Store      | Version | Purpose                                    |
| ---------- | ------- | ------------------------------------------ |
| PostgreSQL | 16      | Primary relational database                |
| Redis      | 7       | Background job queue, webhook dispatch     |

## Infrastructure

| Component          | Purpose                                        |
| ------------------ | ---------------------------------------------- |
| Docker Compose     | Local development stack (db, redis, backend, frontend, worker) |
| Portainer + Traefik| Production deployment with TLS and reverse proxy |
| GitHub Actions     | CI/CD (lint, typecheck, test, coverage, e2e)   |
| install.sh         | Interactive bootstrap (Docker or local mode)   |

## Key Dependencies

### Backend

- `fastapi-pagination` -- limit-offset pagination
- `sse-starlette` -- Server-Sent Events for real-time streaming
- `pydantic-settings` -- env-based configuration
- `black`, `isort`, `flake8`, `mypy` -- code quality tooling

### Frontend

- `cmdk` -- command palette
- `cypress` -- end-to-end testing
- `vitest` -- unit testing
- `@testing-library/react` -- component testing
