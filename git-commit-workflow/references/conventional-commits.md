# Conventional Commits Reference Guide

> Source: https://www.conventionalcommits.org/v1.0.0/
> Companion reference for `git-commit-workflow`.

---

## 1. Specification Format

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Key Structural Rules
1. **Type:** Lowercase noun describing the intent of the change.
2. **Scope (Optional):** Lowercase noun wrapped in parentheses indicating the codebase section affected (e.g., `(auth)`, `(parser)`, `(deps)`).
3. **Breaking Change Marker:** An exclamation mark `!` immediately before the colon (e.g., `feat(api)!: drop legacy v1 endpoints`) signals a breaking API change.
4. **Description:** Imperative, present-tense summary (`add`, not `added` or `adds`), lowercase start, **no trailing period**, under 50 characters.
5. **Body (Optional):** Separated from subject by a single blank line. Explains the motivation, business context, and architectural rationale ("the WHY"). Wrapped at 72 characters.
6. **Footer(s) (Optional):** Separated from body by a single blank line. Contains issue references (`Closes #42`, `Fixes PROJ-1024`) or breaking change descriptions.

---

## 2. Standard Commit Types

| Type | Intent | SemVer Impact | Example |
|---|---|---|---|
| `feat` | Introduces a new user-facing feature or API capability | MINOR (0.x.0) | `feat(auth): add OAuth2 PKCE authorization flow` |
| `fix` | Patches a bug or unintended behavior | PATCH (0.0.x) | `fix(checkout): prevent duplicate payment submission on double-click` |
| `docs` | Documentation-only changes (README, docstrings, architecture guides) | None | `docs(readme): clarify local development prerequisites` |
| `style` | Formatting, whitespace, semicolon changes that do not affect code logic | None | `style: run prettier formatting across src/` |
| `refactor` | Code change that neither fixes a bug nor adds a feature | None | `refactor(db): extract query builder into repository class` |
| `perf` | Code change that improves execution speed, memory, or rendering | None / PATCH | `perf(search): memoize fuzzy search regex compilation` |
| `test` | Adding missing tests or correcting existing tests | None | `test(auth): add unit tests for expired token refresh` |
| `build` | Changes that affect build systems or external dependencies | None / PATCH | `build(deps): bump vite from 5.1.0 to 5.2.0` |
| `ci` | Changes to CI configuration files and scripts (GitHub Actions, GitLab CI) | None | `ci(github): add matrix testing for Node 20 and 22` |
| `chore` | Miscellaneous housekeeping tasks that don't modify src or test files | None | `chore: update .gitignore to ignore scratch directory` |
| `revert` | Reverts a previous commit | Depends | `revert: "feat(billing): enable Stripe tax calculation"` |

---

## 3. Detecting Repository Commit Convention

Before writing a commit message, agents must inspect recent repository history:

```bash
git log -n 15 --oneline
```

- **If Conventional Commits are prevalent** (e.g., `feat:...`, `fix(...):...`): Adopt the convention strictly, reusing existing scope names.
- **If Jira / Ticket prefixes are standard** (e.g., `[PROJ-102] Add webhook`, `ENG-404: fix null pointer`): Match that exact team syntax.
- **If plain imperative sentences are used** (e.g., `Add user avatar upload endpoint`): Maintain imperative style without forcing artificial `feat:` prefixes.

---

## 4. Good vs. Bad Commit Message Examples

### Example 1: New Feature
- ❌ **Bad:** `Added stripe support` *(Past tense, vague, no context)*
- ❌ **Bad:** `feat: stripe payments.` *(Trailing period, non-descriptive)*
- ✅ **Good:**
  ```text
  feat(billing): add Stripe payment intent webhook handler

  Process asynchronous payment confirmation events from Stripe webhooks.
  Validates incoming HMAC signatures before updating invoice records in Postgres.

  Closes #184
  ```

### Example 2: Bug Fix
- ❌ **Bad:** `fix bug in auth` *(Vague; what was the bug?)*
- ❌ **Bad:** `WIP fixing token expiration crash` *(WIP label left in commit)*
- ✅ **Good:**
  ```text
  fix(auth): handle expired JWT tokens without unhandled 500 error

  Catch TokenExpiredError explicitly and return a 401 Unauthorized response
  with standard error JSON payload instead of raising an uncaught exception.

  Fixes #209
  ```

### Example 3: Breaking Change
- ✅ **Good:**
  ```text
  feat(api)!: remove deprecated v1 user profile endpoint

  Delete /api/v1/users/:id in favor of /api/v2/users/:id. The v2 endpoint
  returns normalized ISO-8601 timestamps and camelCase JSON keys.

  BREAKING CHANGE: /api/v1/users/:id has been removed. All clients must
  migrate to /api/v2/users/:id.
  ```
