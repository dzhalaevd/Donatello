---
name: concurrency_fuzzing_testing
description: Use as the lead skill when Python tests must expose scheduler/interleaving bugs in asyncio, threading, queues, workers, databases, caches, or mixed-concurrency code
---

# Concurrency Fuzzing Testing

## Purpose

Design fuzz tests that expose:

- race conditions;
- lost updates;
- dirty reads;
- write skew;
- order-dependent bugs;
- ABA-style anomalies;
- invariant violations;
- deadlocks, livelocks, hangs, and cancellation bugs;
- nondeterministic or flaky behavior caused by scheduling.

Use this skill as the lead skill when the primary risk is concurrent interleaving, not merely the presence of `async`
or `await`.

Strong signals:

- multiple `asyncio` tasks, threads, workers, greenlets, or processes operate at the same time;
- `asyncio.Queue`, worker pools, background consumers, schedulers, or fan-out/fan-in flows coordinate work;
- shared mutable state, database rows, caches, locks, semaphores, or global state are touched concurrently;
- a `read -> modify -> write` sequence can overlap with another operation;
- correctness depends on ordering, cancellation, timeout, backpressure, or task cleanup;
- the suspected failure is flaky, load-sensitive, order-dependent, or only appears under concurrent execution.

Do not choose this skill just because a function is async. If the behavior can be tested by awaiting one operation with
controlled fakes and no competing operation, use `unit-testing` as the lead skill.

## Relationship to Other Testing Skills

Use this skill as the lead when the core question is "can concurrent execution violate an invariant?"

Use `integration-testing` as a supporting skill when the race involves real databases, repositories, transactions, API
flows, or multiple application components.

Use `testing-pytest` as a supporting skill when implementing the final tests in pytest.

Use `unit-testing` instead when the target behavior can be isolated without real concurrency.

Use `test-driven-development` as a workflow overlay when the concurrency bug is being fixed test-first.

Concurrency fuzzing is heavier than normal unit or integration testing. Start small, then escalate only when the risk
justifies it.

## Codebase Analysis

Before writing fuzz tests, inspect the code step by step and identify:

- shared mutable state: `dict`, `list`, object attributes, database rows, caches, globals;
- `read -> modify -> write` sequences without atomicity;
- `await` points between read and write;
- global variables and class attributes;
- external services with stateful behavior;
- transaction boundaries and isolation levels;
- lock usage: `Lock`, `RLock`, `Semaphore`, `asyncio.Lock`, DB locks, advisory locks;
- critical sections where concurrent modification can happen.

Ask concise questions if it is unclear:

- which operations can run concurrently;
- what state must remain consistent;
- which synchronization primitives are expected;
- whether sequential execution defines the valid final states;
- which tests are allowed in PR CI, nightly CI, or local-only suites.

If ambiguity does not block progress, state assumptions and continue.

## Invariants First

Define invariants before choosing the fuzzer.

Useful invariant categories:

- conservation: sum of balances remains constant;
- uniqueness: only one active match, token, reservation, or username;
- monotonicity: counters, versions, timestamps, sequence numbers never move backward;
- idempotency: repeated operation has the same final state;
- serializability: concurrent final state equals one of the valid sequential final states;
- no lost updates: N successful increments produce N durable effects;
- visibility: published state matches persisted state;
- safety: blocked, deleted, or unauthorized entities cannot be acted on.

Prefer invariant assertions over one brittle exact value when the exact interleaving can vary.

## Choosing a Fuzzing Approach

### 1. Random / Monte Carlo Fuzzing

Use first. It is simple and often catches obvious races.

Techniques:

- run the same scenario many times;
- use `asyncio.gather`, threads, or process-level concurrency;
- add small randomized delays at controlled boundaries;
- vary operation order and inputs;
- record failure rate.

Good for:

- quick risk probes;
- reproducing suspected races;
- PR-friendly smoke checks with a small iteration count.

Limitations:

- no guarantee;
- can be slow;
- may be hard to reproduce without seed and trace capture.

### 2. Scheduler or Event Loop Fuzzing

Use when normal repeated runs do not create enough scheduling variation.

Techniques:

- randomize ready callback order in an isolated test event loop;
- inject yields at known context-switch points;
- use a custom event loop policy only inside the test;
- consider Trio for code that can run under Trio, because scheduling order is intentionally less deterministic.

Treat event loop patching as advanced and risky. Keep it isolated, documented, and out of broad test fixtures.

### 3. Systematic Interleaving Exploration

Use for small, high-value scenarios where stronger confidence is needed.

Model the concurrent operations as a tree of possible interleavings. Pause at interesting operations, choose the next
runnable operation, mark the path visited, and repeat until all reachable paths are explored.

Good hook points:

- SQLAlchemy `before_execute` / `before_cursor_execute`;
- repository calls;
- cache read/write methods;
- lock acquisition/release wrappers;
- explicit test-only scheduler yield points;
- outbound service mock calls.

Requirements:

- deterministic code for a deterministic operation order;
- small operation count;
- stable snapshot/reset mechanism;
- trace recording for each explored path.

This can provide near-guarantees for bounded scenarios, but it is too expensive for broad API surfaces.

### 4. Property-Based Concurrency Fuzzing

Use Hypothesis or a similar tool when inputs or operation sequences matter.

Generate:

- operation sequences;
- operation parameters;
- initial states;
- timing decisions;
- concurrency groups.

Assert post-conditions and invariants that must hold for every generated case.

Best when sequential behavior is well specified and concurrent behavior should be equivalent to some valid serial order.

### 5. Input and State Fuzzing

Use as a supplement to concurrency fuzzing.

Tools may include Hypothesis, Atheris, pythonfuzz, or pydantic validation strategies.

Target:

- boundary values;
- invalid payloads;
- malformed states;
- unusual ordering of valid operations;
- state transitions near policy limits.

## General Rules

- Make failing runs reproducible with a seed.
- Capture seed, iteration, operation order, task names, and interleaving trace.
- Keep the minimal scenario that can catch the race.
- Use timeouts for every concurrent run.
- Do not let background tasks leak after the test.
- Avoid real sleeps when a controllable scheduler or injected sleeper is possible.
- Test both normal load and intentionally race-prone conditions.
- Separate fast PR tests from heavy nightly or local stress tests.
- Prefer deterministic reset/snapshot over cleanup-by-hope.
- Never use production data or production infrastructure.

## Basic Async Template

```python
async def test_operation_concurrent_fuzz() -> None:
    seed = 12345
    rng = random.Random(seed)

    for iteration in range(100):
        await reset_state()
        trace: list[str] = []

        async with fuzzing_context(rng=rng, trace=trace):
            await asyncio.wait_for(
                asyncio.gather(
                    operation_a(...),
                    operation_b(...),
                ),
                timeout=1.0,
            )

        assert_invariants_hold(), {
            "seed": seed,
            "iteration": iteration,
            "trace": trace,
        }
```

Use fewer iterations in PR CI and more in nightly CI.

## Lost Update Probe

Use this pattern when two or more operations update the same logical value.

```python
async def test_increment_has_no_lost_updates_under_concurrency() -> None:
    seed = 7357
    attempts = 200
    rng = random.Random(seed)

    for iteration in range(attempts):
        await set_counter("foo", 0)
        trace: list[str] = []

        async def worker(name: str) -> None:
            trace.append(f"{name}:start")
            await maybe_yield(rng)
            await increment("foo")
            trace.append(f"{name}:done")

        await asyncio.wait_for(
            asyncio.gather(worker("a"), worker("b")),
            timeout=1.0,
        )

        assert await get_counter("foo") == 2, {
            "seed": seed,
            "iteration": iteration,
            "trace": trace,
        }
```

If this test is flaky, do not hide the flakiness. Capture the failing seed and turn it into a deterministic regression
when possible.

## Event Loop Fuzzing Guidance

Randomizing `asyncio` internals can reveal bugs, but it is fragile.

If used:

- isolate it to one test module or fixture;
- restore the normal event loop policy after use;
- document Python-version assumptions;
- keep the code small;
- use it as a diagnostic or nightly technique unless it is stable in CI.

Sketch:

```python
class RandomReadyQueue(deque[asyncio.Handle]):
    def __init__(self, rng: random.Random) -> None:
        super().__init__()
        self._rng = rng

    def popleft(self) -> asyncio.Handle:
        self._rng.shuffle(self)
        return super().popleft()
```

Do not patch global scheduler behavior for unrelated tests.

## Systematic Interleaving Guidance

For bounded exhaustive exploration:

1. Select the small set of operations that may race.
2. Add hooks at the operations that define interleaving points.
3. Pause an operation at a hook and wait briefly for a competing operation.
4. Add available operations to the current tree node.
5. Choose the next unexplored child.
6. Execute it and continue.
7. Reset state and repeat until the tree is explored.

Record:

- operation identity;
- task/thread name;
- hook name;
- query or logical operation;
- chosen branch;
- final state snapshot.

Use this for high-risk, low-dimensional cases. Do not attempt exhaustive exploration over unbounded API/state spaces.

## Database Concurrency

When the bug may involve the database:

- use an isolated test database;
- define transaction boundaries explicitly;
- know the isolation level;
- capture final database state snapshots;
- consider SQLAlchemy events such as `before_execute` or `before_cursor_execute`;
- test sequential valid states and compare concurrent final states against them.

Serializability-style check:

1. Start from initial state `S1`.
2. Run `op1` then `op2`; snapshot end state.
3. Reset to `S1`.
4. Run `op2` then `op1`; snapshot end state.
5. Reset to `S1`.
6. Run `op1` and `op2` concurrently under fuzzing.
7. Assert the concurrent final state equals one of the sequential final states, unless the domain explicitly allows
   another state.

## Threading Guidance

For `threading` code:

- use barriers to align competing operations;
- use events to pause at known points;
- run with enough iterations to vary scheduling;
- protect tests with timeouts;
- capture thread names and operation order;
- avoid relying on CPython GIL behavior as a correctness guarantee.

## Hypothesis Guidance

When using Hypothesis:

- generate small operation sequences first;
- keep deadlines realistic or disable them for concurrency tests;
- print or attach the seed and example;
- assert invariants after each sequence or at the end;
- shrink failing cases into deterministic regression tests when practical.

Do not combine huge input spaces with huge interleaving spaces in one test. Control one dimension at a time.

## CI Strategy

Classify tests by cost:

- PR smoke: small seeds, low iteration counts, strict timeout.
- Nightly fuzz: many seeds, high iteration counts, scheduler fuzzing.
- Diagnostic/manual: systematic interleaving, heavy DB exploration, custom event loop patching.

Report the intended tier when proposing a test.

## Failure Reporting

On failure, output enough to reproduce:

- seed;
- iteration;
- operation names and parameters;
- task/thread names;
- interleaving trace;
- initial state snapshot;
- final state snapshot;
- expected invariant or valid sequential states.

Do not report only "race detected"; include the shortest actionable trace available.

## Response Format

When designing concurrency fuzz tests:

1. Identify suspected race points and shared state.
2. Define invariants.
3. Choose fuzzing approach and CI tier.
4. Provide complete test code or precise pseudocode.
5. Explain seed/reproducibility and trace capture.
6. State limitations and when to escalate to heavier techniques.

When reviewing concurrency tests:

1. Lead with missing race coverage or false confidence risks.
2. Check reproducibility, timeout handling, and cleanup.
3. Check that assertions verify invariants, not incidental timing.
4. Suggest a smaller deterministic regression for any known failure trace.
