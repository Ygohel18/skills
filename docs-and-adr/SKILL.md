---
name: docs-and-adr
description: >
  Language-agnostic framework for writing, structuring, and maintaining technical project documentation,
  user-facing READMEs, Keep a Changelog updates, and Architecture Decision Records (ADRs).
  Triggers whenever an agent is asked to "write a README", "document this decision", "add a changelog entry",
  "write an ADR", "why did we choose this approach?", or "update CHANGELOG.md". Enforces the 30-second README rule,
  reproducible setup commands, SemVer-aligned changelogs, immutable superseded ADRs, and documentation freshness gates.
metadata:
  author: yash
  version: "1.0"
  scope: "documentation, readme, changelog, adr, technical-writing, architecture-decisions"
allowed-tools: Read Write Bash
---

# Documentation & Architecture Decision Records (ADRs)

A language-agnostic operational standard for writing project READMEs, user-facing changelogs, and Architecture Decision Records (ADRs).

> **Sibling Standards:**
> - For line-level code comments and docstrings, see [`universal-coding-standards`](file:///Users/apple/Projects/yash/skills/universal-coding-standards/SKILL.md#4-comments--documentation).
> - For commit message semantics vs changelog entries, see [`git-commit-workflow`](file:///Users/apple/Projects/yash/skills/git-commit-workflow/SKILL.md#phase-2-commit-message-crafting).
> - For OpenAPI and contract documentation, see [`api-design`](file:///Users/apple/Projects/yash/skills/api-design/SKILL.md#7-spec-first-documentation).

---

## 1. README Structure & The 30-Second Rule

Assume the reader gives your repository **30 seconds** before deciding whether it solves their problem.

### 1.1 Essential Sections (In Order):
1. **Title & Single-Paragraph Pitch:** What problem does this project solve, and for whom?
2. **Key Capabilities:** 3–5 bullet points highlighting standout features.
3. **Prerequisites & Quickstart:** Copy-pasteable setup and run commands.
4. **Testing Instructions:** How to execute unit/integration test suites.
5. **Contributing & License:** Pointer to `CONTRIBUTING.md` and the project license.

### 1.2 Verification Rule:
- 🚫 **Never document a command you haven't verified!**
- Ensure all installation, Docker, and start commands run without undocumented implicit dependencies.

---

## 2. Changelog Conventions (Keep a Changelog + SemVer)

A changelog communicates user-facing value and upgrade paths, not internal Git churn.

- [ ] **2.1 Strict Categorization:**
  - Group all entries under the six standardized headings: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
- [ ] **2.2 Pair with Semantic Versioning (SemVer):**
  - **MAJOR (v2.0.0):** Incompatible breaking API or schema changes.
  - **MINOR (v1.2.0):** Backwards-compatible new features.
  - **PATCH (v1.1.4):** Backwards-compatible bug fixes.
- [ ] **2.3 Human-Centric Wording:**
  - Write for human consumers. Explain *what changed and why it matters to them*, not raw commit SHA dumps.

---

## 3. Architecture Decision Records (ADRs)

ADRs capture the rationale behind critical technical forks so future engineers don't re-litigate decisions or undo intentional trade-offs.

### 3.1 When to Write an ADR:
- When a decision is **significant, difficult to reverse, or impacts team-wide architecture**:
  - ✅ Choosing a primary database engine (PostgreSQL vs DynamoDB).
  - ✅ Introducing an architectural pattern (Event-Driven Architecture, Micro-frontends).
  - ✅ Adopting a core framework or authentication protocol (OAuth2 PKCE vs Session Cookies).
  - ❌ *Do not write ADRs for routine, easily reversible code styling or minor library helper additions.*

### 3.2 ADR Immutability & Lifecycle:
- Once an ADR is marked **Accepted**, its content is **immutable**.
- When an architecture evolves or changes direction, **never edit or delete the old ADR**.
- Mark the old ADR as `Superseded by ADR-XXXX`, and write a new ADR detailing what changed and linking back to the original.

---

## 4. Documentation Taxonomy: Where Content Lives

Avoid conflating different layers of documentation:

| Documentation Layer | Primary Purpose | Audience | Lifespan / Maintenance |
|---|---|---|---|
| **Code Comments** | Explains *why* a specific line or non-obvious algorithm exists. | Active code maintainer | Kept in sync with code; deleted when code is refactored. |
| **README.md** | High-level project pitch, architecture diagram, and onboarding guide. | New team members, external evaluators | Living document; updated whenever onboarding/setup changes. |
| **CHANGELOG.md** | Chronological record of notable changes between releases. | Developers upgrading versions | **Append-only**; historical releases are never rewritten. |
| **ADR (Architecture Decision)** | Captures historical trade-offs, constraints, and decision drivers. | Engineering organization | **Append-only**; superseded when direction changes. |
| **API Contract (OpenAPI)** | Precise schema, endpoints, types, and status codes. | Frontend & API consumers | Generated alongside or prior to code changes. |

---

## 5. Preventing Documentation Rot

- [ ] **5.1 Same-PR Documentation Rule:**
  - If a code change alters environment variables, installation steps, or API contracts, the documentation updates **must land in the same pull request**. Never defer documentation to a vague "docs later" ticket.
- [ ] **5.2 Conflicting Docs are P1 Bugs:**
  - Documentation that directly contradicts current software behavior is a high-severity bug that damages engineering trust. Fix immediately.

---

## Detailed References

- [`references/adr-template.md`](file:///Users/apple/Projects/yash/skills/docs-and-adr/references/adr-template.md): Ready-to-copy ADR template and a complete worked example (`ADR-0004: Adopt Redis Pub/Sub for Live Order Status Updates`).
- [`references/changelog-template.md`](file:///Users/apple/Projects/yash/skills/docs-and-adr/references/changelog-template.md): Ready-to-copy Keep a Changelog 1.1.0 template with standard category definitions and human-centric writing examples.
