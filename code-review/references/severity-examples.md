# Review Comment Severity Triage & Worked Examples

> Companion reference for `code-review`.
> Calibrates how to categorize code review comments into **BLOCKER**, **SHOULD-FIX**, and **NIT / SUGGESTION**.

---

## 1. Severity Definitions & Decision Criteria

| Severity Level | Definition | Impact on PR Approval | Author Obligation |
|---|---|---|---|
| 🔴 **BLOCKER** | Direct correctness bug, data corruption risk, security vulnerability, breaking API change, unhandled fatal crash, missing regression test for a reported bug, or severe violation of established repository architecture. | **Blocks approval.** PR cannot be merged until resolved. | Must be addressed and verified before merge. |
| 🟡 **SHOULD-FIX** | Meaningful robustness, maintainability, or readability improvement. Missing edge-case handling on non-critical paths, missing docstrings on complex algorithms, ambiguous naming, or unmeasured performance smell. | **Does not strictly block merge** if time-critical, provided the author acknowledges it or files a follow-up ticket. | Should be addressed now or captured in an explicit tracking issue. |
| 🟢 **NIT / SUGGESTION** | Personal aesthetic preference, alternative syntactic idiom that is not objectively superior, minor typo in an internal comment, non-critical variable rename suggestion, or minor micro-optimization. | **Never blocks approval.** Author may merge immediately after reading. | Optional. Author may accept or politely decline. |

---

## 2. Worked Real-World Calibration Examples

| Scenario / Code Pattern | Classification | Rationale |
|---|---|---|
| Unsanitized user string passed directly into raw SQL query | 🔴 **BLOCKER** | Direct security vulnerability (SQL Injection). Must never merge. |
| Missing error check on `db.Query()` return in Go | 🔴 **BLOCKER** | Causes silent failure or nil pointer panic under database outages. |
| New payment calculation function has zero unit tests | 🔴 **BLOCKER** | Financial and core business logic without test coverage is high risk. |
| Public API endpoint changed JSON key from `user_id` to `userId` | 🔴 **BLOCKER** | Breaking change for existing external consumers and mobile apps without versioning. |
| Hardcoded API secret token found in config file | 🔴 **BLOCKER** | Secret leak in Git history. Must be revoked and removed immediately. |
| Function parameter called `data` instead of `invoicePayload` | 🟡 **SHOULD-FIX** | Ambiguous naming harms long-term maintainability, but does not cause a runtime defect. |
| Missing timeout on outbound HTTP client request | 🟡 **SHOULD-FIX** | Server could exhaust thread pool if upstream third party hangs, but happy path works. |
| 60-line function with 4 levels of nested if-else statements | 🟡 **SHOULD-FIX** | Violates clean code standards; early guard returns would significantly improve readability. |
| Incomplete error log message missing customer ID context | 🟡 **SHOULD-FIX** | Makes production debugging harder, but error is properly caught and handled. |
| Suggesting `map.getOrDefault(key, 0)` instead of `if (map.containsKey(key))` | 🟢 **NIT** | Both approaches are correct and functional; idiomatic shorthand preference only. |
| Suggesting destructuring: `const { id, name } = user` over `user.id` | 🟢 **NIT** | Purely stylistic choice; does not affect runtime behavior or safety. |
| Minor typo in a private helper method's comment | 🟢 **NIT** | Low impact; worth fixing if editing, but never worth blocking a deployment. |
| Suggesting `useMemo` for an array of 5 static string items | 🟢 **NIT** | Premature micro-optimization; overhead of `useMemo` exceeds benefit. |
| Preferring `snake_case` over `camelCase` in internal helper in Python | 🔴 **BLOCKER** / 🟡 **SHOULD-FIX** | If the codebase strictly enforces PEP 8 and linters fail, it's a blocker. If unconfigured, it's a strong should-fix. |

---

## 3. The Golden Rules of Review Calibration

1. **Never block on Nits alone:** If a review contains 5 nits and 0 blockers, mark the PR **Approved with comments**, not **Request Changes**.
2. **Distinguish "Wrong" from "Different":**
   - *"This approach has an unhandled null pointer"* $\rightarrow$ **Wrong** (BLOCKER).
   - *"I personally prefer using a switch statement instead of if-else here"* $\rightarrow$ **Different** (NIT).
3. **Explicitly Label Comments:** Prefix comments with `[BLOCKER]`, `[SHOULD-FIX]`, or `[NIT]` so the author immediately knows what requires action before merging.
