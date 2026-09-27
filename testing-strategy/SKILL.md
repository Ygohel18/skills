---
name: testing-strategy
description: >
  Language-agnostic framework for designing, structuring, and evaluating automated test suites.
  Triggers whenever an agent is asked to "write tests for this", "what should I test?", "is this well tested?",
  "how much test coverage do I need?", "this test is flaky", or when debating unit vs integration vs e2e tests.
  Enforces the test pyramid, behavior-driven testing over implementation details, strict mocking discipline,
  root-cause resolution for flaky tests, and using coverage as a risk signal rather than a vanity metric.
metadata:
  author: yash
  version: "1.0"
  scope: "testing-strategy, test-pyramid, unit-testing, integration-testing, flaky-test-debugging"
allowed-tools: Read Write Bash
---

# Testing Strategy & Architecture

A language-agnostic operational standard for deciding what to test, how much to test, and at which layer of the test pyramid.

> **Sibling Standards:**
> - For general test writing guidelines, see [`universal-coding-standards`](file:///Users/apple/Projects/yash/skills/universal-coding-standards/SKILL.md#5-testing--verification).
> - For evaluating test adequacy during code review, see [`code-review`](file:///Users/apple/Projects/yash/skills/code-review/SKILL.md#32-test-adequacy).

---

## 1. Test Pyramid & Level Selection

Select the right test level based on execution cost and isolation needs:

```text
       ▲
      / \        E2E Tests (~5-10%)
     /   \       Full user-journey through real UI/stack. Slow, expensive, high-confidence.
    /-----\
   /       \     Integration Tests (~20-30%)
  /         \    Verify 2+ real components interacting (Real DB, API contracts).
 /-----------\
/             \  Unit Tests (~60-70%)
/_______________\ Isolated functions, math, pure logic, fast in-memory execution.
```

### Level Definitions:
1. **Unit Tests:**
   - **Scope:** Verifies a single isolated function, class, or domain entity.
   - **Dependencies:** Mock out external slow boundaries (network, filesystem, time).
   - **Speed:** Milliseconds. Can run thousands on every file save.
2. **Integration Tests:**
   - **Scope:** Verifies the real interaction between two or more components (e.g., repository layer against a real test database, serialization over HTTP).
   - **Dependencies:** Use lightweight real dependencies (Testcontainers, in-memory SQLite, local test servers).
   - **Speed:** Seconds. Run on git pre-push or PR validation.
3. **End-to-End (E2E) Tests:**
   - **Scope:** Simulates a complete user workflow through the full system (e.g., signup $\rightarrow$ checkout $\rightarrow$ invoice generation).
   - **Dependencies:** Real running services.
   - **Speed:** Minutes. Reserve strictly for mission-critical core paths.

### When to Invert the Pyramid Deliberately:
- **Thin Glue / API Gateways:** When an application is primarily a router/orchestrator with almost no internal algorithmic logic, unit tests add little value. Shift weight toward **integration tests** verifying real payload contracts.
- **UI-Heavy Frontends:** Core component interactions are often best validated through **component integration tests** (e.g. React Testing Library) rather than purely isolated unit tests.

---

## 2. What to Test (The Quality Standard)

- [ ] **2.1 New Logic Always Gets a Test:** Never excuse missing tests with *"it's simple"* or *"it's just a helper"*. Bugs live in the simple things.
- [ ] **2.2 Dual Coverage (Happy Path + Boundary Case):** Every unit of business logic must test:
  1. The primary successful outcome (**happy path**).
  2. At least one boundary, empty, or error condition (**edge case**: null input, negative value, timeout, unauthorized state).
- [ ] **2.3 Test Behavior, Not Implementation Details:**
  - Test public inputs and outputs, not private methods or internal state variables.
  - **The Refactoring Test:** If you rewrite the internal implementation without changing the public contract, your tests should still pass. If they break, you were testing implementation details.
- [ ] **2.4 Don't Test the Framework:** Never write tests verifying that language/framework primitives work (e.g., testing that a plain getter returns what a setter stored, or that a library's array sorting sorts).

---

## 3. Mocking Discipline & Anti-Patterns

Mocking is a necessary tool, but over-mocking destroys test confidence.

- [ ] **3.1 What to Mock:**
  - External I/O (Stripe, Twilio, third-party HTTP APIs).
  - Non-deterministic factors (current system time, random UUIDs, crypto salt).
  - Slow / dangerous resources (disk formatters, email sending).
- [ ] **3.2 What NOT to Mock:**
  - Internal business collaborators or adjacent helper classes. Let them run real code.
  - Language data structures (don't mock a `Map` or `List`).
- [ ] **3.3 The "Over-Mocking" Smell:**
  - If a test requires 30 lines of mock configuration to test 3 lines of business code, **stop**. You are testing your mock configuration, not production behavior.
- [ ] **3.4 Prefer Fakes Over Canned Mocks:**
  - Where practical, use lightweight stateful fakes (e.g., an in-memory repository implementing the interface) over rigid canned mocks (`when(repo.get(1)).thenReturn(...)`).

---

## 4. Diagnosing & Eliminating Flaky Tests

A flaky test is a high-priority **bug in your test suite**, never an acceptable nuisance. Never re-run a failing test in CI until it turns green without investigating.

### Top 4 Causes of Test Flakiness:
1. **Shared Mutable State:** Tests polluting a shared database, global variables, or singleton caches. Fix by isolating test contexts or truncating state in `beforeEach`/`teardown`.
2. **Unmocked Time & Race Conditions:** Relying on real wall-clock delays (`sleep(500)`). Fix by using deterministic fake timers (`vi.useFakeTimers()`, `time-machine`).
3. **Async Polling / Missing Awaits:** Code finishes after the test framework has already asserted. Fix by explicitly awaiting promises or polling conditions with a timeout.
4. **Order Dependence:** Test B passes only if Test A ran first. Verify test suite independence by shuffling execution order (e.g., `pytest --random-order`, `jest --randomize`).

> **Quarantine Policy:** If a flaky test cannot be fixed immediately, quarantine it with a skipped annotation (e.g. `@pytest.mark.skip`) and **must link to an open tracking issue**. Never delete tests silently.

---

## 5. Coverage as a Signal, Not a Target

- [ ] **5.1 Coverage % is a Vanity Metric:** 95% line coverage with weak or missing assertions provides false confidence.
- [ ] **5.2 Prioritize Risk Over Percentages:**
  - Critical paths (Authentication, Payment processing, State machines, Data integrity) require rigorous **branch coverage**.
  - Trivial boilerplate (DTOs, simple config maps, generated code) does not need coverage.
- [ ] **5.3 Ban Tautological Tests:** Reject tests written solely to hit coverage numbers without asserting meaningful behavioral outcomes (e.g. calling a function without an `assert` or `expect`).

---

## 6. Test Design & Structure

- [ ] **Scenario-Descriptive Naming:** Name tests after the scenario and expected outcome:
  - ✅ `returns_validation_error_when_email_lacks_at_symbol`
  - ❌ `test_email` or `test_error`
- [ ] **AAA Pattern (Arrange, Act, Assert):** Visually separate test execution into three clear blocks:
  ```typescript
  // Arrange
  const cart = new ShoppingCart();
  cart.add(item, 2);

  // Act
  const total = cart.calculateTotal();

  // Assert
  expect(total).toBe(40.0);
  ```
- [ ] **Independent Execution:** Every test must be completely isolated and capable of running in parallel or random order.

---

## Detailed References

- [`references/framework-notes.md`](file:///Users/apple/Projects/yash/skills/testing-strategy/references/framework-notes.md): Canonical test idioms, parameterized tables, and mocking examples across **pytest (Python)**, **Vitest / Jest (JS/TS)**, **Go testing**, **JUnit 5 (Java)**, **cargo test (Rust)**, and **PHP / Laravel (Pest & PHPUnit)**.


