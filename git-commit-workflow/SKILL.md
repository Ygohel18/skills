---
name: git-commit-workflow
description: >
  Language-agnostic workflow for preparing, crafting, validating, and managing Git commits and branches.
  Triggers whenever an agent is about to create a git commit ("git commit", "commit these changes",
  "stage and commit"), reviews recent commits ("review my commit", "check git diff"), prepares a pull request,
  or handles post-commit operations ("push changes", "draft PR description"). Enforces pre-commit diff reviews,
  secret prevention, debug artifact cleanup, Conventional Commits formatting, atomic commit hygiene,
  and destructive command guardrails.
metadata:
  author: yash
  version: "1.0"
  scope: "git-version-control, commit-hygiene, pre-commit-checks, code-safety"
allowed-tools: Read Write Bash
---

# Git Commit Workflow

An operational checklist for crafting clean, atomic, and safe Git commits across any language or repository.

> **Sibling Standard:** For general code quality, naming, and engineering hygiene, pair this workflow with the [`universal-coding-standards`](file:///Users/apple/Projects/yash/skills/universal-coding-standards/SKILL.md) skill.

---

## Phase 1: Pre-Commit Checks (Before `git commit`)

Walk through these verification gates before executing any commit command:

### 1.1 Read the Staged Diff
- [ ] **Inspect Staged Content:** Always run and inspect `git diff --cached` before writing the commit message.
  ```bash
  git diff --cached
  ```
- [ ] **Never Commit Blindly:** Never assume what was staged based on file names alone. Confirm every added or deleted line.

### 1.2 Scan for Secrets & Credentials
- [ ] **Zero Hardcoded Secrets:** Verify no staged files contain:
  - Private API keys, JWT secrets, database connection strings, passwords, or OAuth bearer tokens.
  - Private SSH/TLS keys (`.pem`, `.key`, `id_rsa`).
  - Staged `.env`, `.env.local`, or configuration files with real secrets (ensure `.env.example` is used instead).

### 1.3 Strip Debug Artifacts & Dead Code
- [ ] **No Ephemeral Logging:** Check for leftover ad-hoc debug logs (`console.log`, `print()`, `fmt.Println()`, `dd()`, `debugger;`, `binding.pry`, `import pdb`).
- [ ] **No Dead Code Chunks:** Remove large commented-out blocks of replaced code.
- [ ] **No Untracked TODOs:** If a `TODO` is added, ensure it links to an active issue/ticket (e.g. `// TODO(PROJ-120): ...`).

### 1.4 Prevent Unintended & Binary Files
- [ ] **Respect `.gitignore`:** Run `git status -s` to ensure untracked build artifacts, caches, or dependencies are not staged:
  - Node / JS: `node_modules/`, `dist/`, `.next/`, `.turbo/`
  - Python: `__pycache__/`, `.pytest_cache/`, `*.pyc`, `.venv/`
  - Java / Kotlin / Rust: `target/`, `build/`, `.gradle/`, `*.class`
  - OS / IDE: `.DS_Store`, `Thumbs.db`, `.idea/`, `.vscode/` (unless team-shared)
- [ ] **No Large Binary Blobs:** Never stage large SQLite files, datasets, videos, or compiled binaries without Git LFS justification.

### 1.5 Enforce Atomicity
- [ ] **Single Coherent Change:** The commit must represent **one logical unit of work**.
- [ ] **Separate Formatting from Logic:** Never bundle a massive repository reformatting or lint-fix pass into a feature or bug fix commit.
- [ ] **Interactive Staging:** If unrelated edits exist in the working directory, stage only relevant hunks using:
  ```bash
  git add -p <file>
  ```

### 1.6 Verify Branch Context
- [ ] **Protected Branch Check:** Never commit directly to protected branches (`main`, `master`, `release/*`) if the project follows feature-branch branching models.
- [ ] **Feature Branch:** Ensure work resides on a dedicated branch (e.g., `feat/auth-pkce`, `fix/issue-104`).

### 1.7 Run Lint, Format, and Test Gates
- [ ] **Respect Pre-Commit Hooks:** If the project uses Husky, lint-staged, or `.pre-commit-config.yaml`, let the hooks run.
- [ ] **Never Bypass Hooks:** Never append `--no-verify` or `-n` unless the user explicitly demands it (see [`references/safety-rules.md`](file:///Users/apple/Projects/yash/skills/git-commit-workflow/references/safety-rules.md)).

---

## Phase 2: Commit Message Crafting

### 2.1 Detect Existing Repository Style
Inspect the last 15 commits before authoring the message:
```bash
git log -n 15 --oneline
```
- If the project uses Conventional Commits $\rightarrow$ follow [`references/conventional-commits.md`](file:///Users/apple/Projects/yash/skills/git-commit-workflow/references/conventional-commits.md).
- If the project uses ticket prefixes (e.g., `[JIRA-123] ...`) $\rightarrow$ mirror that convention.

### 2.2 Standard Message Structure
```text
<type>(<scope>): <imperative summary under 50 chars>

<Detailed body explaining WHY this change was made, what problem it solves,
and any non-obvious trade-offs or decisions made. Wrapped at 72 chars.>

<Footer: references, ticket IDs, breaking change notices>
```

### 2.3 Subject Line Rules
- [ ] **Imperative Mood:** Use `add`, `fix`, `refactor`, `prevent` (never `added`, `adds`, `fixing`).
- [ ] **Soft Limit 50 Chars:** Keep the header concise (hard limit 72 chars).
- [ ] **No Trailing Period:** Never end the subject line with a period `.`.
- [ ] **No Sensitive Data:** Never include internal hostnames, user emails, or tokens in the commit message.

### 2.4 Explanatory Body ("The Why")
- [ ] Leave one blank line between the subject and the body.
- [ ] Explain **why** the change was necessary (business requirement, edge-case failure, security patch). The diff already shows *what* changed.

### 2.5 Ticket Linking
- [ ] Reference tickets when applicable (`Fixes #142`, `Ref: PROJ-982`). Never invent or hallucinate ticket IDs.

---

## Phase 3: Post-Commit Actions

### 3.1 Verify What Landed
Immediately verify the created commit:
```bash
git show --stat --oneline HEAD
```
Confirm:
1. The commit hash and message are correct.
2. Only the intended files and line counts were committed.

### 3.2 Push Discipline
- [ ] **Push Feature Branch:**
  ```bash
  git push -u origin <branch-name>
  ```
- [ ] **Never Bare Force-Push:** Never run `git push --force` on shared branches. If rewriting a private branch, use:
  ```bash
  git push --force-with-lease origin <branch-name>
  ```

### 3.3 CI & Pipeline Awareness
- [ ] Acknowledge that the pushed commit triggers CI/CD workflows (lint, tests, container builds). Do not declare a task "complete" if CI checks are failing.

### 3.4 Pull / Merge Request Follow-Through
- [ ] When a logical unit of work is completed, prompt the user or draft a PR description:
  - Summary of changes
  - Motivation / context
  - Testing steps performed
  - Related issue links

### 3.5 History Preservation & Traceability
- [ ] Once commits have been pushed and shared with teammates, do not rewrite history (`rebase -i`, `amend`) to hide mistakes. Use a forward corrective commit (`fix: ...`) or `git revert <sha>`.

---

## Phase 4: Strict Safety Guardrails

The following rules apply unconditionally:

1. **User Review Required:** Never commit or push code on behalf of the user without displaying the diff and proposed commit message first, unless autonomous commits were explicitly pre-authorized for the session.
2. **Prohibited Destructive Commands:**
   - 🚫 `git push --force` (without `--force-with-lease` and explicit confirmation)
   - 🚫 `git reset --hard` (destroys uncommitted changes)
   - 🚫 `git clean -fdx` (wipes untracked files)
   - 🚫 `git rebase -i` on shared upstream history
3. **No `--no-verify` Bypass:** If a git hook fails, fix the code or test. Never bypass with `--no-verify`.

---

## Reference Guides

- [`references/conventional-commits.md`](file:///Users/apple/Projects/yash/skills/git-commit-workflow/references/conventional-commits.md): Complete specification, type taxonomy (`feat`, `fix`, `docs`, `refactor`, `perf`), breaking change syntax, and good/bad examples.
- [`references/safety-rules.md`](file:///Users/apple/Projects/yash/skills/git-commit-workflow/references/safety-rules.md): Guardrail policies, destructive command restrictions, safe alternatives, and emergency `git reflog` recovery steps.
