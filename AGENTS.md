# AGENTS.md

This file contains repository-specific instructions for coding agents. It applies to the entire repository unless a
more specific `AGENTS.md` exists in a subdirectory.

## Load Context Selectively

Read only the documents relevant to the task:

| Task concerns | Canonical document |
|---|---|
| Product problem, audience, or intended outcome | [`arch/product/vision.md`](arch/product/vision.md) |
| Product beliefs and value judgments | [`arch/product/philosophy.md`](arch/product/philosophy.md) |
| Product decision rules and guardrails | [`arch/product/principles.md`](arch/product/principles.md) |
| Research findings and evidence limits | [`arch/product/research.md`](arch/product/research.md) |
| Domain terminology | [`arch/product/glossary.md`](arch/product/glossary.md) |
| System structure, runtime relationships, data ownership, or known technical gaps | [`ARCHITECTURE.md`](ARCHITECTURE.md) |
| Local setup and environment variables | [`DEVELOPMENT.md`](DEVELOPMENT.md) |
| Available repository commands | [`Makefile`](Makefile) |

Before changing a domain concept, read the glossary and relevant product document. Before changing a technical seam,
runtime process, persistence path, or external integration, read the architecture document and relevant source files.

The codebase is in transition. Prefer current source code, dependency manifests, migrations, and executable
configuration over documentation when they disagree, then update the stale document in the same change.

## Working Rules

- Preserve existing user changes. The worktree may already be dirty; do not revert, overwrite, stage, or reformat
  unrelated files.
- Keep changes scoped to the requested application area. Do not couple `backend`, `tgbot`, and `front` merely to reuse a
  small implementation detail.
- Read the files being changed, their tests, and one relevant existing pattern before implementation.
- Add or update tests for behavior changes. For a bug fix, reproduce the bug with a failing test first when practical.
- Do not commit secrets or real credentials. `.env` files are local-only; use placeholders in documentation and
  fixtures.
- Do not change a database schema without an Alembic migration. Inspect existing migrations before choosing revision
  dependencies or naming conventions.
- Keep public HTTP behavior backward-compatible unless the task explicitly changes the contract.
- Do not add personal data, tokens, message text, user IDs, chat IDs, or unbounded values as metric or log labels.
- Report checks that could not run and the concrete reason. Never describe an unexecuted check as passing.

## Backend Work

- Use Python 3.13 and the isolated `backend` uv environment.
- Follow the dependency direction and module seams documented in
  [`ARCHITECTURE.md`](ARCHITECTURE.md#architectural-style).
- Keep REST controllers thin: validate and translate HTTP data, invoke an application operation, and translate the
  result.
- Do not put SQLAlchemy queries, provider-specific token logic, or business decisions in controllers.
- Obtain application dependencies through Dishka providers rather than constructing sessions or collaborators in
  controllers.
- Keep transaction ownership explicit through the application operation and unit-of-work/session seam.

Use the root Makefile:

```bash
make install-backend
make run-backend
make test-backend
make verify-backend
```

The backend has no configured type checker. Do not borrow one from the Telegram environment or invent a
`typecheck-backend` check.

Backend pytest imports `tests.fixtures.db` as a plugin. If collection cannot resolve `tests`, diagnose the package and
test-path setup instead of weakening discovery or hiding the import error.

## Telegram Bot Work

- Use Python 3.13 and the isolated `tgbot` uv environment.
- Keep handlers focused on Telegram interaction and delegate reusable behavior to application-facing modules.
- Do not perform network calls at module import time.
- Preserve polling and webhook startup modes unless the task explicitly removes one.
- Do not run polling and webhook consumption for the same bot token simultaneously.

Use the root Makefile:

```bash
make install-tgbot
make run-tgbot-polling
make run-tgbot-webhook
make test-tgbot
make verify-tgbot
```

Some end-to-end tests require Telegram credentials and network access. Never substitute real credentials or claim those
tests passed when the required environment is unavailable.

## Frontend Work

- Use TypeScript for application code and keep React components focused.
- Consume backend behavior through documented HTTP contracts; do not reproduce product rules in browser-only state.
- Prefer the existing ESLint and TypeScript configuration over introducing new formatting or state-management tools.
- Do not edit generated dependencies under `front/node_modules`.

Use the root Makefile:

```bash
make install-front
make run-front
make lint-front
make typecheck-front
make build-front
make verify-front
```

There is no frontend test script; `test-front` is intentionally absent.

## Repository Checks

Use the compositional root targets:

```bash
make lint
make format
make format-check
make typecheck
make test
make verify
```

The Makefile runs tools through each application's environment. Do not rely on globally installed Ruff, Flake8, pytest,
mypy, ESLint, or TypeScript executables.

Fix applicable violations in code. Change lint configuration only when a rule conflicts with a repository-wide design
choice, and document that reason in the configuration. Run the smallest relevant checks first, then `verify` targets for
every application area modified.

## Local Infrastructure Safety

Use `make infra-up`, `make infra-logs`, and `make infra-down`. Starting containers is unnecessary for isolated unit
tests. Do not modify, reset, or delete local database volumes unless the user explicitly requests it.

The backend and Telegram webhook app both default to port 8000. Change one port before running both on the same host.

## Documentation Rules

- Update setup documentation when environment variables or operator workflows change.
- Update `ARCHITECTURE.md` when runtime relationships, module seams, data ownership, external systems, or known gaps
  change.
- Update the one owning product document when product meaning changes; link to it instead of copying its claims.
- Keep examples copy-pasteable and use repository-relative paths in documentation.
- Record hard-to-reverse, surprising technical trade-offs as ADRs under `arch/adr/`; do not use ADRs for routine changes.
- Explain non-obvious implementation constraints close to the code, but do not bury product or architectural decisions
  in comments.
