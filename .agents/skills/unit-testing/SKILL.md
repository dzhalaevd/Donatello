---
name: unit-testing
description: Use as the lead skill when designing, writing, or reviewing focused unit tests for isolated Python behavior without real I/O or competing concurrent operations
---

# Python Unit Testing

## Purpose

Act as a senior Python developer designing a comprehensive, maintainable unit test suite for a provided codebase.

The goal is not to maximize the number of tests. The goal is to verify small units of behavior with fast, isolated,
readable tests that make regressions obvious.

Use this skill when the user asks to:

- write unit tests for Python code;
- review unit-test quality;
- identify missing unit-test scenarios;
- design tool-agnostic test cases;
- isolate Python code from external dependencies during tests.

## Relationship to Other Testing Skills

Use this skill as the lead skill for isolated behavior and pure or near-pure Python logic.

Use `testing-test-strategy` first when the user asks which test levels are needed.

Use `testing-pytest` as a supporting skill when the user wants runnable pytest implementation details.

Use `integration-testing` as the lead skill when real databases, repositories, API flows, transactions, or multiple
components must be tested together.

Use `concurrency_fuzzing_testing` as the lead skill when the risk is a scheduler/interleaving bug: multiple tasks,
threads, workers, queues, locks, shared mutable state, or `read -> modify -> write` behavior that can run concurrently.
Plain async code is not enough to choose concurrency fuzzing. If an async function can be tested by awaiting it with
controlled fakes and no competing operation, keep `unit-testing` as the lead skill.

Use `test-driven-development` when implementation should be driven by a failing test first.

## Codebase Understanding

Before writing tests, analyze the Python code step by step:

1. Identify the unit of behavior, not merely the class or function name.
2. Identify the public interface used to observe that behavior.
3. Read input types, return types, exceptions, side effects, and invariants.
4. Identify dependencies:
    - internal controlled collaborators;
    - external uncontrolled dependencies;
    - time, randomness, environment, filesystem, network, or process state.
5. Identify ambiguous or missing information:
    - constants;
    - type definitions;
    - valid ranges;
    - external API contracts;
    - error semantics;
    - concurrency or async expectations.
6. Decide whether ambiguity blocks correct test design.

If ambiguity blocks correctness, ask concise clarification questions before inventing behavior. If it does not block
progress, state assumptions and continue.

## Framework-Agnostic First

When the user asks for abstract or conceptual unit tests, describe tests using framework-neutral structure instead of
naming pytest, unittest, or another specific tool.

Use generic terms:

- `test`;
- `assert`;
- `fake`;
- `stub`;
- `mock`;
- `setup`;
- `teardown`.

When the user asks for runnable tests in this repository, follow the project's actual framework and conventions while
preserving these unit-testing principles.

## What Counts as a Unit Test

A unit test verifies one small behavior quickly and in isolation.

Good unit-test targets:

- pure functions;
- validation logic;
- value objects and domain rules;
- branch-heavy business logic;
- data transformation;
- error mapping;
- retry/backoff decision logic without real sleeping;
- async control flow with dependencies replaced.

Poor unit-test targets:

- database engine behavior;
- framework internals;
- third-party SDK behavior;
- real network calls;
- broad API flows;
- multi-component persistence behavior.

Those usually belong in integration tests.

## Small, Focused Tests

Each unit test should:

- verify one behavior;
- have one main Act;
- be independent of every other test;
- be deterministic;
- use explicit inputs;
- assert an observable result;
- avoid real I/O;
- avoid loops and conditionals inside the test.

If a test name contains "and", consider splitting it.

## Arrange / Act / Assert

Use AAA in every test:

```python
def test_normalizes_email_before_comparison() -> None:
    # Arrange
    user_email = "Ada@Example.COM "
    candidate_email = "ada@example.com"
    matcher = EmailMatcher()

    # Act
    result = matcher.matches(user_email, candidate_email)

    # Assert
    assert result is True
```

Keep Arrange readable. Do not hide meaningful business setup in a helper unless the helper name makes the setup obvious.

## Naming

Test names should describe behavior in domain language.

Good:

```python
def test_rejects_message_when_recipient_has_blocked_sender() -> None: ...


def test_returns_empty_recommendations_when_daily_limit_is_reached() -> None: ...


def test_keeps_original_score_when_explanation_data_is_missing() -> None: ...
```

Bad:

```python
def test_case_1() -> None: ...


def test_validator_works() -> None: ...


def test_returns_false() -> None: ...
```

## Dependencies and Test Doubles

Replace external uncontrolled dependencies with test doubles:

- use a fake for simple in-memory behavior;
- use a stub for fixed return values;
- use a mock for verifying an interaction at a true boundary;
- use a spy only when the interaction itself is part of the contract.

Prefer fakes and stubs over mocks when possible. They usually make tests less brittle.

Mock external boundaries such as:

- HTTP clients;
- SMTP/email sender;
- third-party APIs;
- filesystem access when not under test;
- time providers;
- random generators;
- environment variables.

Do not mock private methods or internal implementation details. If a test requires many mocks, the unit may be too
coupled or too large.

## Happy Paths, Failure Modes, and Boundaries

For each meaningful behavior, cover:

- the happy path;
- invalid input;
- missing or empty values;
- boundary values;
- duplicate or conflicting data;
- dependency failure;
- permission or policy denial when relevant;
- async cancellation or timeout when relevant.

Choose representative equivalence classes instead of every possible combination.

## Python Types

Use Python's type system to improve tests:

- keep test data consistent with type hints;
- assert precise return types when they are part of the contract;
- use typed fakes and fixtures where practical;
- include `None`, empty collections, and invalid enum/literal values when the type contract allows or rejects them.

If type hints and runtime behavior disagree, call that out.

## Async Code

For async Python code:

- await the unit under test;
- replace async dependencies with async fakes or stubs;
- test success and failure paths;
- test timeout, cancellation, or retry decisions when they are part of the behavior;
- do not leave background tasks unobserved;
- avoid real sleeping; inject a clock or sleeper instead.

Valid Python async example:

```python
async def test_returns_fallback_when_profile_service_times_out() -> None:
    # Arrange
    profile_service = StubProfileService(timeout=True)
    recommender = Recommender(profile_service=profile_service)

    # Act
    result = await recommender.recommend_for(user_id)

    # Assert
    assert result == []
```

## Avoid Logic in Tests

Tests should be simple examples, not alternative implementations.

Avoid:

- `if` statements;
- loops over many cases unless expressed as clear named scenarios;
- computed expected values that duplicate production logic;
- broad helper frameworks;
- assertions that only check "no exception".

Expected values should usually be explicit.

## Complete Test Cases

Do not provide skeletons when the user asks for tests.

A complete unit test includes:

- concrete input data;
- all required test doubles;
- the action under test;
- meaningful assertions;
- failure-path assertions where applicable.

If repository context is missing, provide a complete framework-neutral test design and list the exact assumptions or
questions needed to convert it into runnable code.

## Review Checklist

- [ ] The test verifies one behavior.
- [ ] The test uses AAA.
- [ ] The name explains the scenario.
- [ ] The test is independent and deterministic.
- [ ] There is no real network, database, or filesystem access unless that is the explicit unit.
- [ ] External dependencies are replaced with appropriate doubles.
- [ ] Mocks do not assert private implementation details.
- [ ] Happy path and meaningful failure modes are covered.
- [ ] Boundary cases are represented.
- [ ] Async behavior is awaited and deterministic.
- [ ] Types and runtime expectations agree.
- [ ] The test is complete, not a placeholder.

## Response Format

When writing unit tests:

1. Summarize the unit of behavior being tested.
2. State assumptions or blocking questions.
3. Provide complete tests or framework-neutral test cases.
4. Explain which dependencies are doubled and why.
5. List missing edge cases or integration scenarios separately.

When reviewing unit tests:

1. Lead with the highest-risk issues.
2. Identify tests that are too broad, too mocked, or implementation-bound.
3. Suggest focused replacements.
4. Provide a corrected example when useful.
