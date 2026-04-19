---
name: testing-test-strategy
description: Use as the lead skill when choosing what backend tests to write, reviewing test plans, or balancing unit, integration, API, concurrency, and E2E coverage
---

# Backend Test Strategy

## Purpose

Help an agent choose a valuable backend test suite. The goal is confidence, safe refactoring, and readable tests, not
maximum coverage.

Use this skill when the user asks to:

- choose a testing strategy;
- explain what tests are needed for a feature;
- review whether a test suite has the right balance;
- reduce fragile, slow, or low-value tests.

## Skill Routing

Choose the lead skill by the primary risk, then add supporting skills for tooling or workflow.

| User need | Lead skill | Supporting skills |
| --- | --- | --- |
| Decide what tests are needed | `testing-test-strategy` | `unit-testing`, `integration-testing`, `concurrency_fuzzing_testing`, `testing-pytest` |
| Isolated Python logic, validation, transformations, simple async function awaited once | `unit-testing` | `testing-pytest` |
| Real database, repository, transaction, migration, API flow, or multiple components | `integration-testing` | `testing-pytest` |
| Multiple workers/tasks/threads, `asyncio.Queue`, shared state, locks, cancellation, backpressure, lost updates, order-dependent failures | `concurrency_fuzzing_testing` | `integration-testing`, `testing-pytest` |
| Runnable pytest syntax, fixtures, parametrization, mocks, `pytest-httpx`, `dirty-equals` | the relevant level skill | `testing-pytest` |
| Production change should be test-first | the relevant level skill | `test-driven-development`, `testing-pytest` |

Async alone is not a concurrency-fuzzing signal. An async function with controlled dependencies and no competing task is
usually a unit test. Concurrency fuzzing becomes the lead when correctness depends on interleaving between concurrent
operations.

## Product Fit

For this project, tests should protect meaningful user outcomes and trust. Prefer tests that verify compatibility,
transparency, safety, and offline-meeting flows over tests that only defend internal plumbing.

Do not optimize test plans around engagement mechanics, gamified loops, or retention-only behavior.

## Agent Mindset

- Tests should verify behavior, not implementation details.
- Tests should support development, not exist solely for coverage metrics.
- A good test is understandable, independent, and resilient to refactoring.
- Prefer sociable tests when they give greater confidence at a reasonable cost.
- Use solitary/unit tests for pure functions, isolated complex logic, and many edge cases.
- Do not test components that do not belong to the application, such as the database engine, SQL engine, framework, or
  third-party SDK internals.
- Do not turn tests into a custom abstraction framework on top of pytest.

## Choosing Test Level

Before writing tests, identify the observable behavior and the smallest public interface that can verify it.

### Unit Tests

Choose unit tests when:

- a single unit of behavior is being verified;
- the code is fast and has no real I/O;
- the logic is pure or nearly pure;
- many edge cases need coverage.

A unit is a unit of behavior, not necessarily one class or function.

### Integration Tests

Choose integration tests when:

- interactions between components must be verified;
- repositories, transactions, migrations, serialization, or database state matter;
- behavior should be tested close to production;
- unit tests do not provide enough confidence.

Use an isolated test database. Never use production data or production infrastructure.

### API and E2E Tests

Choose API or E2E tests when:

- a key user or API scenario is verified end to end;
- the public interface is the important contract;
- the scenario is business-critical.

Keep E2E tests few. They are slower, costlier to maintain, and worse at localizing failures.

## Recommended Backend Balance

Use this as a default:

- unit tests for pure business logic, validation, calculations, and complex branching;
- integration tests for repositories, database behavior, transactions, and component interaction;
- API/E2E tests for key routes and business flows.

If a service has little isolated business logic, it is fine to have more integration/API tests and fewer unit tests.

## Coverage

Coverage is a signal, not a goal.

Judge tests by:

1. bug protection;
2. resistance to safe refactoring;
3. fast feedback;
4. maintenance cost.

A small suite that catches real regressions is better than 100% coverage made of brittle tests.

## Review Checklist

- [ ] Tests verify behavior, not implementation.
- [ ] Test names describe scenarios clearly.
- [ ] Arrange / Act / Assert is visible.
- [ ] Each test has one main Act.
- [ ] There are no hidden branches or `if` statements inside tests.
- [ ] Tests do not depend on execution order.
- [ ] Mocks are justified and limited to real boundaries.
- [ ] Important failures and edge cases are covered.
- [ ] Tests survive safe refactoring.
- [ ] Tests are fast enough for their level.
- [ ] Coverage is not the only reason a test exists.

## Response Format

When the user asks for a strategy:

1. Break the feature into observable behaviors.
2. Assign unit, integration, API, or E2E levels.
3. State what to mock and why.
4. Give the smallest useful scenario list.

When the user asks for a review:

1. Lead with the main risks.
2. Point out brittle or redundant tests.
3. Suggest a concrete restructuring.
4. Provide an improved example if helpful.

## Short Rule

Write more confidence, not more tests.

A test should answer: if this fails, did user-visible or business behavior actually break?
