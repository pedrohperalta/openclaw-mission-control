# Product Guidelines

## Voice and Tone

**Concise and direct.** Documentation and UI text should be minimal, precise, and operational. Avoid filler words, marketing language, and unnecessary qualifiers. Say what something does, not what it "helps" do.

Examples:

- Good: "Creates a board and assigns a lead agent."
- Avoid: "This feature helps you easily create a new board and conveniently assign a lead agent."

## Design Principles

### Operations-first

Built for running agent work reliably, not just creating tasks. Every feature should serve day-to-day operational needs. If a feature doesn't help someone operate the system, it doesn't belong.

### Governance built-in

Approvals, auth modes, and clear control boundaries are first-class concerns. Safety and auditability are not optional add-ons -- they are part of the core design.

### API-first

Operators and automation clients act on the same objects and lifecycle. Every UI action has an API equivalent. The API contract is the source of truth; the UI is a consumer of that contract.

## Additional Standards

- **No emoji** in code, commits, or documentation unless explicitly requested.
- **Conventional Commits** for all commit messages.
- **Small, focused PRs** -- one concern per pull request.
- **Tests accompany behavior changes** -- if the behavior changed, the tests must reflect it.
