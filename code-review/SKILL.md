---
name: code-review
description: >
  Language-agnostic framework for conducting thorough, respectful, and constructive code reviews on pull requests,
  merge requests, git diffs, or code snippets. Triggers whenever an agent is asked to "review this PR",
  "review this diff", "give feedback on this code", "is this ready to merge?", "audit this pull request",
  or "critique this implementation". Enforces structured review ordering (intent first, architecture second,
  lines last), objective 3-tier severity triage (Blocker vs Should-Fix vs Nit), actionable feedback phrasing,
  and clear approval decisions.
metadata:
  author: yash
  version: "1.0"
  scope: "code-review, pr-feedback, quality-audit, collaborative-engineering"
allowed-tools: Read Write Bash
---

# Code Review Protocol

An operational guide for reviewing another engineer's pull request, diff, or code snippet across any programming language.

> **Sibling Standards:**
> - For the underlying engineering standards and language conventions, refer to [`universal-coding-standards`](file:///Users/apple/Projects/yash/skills/universal-coding-standards/SKILL.md).
> - For evaluating commit history, commit messages, and branch hygiene, refer to [`git-commit-workflow`](file:///Users/apple/Projects/yash/skills/git-commit-workflow/SKILL.md).
> - For vetting any newly introduced dependencies, refer to [`package-security-vetting`](file:///Users/apple/Projects/yash/skills/package-security-vetting/SKILL.md).

---

## 1. Review Scope & Order

Follow this 3-step sequence when evaluating any code change:

```text
Step 1: Understand Intent (PR description, linked ticket, acceptance criteria)
  │
Step 2: High-Level Architecture (Does the approach make sense? Any design flaws?)
  │
Step 3: Detailed File Review (Logic correctness, edge cases, tests, security, nits)
```

1. **Understand Intent First:** Always read the PR description, user story, or linked issue *before* inspecting the diff. Review against what the change claims to accomplish.
2. **Review High-Level Approach First:** Evaluate the architectural design, component boundaries, and schema changes before examining line-by-line syntax. If the high-level approach is fundamentally flawed, detailed syntax feedback is wasted.
3. **Distinguish "Wrong" from "Different":**
   - **Wrong:** Causes a bug, security flaw, data corruption, or breaks conventions $\rightarrow$ **Blocks approval**.
   - **Different:** An alternative stylistic approach that works equally well $\rightarrow$ **Suggest as optional Nit**.

---

## 2. Severity Triage Framework

Every review comment must be categorized into one of three explicit tiers:

| Tier | Marker | Criteria | Impact on Approval |
|---|---|---|---|
| **Blocking** | 🔴 `[BLOCKER]` | Direct bugs, edge-case crashes, security flaws, missing tests for core logic, breaking API changes, or repo guideline violations. | **Blocks approval.** Must be fixed before merging. |
| **Should-Fix** | 🟡 `[SHOULD-FIX]` | Ambiguous naming, missing documentation on complex logic, missing timeout/retry handling, or unmeasured performance smells. | Does not block merge if time-critical; may be tracked in a follow-up ticket. |
| **Nit / Suggestion** | 🟢 `[NIT]` | Non-standard personal preference, stylistic alternative, minor typo in a comment, or minor micro-optimization. | **Never blocks approval.** Author has full discretion to adopt or skip. |

> **Golden Rule:** Never block a pull request on nits alone. If a PR has 0 blockers and 6 nits, approve the PR with comments.

---

## 3. Review Checklist (What to Check)

Verify these five dimensions across the diff:

### 3.1 Correctness & Edge Cases
- [ ] Does the implementation fulfill all stated ticket requirements?
- [ ] Are boundary values handled (null/nil, empty arrays, zero values, negative numbers, long strings)?
- [ ] Are concurrency, race conditions, or state mutations handled safely?
- [ ] Are error states caught and handled gracefully (no silent swallowing)?

### 3.2 Test Adequacy
- [ ] Are all new features and bug fixes accompanied by automated tests?
- [ ] Do tests assert on real behavioral outcomes rather than mocking out the entire system?
- [ ] Are both the happy path and at least one failure/edge path tested?

### 3.3 Security & Dependencies
- [ ] Zero committed secrets, private tokens, or hardcoded credentials.
- [ ] All external user inputs are validated and sanitized at system boundaries.
- [ ] Database queries use parameterized queries (zero SQL string interpolation).
- [ ] If new dependencies are added, verify provenance and security advisories via [`package-security-vetting`](file:///Users/apple/Projects/yash/skills/package-security-vetting/SKILL.md).

### 3.4 Readability & Maintainability
- [ ] Would a new engineer understand this code in 6 months without explanation?
- [ ] Are identifiers intention-revealing and idiomatic to the target language?
- [ ] Are functions short, focused, and free of deeply nested conditional pyramids?

### 3.5 Scope Creep & Atomicity
- [ ] Does this PR represent **one logical unit of work**?
- [ ] Flag unrelated formatting changes, opportunistic refactors, or accidental file edits bundled into the PR.

---

## 4. Constructive Phrasing Rules

When drafting review comments:

1. **Critique the Code, Not the Author:**
   - ❌ *"You forgot to validate the payload."*
   - ✅ *"This endpoint doesn't appear to validate the payload schema before passing it to the database."*
2. **Inquire Rather than Accuse:**
   - ❌ *"This will break when the list is empty."*
   - ✅ *"What happens here if the list is empty? Would `items[0]` throw an `IndexOutOfBounds` error?"*
3. **Explain the "Why":** Always explain the underlying risk (e.g. data loss, performance degradation, security exploit) so the author learns the rationale.
4. **Provide Actionable Code Suggestions:** Include concrete code snippets demonstrating the recommended fix.
5. **Praise Good Decisions:** Acknowledge clean abstractions, clever simplifications, and thorough tests.

*(See [`references/feedback-phrasing.md`](file:///Users/apple/Projects/yash/skills/code-review/references/feedback-phrasing.md) for more examples).*

---

## 5. The Review Decision

End every review with an unambiguous summary and verdict:

### Option A: Approve (No Blockers)
- Use when the code is safe, correct, and adequately tested.
- If suggestions or nits are included, clearly label them as non-blocking:
  > *"Looks solid! Left two minor non-blocking nits regarding naming. Approved!"*

### Option B: Request Changes (At Least One Blocker)
- Use when one or more 🔴 `[BLOCKER]` issues must be addressed before merge.
- Provide a concise summary checklist at the top of the review:
  > *"Great progress on this feature! Before merging, we need to address two blocking items:*
  > *1. Parameterize the raw SQL query in `findUserById` (security).*
  > *2. Add unit tests covering the zero-balance edge case.*
  > *Happy to re-review once updated!"*

---

## Reference Guides

- [`references/feedback-phrasing.md`](file:///Users/apple/Projects/yash/skills/code-review/references/feedback-phrasing.md): Practical before-and-after examples demonstrating respectful, constructive phrasing for bugs, performance, style, and positive reinforcement.
- [`references/severity-examples.md`](file:///Users/apple/Projects/yash/skills/code-review/references/severity-examples.md): Worked real-world examples calibrating how to categorize review comments into Blocker, Should-Fix, and Nit.
