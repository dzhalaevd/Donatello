---
name: test-driven-development
description: Use as a workflow overlay when implementing any feature, bugfix, refactor, or behavior change before writing production code
---

# Test-Driven Development

## Purpose

Use TDD to clarify desired behavior before changing production code. The point is confidence and better design, not
ritual for its own sake.

TDD is a workflow overlay, not a replacement for choosing the right test level. Combine it with:

- `unit-testing` for isolated behavior;
- `integration-testing` for database/API/multi-component behavior;
- `concurrency-fuzzing-testing` for race-condition or interleaving bugs;
- `testing-pytest` for pytest implementation details.

## When to Use

Use this skill for:

- new features;
- bug fixes;
- refactoring that changes structure but should preserve behavior;
- any behavior change.

Ask the user before skipping TDD for throwaway prototypes, generated code, or pure configuration.

## Core Rule

Write the failing test first. Watch it fail for the expected reason. Then write the smallest production change that
makes it pass.

If a test passes immediately, it did not prove the new behavior. Fix the test or choose a behavior that is not already
covered.

## Red / Green / Refactor

### 1. Red

Write one small test for the next observable behavior.

```python
def test_rejects_empty_email(client: Client) -> None:
    response = client.post("/api/users", json={"email": "", "name": "Ada"})

    assert response.status_code == 422
    assert response.json()["detail"]
```

Run only the relevant test first:

```bash
pytest path/to/test_file.py::test_rejects_empty_email
```

Confirm:

- the test fails;
- the failure is expected;
- it fails because the behavior is missing, not because of a typo, fixture error, or bad setup.

### 2. Green

Write the minimal production code to pass the test.

Do not add extra options, unrelated refactors, or future behavior. If the next requirement matters, write the next
failing test for it.

Run the focused test again, then the relevant nearby test set.

### 3. Refactor

Only after green:

- remove duplication;
- improve names;
- simplify structure;
- extract helpers if they reduce real noise.

Keep the tests green during refactoring.

## Bug Fix Workflow

For a bug:

1. Write a failing test that reproduces the bug.
2. Confirm the test fails on current code.
3. Fix the bug with the smallest change.
4. Confirm the new test and related tests pass.
5. Keep the regression test.

Never fix a backend bug only by manual verification when an automated regression test can reasonably cover it.

## Good TDD Tests

A useful first test:

- names the behavior clearly;
- uses the public interface;
- has one main Act;
- asserts a meaningful public result;
- mocks only external uncontrolled dependencies;
- is small enough to fail for one clear reason.

Avoid first tests that:

- assert private methods or internal call counts;
- check implementation details before behavior;
- require a huge fixture setup;
- use broad mocks that make the test pass without executing real code.

## Existing Code

When changing untested existing code:

1. Add a characterization test for current behavior if needed.
2. Add a failing test for the desired new behavior.
3. Change production code.
4. Refactor only with tests passing.

If the existing design is hard to test, let that inform the design. Prefer simpler public interfaces and dependency
boundaries over heavier test machinery.

## When Stuck

If you do not know how to test the behavior:

- write the assertion first;
- describe the wished-for public API;
- reduce the behavior to one smaller case;
- ask the user for the intended behavior if the product decision is unclear.

If the test setup is huge, consider whether the behavior belongs in a smaller unit test or whether the production design
is too coupled.

## Completion Checklist

Before marking TDD work complete:

- [ ] Each behavior change has a test.
- [ ] The test was run and failed before implementation.
- [ ] The failure reason was expected.
- [ ] The production change was minimal.
- [ ] Focused tests pass.
- [ ] Relevant surrounding tests pass.
- [ ] Tests verify public behavior rather than internals.

## Response Format

When reporting TDD work:

1. Name the failing test that was added.
2. Say what failure it produced before implementation.
3. Summarize the production change.
4. List the verification commands and results.
