---
name: universal-coding-standards
description: >
  Enforce clean, robust, and secure engineering standards across any programming language (Python,
  JavaScript, TypeScript, Go, Rust, Java, C#, PHP, Ruby, C/C++). Triggers whenever an agent writes,
  reviews, audits, or refactors code, generates pull requests, checks code quality, or answers questions
  like "is this good code?", "review this PR", "refactor this function", or "write clean code".
  Applies 10 universal pillars: naming, error handling, function design, comments, testing, security,
  dependencies, version control, formatting, and performance trade-offs.
metadata:
  author: yash
  version: "1.0"
  scope: "cross-language, engineering-standards, code-review"
allowed-tools: Read Write Bash
---

# Universal Coding Standards

A language-agnostic operational standard for writing, refactoring, and reviewing code.

> **Precedence Rule:** Specific repository configurations (`.editorconfig`, `tsconfig.json`, `ruff.toml`) and official ecosystem formatters (`gofmt`, `rustfmt`, `black`, `dotnet format`) **always take precedence** over generic aesthetic preferences.

---

## The 10 Engineering Pillars (Operational Checklist)

Run through this checklist while authoring or evaluating any code changes:

### 1. Naming & Structure
- [ ] **Idiomatic Casing:** Apply the target language's standard casing (see [`references/language-notes.md`](file:///Users/apple/Projects/yash/skills/universal-coding-standards/references/language-notes.md)).
  - Python / Rust / Ruby: `snake_case` functions and variables
  - JS / TS / Java: `camelCase` functions and variables
  - C#: `PascalCase` methods, `_camelCase` private fields
  - Go: `camelCase` private, `PascalCase` exported
- [ ] **Intention-Revealing Names:** Use clear, descriptive names over cryptic abbreviations. Avoid single-letter variables outside tight loop counters (`i`, `j`) or well-known coordinate math (`x`, `y`).
- [ ] **Single Responsibility per File:** Organize modules so each file owns one cohesive concept or responsibility. Avoid "dumping-ground" utility files.

### 2. Error Handling & Resilience
- [ ] **No Silent Swallowing:** Never use empty `catch` blocks or bare `except: pass`. At minimum, log the error with context or re-raise.
- [ ] **Actionable Errors:** Error messages must identify what failed, the offending identifier or argument, and whether recovery is possible.
- [ ] **Recoverable vs Fatal:** Handle expected domain failures (e.g., missing record, validation error) explicitly; reserve panics, crashes, or unhandled exceptions for unrecoverable state corruption.
- [ ] **Propagate Context:** In Go, check `if err != nil` and wrap with `fmt.Errorf("...: %w", err)`; in Rust, propagate with `?`; in JS/Python/Java/C#, preserve error causes or stack traces.

### 3. Function & Method Design
- [ ] **Single Responsibility Principle (SRP):** Each function does one thing well. If a function requires section comments to explain sequential phases, extract those phases into helper functions.
- [ ] **Manageable Size:** Keep functions short and readable (aim for under 40–50 lines).
- [ ] **Guard Clauses Over Deep Nesting:** Invert conditions and return early to keep the main happy path at the lowest possible indentation level.
- [ ] **Explicit Inputs & Outputs:** Prefer pure functions and explicit parameters over implicit modification of shared global state.

### 4. Comments & Documentation
- [ ] **Document the "Why", Not the "What":** Code describes *how*; comments explain *why* non-obvious constraints, business edge cases, or workarounds exist.
- [ ] **Public API Docs:** Exported functions, public classes, and HTTP endpoints must include docstrings/JSDoc/Rustdoc specifying purpose, parameters, return types, and thrown exceptions.
- [ ] **Zero Dead Code:** Delete commented-out code blocks immediately. Git history preserves past experiments.

### 5. Testing & Verification
- [ ] **Test Coverage for New Logic:** Every new feature, calculation, or bug fix must include corresponding unit or integration tests.
- [ ] **Dual Coverage (Happy + Edge):** Test both the successful path and at least one boundary/error condition (e.g. empty list, negative balance, timeout, invalid format).
- [ ] **Deterministic Data:** Avoid hardcoding volatile test data (timestamps like `Date.now()`, live external endpoints) that causes flaky test failures.

### 6. Security Baseline
- [ ] **Zero Hardcoded Secrets:** Never commit API keys, database credentials, JWT secrets, or private keys. Load strictly from environment variables or secure vaults.
- [ ] **Input Sanitization & Validation:** Treat all external data (HTTP bodies, query params, files, headers) as untrusted. Validate schemas at system boundaries.
- [ ] **Prevent Injection Vectors:**
  - SQL: Never concatenate SQL strings; use parameterized queries or ORM binding.
  - Commands: Never pass unescaped user input to `shell=True` or `exec()`.
  - Deserialization: Avoid unsafe object deserializers (`pickle.loads()`, `BinaryFormatter`, unvalidated `YAML.load()`).

### 7. Dependency & Version Hygiene
- [ ] **Standard Library First:** Do not install third-party packages for functionality already provided natively by the modern standard library.
- [ ] **Locked Versions:** Always maintain and commit package lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `Cargo.lock`, `uv.lock`, `composer.lock`, `go.sum`).
- [ ] **Security Audits:** Avoid dependencies with unmaintained licenses or known high-severity CVEs.

### 8. Version Control Hygiene
- [ ] **Atomic Commits:** Bundle one logical change per commit with a concise, imperative commit message (`Add payment webhook handler`).
- [ ] **Ignore Build Artifacts:** Verify `.gitignore` excludes `node_modules/`, `target/`, `dist/`, `__pycache__/`, `.env`, and OS metadata (`.DS_Store`).
- [ ] **No Large Binary Blobs:** Never commit compiled binaries, large SQLite files, or large video assets to Git without LFS justification.

### 9. Formatting & Linting
- [ ] **Automated Tooling Compliance:** Format code using project tools (`prettier`, `ruff`, `gofmt`, `rustfmt`, `dotnet format`).
- [ ] **Clean Static Analysis:** Code must pass all project linters (`eslint`, `ruff check`, `golangci-lint`, `cargo clippy`, `phpstan`) with zero errors or unaddressed warnings.
- [ ] **Consistent Styling:** Adhere to established whitespace, quote, and line-length conventions of the surrounding repository.

### 10. Performance & Readability Trade-Off
- [ ] **Readability First:** Clear, predictable, maintainable code trumps clever micro-optimizations by default.
- [ ] **Measured Optimization:** Optimize algorithms and memory only on verified hot paths with profiling data or concrete performance requirements.
- [ ] **Avoid Obvious Anti-Patterns:** Eliminate accidental $O(N^2)$ lookups (e.g., searching an unindexed array inside a loop instead of using a `Set` or `Map`) and database N+1 queries.

---

## Detailed References

- [`references/language-notes.md`](file:///Users/apple/Projects/yash/skills/universal-coding-standards/references/language-notes.md): Per-language casing tables, canonical formatters/linters, idiomatic error handling, and ecosystem security footguns (Python, JS/TS, Go, Rust, Java, C#, PHP, Ruby, C/C++).
- [`references/review-checklist.md`](file:///Users/apple/Projects/yash/skills/universal-coding-standards/references/review-checklist.md): Fast pass/fail checklist categorized by **BLOCKER**, **WARNING**, and **NIT** for code reviews and PR audits.
