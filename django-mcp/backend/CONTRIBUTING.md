# Contributing Guide

## Git Workflow

### Branching Strategy

| Branch | Purpose | Base |
|---|---|---|
| `main` | Production-ready code | — |
| `develop` | Integration branch | `main` |
| `feature/<TICKET>_<slug>` | Feature work | `develop` |
| `bugfix/<TICKET>_<slug>` | Bug fixes | `develop` |
| `hotfix/<TICKET>_<slug>` | Production hotfixes | `main` |
| `release/<version>` | Release preparation | `develop` |

### Commit Message Convention

Format: `<type>(<scope>): <subject>`

**Types:** `feat` | `fix` | `docs` | `style` | `refactor` | `test` | `chore` | `perf` | `ci` | `build` | `revert`

**Examples:**
```
feat(orders): add order creation endpoint
fix(auth): resolve token refresh race condition
docs(readme): update docker instructions
chore(deps): upgrade Django to 5.0.4
```

## Development Setup

```bash
python -m venv .venv && source .venv/bin/activate
make install   # installs deps + pre-commit hooks
cp .env.example .env
make migrate
make run
```

## Code Style

- **Formatter**: Black (line length 120)
- **Imports**: isort (black profile)
- **Linter**: Flake8 + Pylint
- Pre-commit hooks enforce all of the above automatically.

## Testing

- Write tests for all new features and bug fixes.
- Aim for >80% coverage.
- Run `make test` before pushing.

## Pull Request Checklist

- [ ] Branch follows naming convention
- [ ] Commits follow Conventional Commits format
- [ ] Tests added / updated
- [ ] Migrations created if models changed
- [ ] `make lint` passes
- [ ] `make test` passes
- [ ] PR title: `<TICKET_ID> | <TYPE> | <SHORT_TITLE>`
- [ ] PR body includes: Ticket, Summary, Affected areas, Tests, Design link, Review focus

## Code Review Guidelines

- Review for correctness, security, and performance — not personal style.
- Approve only when all checklist items are satisfied.
- Request changes with specific, actionable comments.
