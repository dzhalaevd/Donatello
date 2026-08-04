---
name: testing-pytest
description: Use as a supporting skill when the test level is known and the implementation should use pytest, fixtures, parametrization, mocks, dirty-equals, pytest-httpx, coverage, benchmark, or Allure
---

# Pytest Backend Testing

## Purpose

Guide to concrete pytest implementation for backend services.

Use this as a supporting/tooling skill after the lead testing skill is known:

- `unit-testing` leads isolated Python behavior;
- `integration-testing` leads database, repository, transaction, API, and multi-component behavior;
- `concurrency_fuzzing_testing` leads scheduler/interleaving/race-condition behavior;
- `testing-test-strategy` leads broad test planning;
- `test-driven-development` leads the test-first workflow.

If the user simply asks for "pytest tests" and the level is unclear, first infer or state the lead level, then use this
skill for pytest-specific syntax and fixtures.

## Test Writing Algorithm

1. Define the observable behavior.
2. Choose the smallest public interface that verifies it.
3. Identify dependencies:
    - controlled internal dependencies;
    - uncontrolled external dependencies.
4. Mock only uncontrolled external dependencies.
5. Prepare data explicitly.
6. Perform one main action.
7. Assert through a public effect:
    - API response;
    - database state;
    - return value;
    - published event;
    - external service call.
8. Ensure the test is independent.
9. Check that the test is not tied to incidental implementation details.

## Arrange / Act / Assert

Write tests using AAA:

```python
def test_create_user_fails_when_email_already_exists(client: Client) -> None:
    # Arrange
    client.post("/api/users", json={"name": "John", "email": "john@example.com"})

    # Act
    response = client.post(
        "/api/users",
        json={"name": "John2", "email": "john@example.com"},
    )

    # Assert
    assert response.status_code == 409
    assert "already exists" in response.json()["message"].lower()
```

Rules:

- one test has one main Act;
- avoid `Act -> Assert -> Act -> Assert` unless it is one coherent scenario;
- do not use `if` inside tests;
- do not hide important setup in unclear helpers;
- a huge Arrange often signals the test or code design should be simplified.

## Naming

Name tests in domain language.

Good:

```python
def test_create_user_fails_when_email_already_exists() -> None: ...
```

Bad:

```python
def test_create_user_409_case_2() -> None: ...
```

Prefer clarity over a rigid naming scheme.

## Mocking

Mock external uncontrolled dependencies:

- external HTTP;
- SMTP;
- third-party APIs and SDKs;
- external brokers and queues;
- filesystem access when it is not the subject of the test;
- unstable time, randomness, and environment sources.

Do not mock by default:

- internal application services;
- repositories when a test database gives better confidence;
- the database as a controlled dependency;
- cache controlled entirely by the service;
- private methods;
- internal calls that are not part of the public contract.

Mocking internal implementation often makes tests brittle.

When creating mocks, prefer specs:

```python
from unittest.mock import Mock, create_autospec

email_sender_mock = Mock(spec=EmailSender)
repository_mock = create_autospec(UserRepository)
```

Specs catch typos, wrong attributes, bad signatures, and contract drift.

## Public Behavior

Avoid asserting internals:

```python
def test_user_creation_internals(client, user_repository_mock, db_session) -> None:
    response = client.post("/api/users", json={"name": "John", "email": "john@example.com"})

    assert response.status_code == 201
    assert db_session.execute.call_count == 2
    user_repository_mock.create.assert_called_once()
```

Prefer public effects:

```python
from dirty_equals import IsDatetime, IsInt


def test_create_user_successfully(client, email_service_mock) -> None:
    email_service_mock.send_welcome_email.return_value = True

    response = client.post(
        "/api/users",
        json={"name": "John", "email": "john@example.com"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": IsInt,
        "name": "John",
        "email": "john@example.com",
        "created_at": IsDatetime,
        "updated_at": IsDatetime,
    }
    email_service_mock.send_welcome_email.assert_called_once()
```

## DAMP Over Excessive DRY

In tests, readability matters more than removing every duplicate line.

Prefer DAMP: Descriptive And Meaningful Phrases.

Small duplication is acceptable when it makes the scenario obvious. Do not build complex helper classes or factories
that hide the business meaning.

A helper is useful when it is:

- short;
- typed;
- not hiding important business logic;
- reducing noise rather than meaning;
- reused by many similar tests.

## Independence

Each test should:

- prepare its own data;
- not depend on execution order;
- avoid global mutable state;
- not rely on data created by another test;
- isolate or clean up side effects.

Bad:

```python
created_user_id = None


def test_create_user(client) -> None:
    global created_user_id
    created_user_id = client.post("/api/users", json={...}).json()["id"]


def test_get_user(client) -> None:
    response = client.get(f"/api/users/{created_user_id}")
    assert response.status_code == 200
```

Good:

```python
def test_get_user(client) -> None:
    create_response = client.post(
        "/api/users",
        json={"name": "John", "email": "john@example.com"},
    )
    user_id = create_response.json()["id"]

    response = client.get(f"/api/users/{user_id}")

    assert response.status_code == 200
```

## Fixtures

Use fixtures for infrastructure and repeated preparation:

- test client;
- test DB/session;
- external service mocks;
- test data factories;
- environment settings.

Rules:

- type fixtures;
- avoid magical fixtures;
- do not create data in a fixture unless the fixture name makes that obvious;
- keep important Arrange visible;
- keep wrapper fixtures simple and local.

Typed factory example:

```python
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(slots=True)
class User:
    id: int | None
    name: str
    email: str


UserFactory = Callable[..., User]
```

## Parametrization

Use `pytest.mark.parametrize` for meaningful scenarios:

```python
import pytest


@pytest.mark.parametrize(
    ("email", "expected_status"),
    [
        ("john@example.com", 201),
        ("invalid-email", 422),
        ("", 422),
    ],
)
def test_create_user_email_validation(client, email: str, expected_status: int) -> None:
    response = client.post("/api/users", json={"name": "John", "email": email})

    assert response.status_code == expected_status
```

Avoid combinatorial explosions. Parametrize important equivalence classes, not every possible combination.

## Errors and Edge Cases

Do not stop at happy paths. Check:

- invalid input;
- duplicates;
- empty lists;
- missing entities;
- permissions;
- idempotency when relevant;
- external service timeouts and failures;
- boundary values;
- meaningful concurrency scenarios.

## dirty-equals

Use `dirty-equals` for complex structures with dynamic values:

```python
from dirty_equals import IsDatetime, IsInt, IsRegex

assert response.json() == {
    "id": IsInt,
    "email": "john@example.com",
    "created_at": IsDatetime,
    "request_id": IsRegex(r"^[a-f0-9-]{36}$"),
}
```

This is clearer than many tiny asserts for datetime formats, regexes, and types.

## External HTTP

For `httpx` code, use `pytest-httpx`:

```python
def test_get_user_from_external_api(httpx_mock) -> None:
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/users/42",
        json={"id": 42, "name": "Ada"},
        status_code=200,
    )

    result = get_user(42)

    assert result == {"id": 42, "name": "Ada"}
```

For a large external API, create a thin mocker:

```python
class ExternalApiMocker:
    def __init__(self, httpx_mock) -> None:
        self._httpx_mock = httpx_mock

    def add_user_response(self, user_id: int, name: str) -> None:
        self._httpx_mock.add_response(
            method="GET",
            url=f"https://api.example.com/users/{user_id}",
            json={"id": user_id, "name": name},
        )
```

The wrapper should simplify tests, not become another framework.

## Benchmark Tests

For benchmark tests, `pytest-benchmark` is acceptable.

Recommended config:

```toml
[tool.pytest.ini_options]
addopts = "--benchmark-skip"
python_functions = ["test_*", "bench_*"]
```

Normal tests should run in CI by default. Benchmarks should be explicit.

## Allure

If the project uses Allure, add human-readable titles to important tests:

```python
import allure


@allure.title("User cannot register with an already used email")
def test_create_user_fails_when_email_already_exists(client) -> None: ...
```

Do not duplicate obvious descriptions for every small unit test.

## Response Format

When writing tests:

1. Briefly explain the chosen test level.
2. Provide the test code.
3. State what is mocked and why.
4. Mention useful edge cases that remain.
