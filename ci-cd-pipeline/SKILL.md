---
name: ci-cd-pipeline
description: >
  Language-agnostic framework for designing, reviewing, optimizing, and securing CI/CD pipelines
  (GitHub Actions, GitLab CI, CircleCI). Triggers whenever an agent is asked to "set up CI",
  "write a GitHub Actions workflow", "why is my pipeline slow?", "how should I deploy this?",
  "add a required check", or "configure build caching". Enforces fast-fail topologies, lockfile-based caching,
  job parallelization, immutable artifact promotion, and progressive deployment safety.
metadata:
  author: yash
  version: "1.0"
  scope: "ci-cd, github-actions, gitlab-ci, circleci, devops, deployment-safety"
allowed-tools: Read Write Bash
---

# CI/CD Pipeline Architecture & Standards

A language-agnostic operational standard for designing, reviewing, and optimizing automated continuous integration and continuous deployment pipelines.

> **Sibling Standards:**
> - For local pre-commit checks before pushing to CI, see [`git-commit-workflow`](file:///Users/apple/Projects/yash/skills/git-commit-workflow/SKILL.md#phase-1-pre-commit-checks-before-git-commit).
> - For injecting credentials securely into pipeline runners, see [`secrets-and-config-management`](file:///Users/apple/Projects/yash/skills/secrets-and-config-management/SKILL.md#3-cicd-pipeline-practices).
> - For diagnosing flaky tests that break pipeline runs, see [`testing-strategy`](file:///Users/apple/Projects/yash/skills/testing-strategy/SKILL.md#4-diagnosing--eliminating-flaky-tests).

---

## 1. Pre-Commit vs. CI Division of Labor

Never confuse local pre-commit hooks with remote CI pipelines:

| Check Layer | Execution Context | Execution Budget | Appropriate Checks |
|---|---|---|---|
| **Pre-Commit** (Local) | Developer machine via Git hook | **< 5 seconds** | Code formatting, fast linters on *staged files only*, basic syntax checks. |
| **CI Pipeline** (Remote) | Ephemeral cloud runner / container | **3–10 minutes** | Full repository test suite, multi-version matrices, type checking, security audits, container builds. |

- 🚫 **Never rely solely on pre-commit hooks for correctness or security:** Developers can bypass local hooks with `git commit --no-verify`. CI is the **authoritative gatekeeper**.

---

## 2. Pipeline Structure & Topology

- [ ] **2.1 Fail-Fast Topology:**
  - Structure pipelines in phased dependency tiers:
    ```text
    Tier 1 (Fast-Fail, Parallel): Linting + Static Analysis + Typechecking (< 60s)
      │
    Tier 2 (Core Validation): Unit & Fast Integration Tests (1–3 min)
      │
    Tier 3 (Heavy/End-to-End): Full Build + E2E Tests + Security Scans
      │
    Tier 4 (Deployment): Environment Promotion (Staging -> Production)
    ```
  - Abort downstream jobs immediately if a fast-fail check fails.
- [ ] **2.2 Parallelize Independent Jobs:**
  - Never run lint, type-check, and unit tests in a single serial script if the CI runner supports concurrent jobs.
- [ ] **2.3 Pipelines as Code:**
  - Store pipeline definitions in version control alongside application source code (`.github/workflows/`, `.gitlab-ci.yml`), never configured purely via web UIs.

---

## 3. Caching & Performance

- [ ] **3.1 Key Caches on Lockfile Hashes:**
  - Cache package manager stores (`~/.npm`, `~/.cache/pip`, `~/.cargo/registry`, `go-build`) keyed strictly on the cryptographic hash of the lockfile:
    - GitHub Actions: `v1-deps-${{ hashFiles('**/pnpm-lock.yaml') }}`
    - GitLab CI: `cache:key:files: - package-lock.json`
- [ ] **3.2 Pass Artifacts Between Stages (Build Once):**
  - Compile application binaries or web bundles once in a `build` job, upload them as CI artifacts, and download them in downstream `test` and `deploy` jobs.
  - 🚫 **Never rebuild from scratch** in the deploy job.
- [ ] **3.3 Never Cache Dynamic State or Secrets:**
  - 🚫 Never cache test results themselves (masks failures).
  - 🚫 Never cache directories containing secret keys or environment variables.

---

## 4. Deployment Safety & Progressive Rollouts

- [ ] **4.1 Mandatory Passing CI Gates:**
  - Require all critical CI checks to pass before merging PRs or initiating deployments. Disallow administrative bypasses for normal feature releases.
- [ ] **4.2 Progressive Deployment Strategies:**
  - Production-critical services must employ progressive delivery rather than abrupt all-at-once restarts:
    - **Canary:** Route 5% $\rightarrow$ 25% $\rightarrow$ 100% of user traffic while monitoring error rates.
    - **Blue-Green:** Stand up an identical green environment; switch router traffic atomically once health checks pass.
- [ ] **4.3 Pre-Defined Rollback Mechanism:**
  - Every deployment plan must document the exact rollback procedure before execution (e.g. automated health check failure rollback or instant traffic reroute).
- [ ] **4.4 Decouple Deployment from Release:**
  - Deploy code silently to production behind feature flags, allowing product enablement without emergency code deployments.

---

## 5. Environment Promotion

- [ ] **5.1 Single Immutable Artifact Promotion:**
  - The exact same container image or compiled bundle tested in Staging must be promoted to Production.
  - Recompiling for each environment introduces configuration drift and untested build variations.
- [ ] **5.2 Environment Parity:**
  - Staging topologies (database engine, Redis version, reverse proxy) must mirror production as closely as possible to prevent "works in staging, fails in prod" incidents.

---

## 6. Pipeline Observability & Job Health

- [ ] **6.1 Actionable Failure Alerts:**
  - Route build failure notifications to team communication channels (Slack, Discord, Teams) with direct links to the failing job log.
- [ ] **6.2 Zero Tolerance for Flaky CI Jobs:**
  - Treat an intermittently failing CI job as a high-severity operational bug. Investigate race conditions, runner timeouts, and network dependencies rather than repeatedly retrying builds.

---

## Detailed References

- [`references/platform-notes.md`](file:///Users/apple/Projects/yash/skills/ci-cd-pipeline/references/platform-notes.md): Complete configuration syntax and patterns for **GitHub Actions**, **GitLab CI**, and **CircleCI** covering caching directives, job dependencies (`needs`), artifact passing, and environment-scoped secrets.
