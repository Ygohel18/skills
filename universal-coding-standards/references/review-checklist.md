# Universal Code Review Checklist

> Compact pass/fail checklist for code reviews, pull requests, refactorings, and pre-commit audits.
> Classification: **BLOCKER** (must fix before merge), **WARNING** (should fix unless justified), **NIT** (non-blocking suggestion).

---

## 1. Naming & Structure
- [ ] **BLOCKER:** No single-letter variable names outside of tight loop counters (`i`, `j`, `k`) or coordinate tuples (`x`, `y`, `z`).
- [ ] **BLOCKER:** Case convention matches language idiom (see `language-notes.md`: `snake_case` in Python/Rust, `camelCase` in JS/Java/Go, `PascalCase` in C#).
- [ ] **WARNING:** Names reflect business intent and state (e.g. `is_authenticated` over `flag`, `user_accounts` over `data`).
- [ ] **WARNING:** Single responsibility per file/module; no sprawling 1500+ line "utils" or "helpers" dumping grounds.

---

## 2. Error Handling
- [ ] **BLOCKER:** No empty/bare `catch` or `except: pass` blocks silently swallowing exceptions.
- [ ] **BLOCKER:** In Go, all `(val, err)` returns are checked (`if err != nil`); in Rust, all `Result` values are handled or propagated with `?`.
- [ ] **WARNING:** Error messages contain actionable context (which resource failed, what identifier was being processed).
- [ ] **WARNING:** Distinct separation between expected domain errors (e.g. `UserNotFound`) and unexpected internal faults (e.g. database timeout).

---

## 3. Function & Method Design
- [ ] **BLOCKER:** No hidden side effects modifying global/shared mutable state without explicit documentation.
- [ ] **WARNING:** Functions adhere to Single Responsibility Principle (SRP) and fit within a manageable reading length (< 50 lines typical).
- [ ] **WARNING:** Guard clauses and early returns are used to eliminate arrow-anti-pattern nesting (> 3 nested indentation levels).
- [ ] **WARNING:** Function parameter list is reasonable (<= 4 params; group into a structured options/config object if larger).

---

## 4. Comments & Documentation
- [ ] **BLOCKER:** Zero commented-out dead code chunks left in the codebase (git history preserves history).
- [ ] **WARNING:** Comments explain **why** a decision was made (business constraints, non-obvious workarounds), not **what** the syntax does.
- [ ] **WARNING:** Public APIs, exported functions, and reusable library classes include docstrings describing purpose, arguments, return type, and thrown errors.

---

## 5. Testing
- [ ] **BLOCKER:** New business logic, bug fixes, and critical paths are covered by automated unit/integration tests.
- [ ] **BLOCKER:** Tests assert on concrete expected behavior, not trivial tautologies (`expect(true).toBe(true)`).
- [ ] **WARNING:** Tests cover at least one happy path + at least one boundary/edge condition (null/empty inputs, network timeout, unauthorized access).
- [ ] **WARNING:** No hardcoded volatile fixtures or fragile sleeps that induce flaky test failures.

---

## 6. Security Baseline
- [ ] **BLOCKER:** Absolutely zero hardcoded credentials, secret keys, bearer tokens, or internal API passwords.
- [ ] **BLOCKER:** No SQL string concatenation; parameterized queries or ORM binds are strictly used.
- [ ] **BLOCKER:** No dynamic code evaluation (`eval()`, `exec()`, `Function()`, `pickle.loads()`, `YAML.load()`) on user-controlled input.
- [ ] **BLOCKER:** External inputs (HTTP bodies, query params, file uploads) are strictly validated/sanitized before use.

---

## 7. Dependency & Version Hygiene
- [ ] **BLOCKER:** Dependencies are accompanied by a lockfile (`package-lock.json`, `Cargo.lock`, `uv.lock`, `composer.lock`).
- [ ] **WARNING:** No unnecessary third-party packages introduced for tasks trivial in standard library (e.g. `left-pad`, simple UUID generation).
- [ ] **WARNING:** Newly added dependencies are active, maintained, and do not introduce known severe CVE vulnerabilities.

---

## 8. Version Control Hygiene
- [ ] **BLOCKER:** No committed `.env` files, build artifacts (`dist/`, `build/`, `.class`, `.pyc`), `.DS_Store`, or IDE caches (`.idea/`, `.vscode/`).
- [ ] **WARNING:** Commit messages follow the imperative mood with clear intent (`Add user rate limiting to prevent auth brute force`).
- [ ] **WARNING:** Commit is atomic (bundles one coherent change, rather than 10 unrelated file edits).

---

## 9. Formatting & Linting
- [ ] **BLOCKER:** Passes all repository linters, type checks (`tsc`, `mypy`, `cargo clippy`), and automated CI build checks.
- [ ] **WARNING:** Code is formatted with the project's configured formatter (`Prettier`, `Ruff`, `gofmt`, `rustfmt`, `dotnet format`).
- [ ] **NIT:** Consistent trailing commas, indentation, and quote styles matching adjacent codebase files.

---

## 10. Performance & Readability Trade-Off
- [ ] **BLOCKER:** No obvious $O(N^2)$ nested loops over unbounded data or N+1 query patterns in database fetching.
- [ ] **WARNING:** Simple, clear, readable code is chosen over esoteric one-liners or premature micro-optimizations.
- [ ] **WARNING:** Any complex performance-critical algorithmic optimization includes an explanatory comment citing benchmarks or constraints.
