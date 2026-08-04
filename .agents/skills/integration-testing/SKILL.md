---
name: integration-testing
description: Use as the lead skill when testing backend behavior across databases, repositories, transactions, migrations, API flows, or multiple application components
---

# Backend Integration Testing

## Purpose

Guide tests that verify multiple backend components together. Use this as the lead skill when a real repository,
database, transaction boundary, migration, serializer, or API flow matters.

If the main risk is a race condition, lost update, worker interleaving, queue ordering, cancellation, or any other
concurrency anomaly, use `concurrency_fuzzing_testing` as the lead skill and use this skill for the database/API setup
details.

## When to Choose Integration Tests

Choose integration tests when:

- interactions between components need verification;
- database state, repositories, transactions, migrations, or serialization are part of the behavior;
- API behavior should be tested close to production;
- unit tests are too isolated to give confidence.

Use an isolated test database. Never point tests at production data or production infrastructure.

## Sociable Over Over-Mocked

For backend features, prefer sociable tests when they stay fast and understandable.

Sociable tests check several components together and mock only external boundaries. They are useful for:

- service behavior;
- API scenarios;
- business flows;
- real interaction between application components.

Use solitary tests for pure functions, complex algorithms, many edge cases, or code that is too expensive to run through
API/DB paths.

## What to Keep Real

Usually keep these real in integration tests:

- application services;
- repositories;
- database session and transaction handling;
- request/response serialization;
- migrations when migration behavior is under test;
- authorization and validation paths that affect the public outcome.

Do not directly test the database engine, SQL engine, framework internals, or third-party SDK internals.

## What to Mock

Mock external uncontrolled boundaries:

- outbound HTTP;
- SMTP;
- third-party APIs and SDKs;
- external brokers and queues;
- unstable filesystem access;
- time, randomness, and environment when deterministic behavior matters.

Avoid mocking internal repositories or services when a real test database would verify the behavior with better
confidence.

## API and E2E Scope

Use API/E2E tests for key public scenarios:

- critical user or API flow;
- behavior that must work through the public interface;
- business-critical path.

Keep full E2E tests few because they are slower, harder to maintain, and less precise at localizing failures.

For this product, prioritize flows that reduce dating-app burnout and improve meaningful offline outcomes, such as:

- transparent match explanation;
- respectful recommendation limits;
- intentional conversation flows;
- meeting-planning or safety-relevant flows.

Do not add E2E coverage for addictive engagement loops or artificial urgency mechanics.

## Database Isolation

Each integration test should:

- create the data it needs;
- not depend on execution order;
- isolate data with transactions, truncation, per-test schemas, or disposable databases;
- keep migrations and schema setup deterministic;
- avoid hidden cross-test state.

Slow tests often come from heavy database setup. Prefer shared infrastructure with per-test isolation over rebuilding
everything for every test, as long as isolation remains strong.

## Assertions

Assert through public effects:

- response body and status;
- persisted database state;
- emitted domain event;
- scheduled external call;
- externally visible error.

Avoid asserting internal method call counts, private helpers, or incidental SQL/query structure unless that structure is
the explicit contract.

## Handling Slow or Brittle Tests

If integration tests are slow:

- move pure logic to unit tests;
- reduce full E2E coverage;
- inspect database fixture setup;
- use transactions, rollback strategies, or disposable containers appropriately;
- keep benchmarks out of normal CI.

If integration tests are brittle:

- remove assertions on internal calls;
- assert public behavior through API/DB effects;
- reduce mocks on internal components;
- replace overly broad E2E tests with targeted integration tests.

If tests do not catch real bugs:

- add meaningful assertions;
- include negative scenarios;
- check business invariants;
- avoid status-code-only tests.

## Minimal Scenario Set

For a backend feature, start with:

- one happy path through the public interface;
- one important validation or permission failure;
- one missing/duplicate/invalid state case;
- one external dependency failure if the feature calls outside systems;
- one persistence or transaction assertion when state matters.

Add more only when the behavior or risk justifies it.

## Response Format

When proposing integration tests:

1. Name the public behavior under test.
2. Identify real components and mocked boundaries.
3. Describe database isolation.
4. Provide the minimal scenario list or test code.
