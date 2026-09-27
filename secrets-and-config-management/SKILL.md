---
name: secrets-and-config-management
description: >
  Language-agnostic framework for managing secrets, credentials, environment variables, and application configuration.
  Triggers whenever an agent is asked to "add an API key", "set up environment variables", "I committed a secret by accident",
  "how should I store this credential?", "secrets in CI", "manage config", or "configure secret scanning".
  Covers secret vs config classification, local .env.example discipline, centralized config loaders,
  CI encrypted secrets, production vaults (AWS Secrets Manager, Vault, Doppler), rotation playbooks, and Gitleaks scanning.
metadata:
  author: yash
  version: "1.0"
  scope: "secrets-management, credentials, env-vars, devsecops, incident-response"
allowed-tools: Read Write Bash
---

# Secrets & Configuration Management

A language-agnostic operational standard for handling secrets, environment variables, and configuration across local development, CI/CD, and production environments.

> **Sibling Standards:**
> - For pre-commit scanning and verifying staged diffs before committing, see [`git-commit-workflow`](file:///Users/apple/Projects/yash/skills/git-commit-workflow/SKILL.md#12-scan-for-secrets--credentials).
> - For avoiding malicious packages that steal environment variables, see [`package-security-vetting`](file:///Users/apple/Projects/yash/skills/package-security-vetting/SKILL.md).
> - For application-level input sanitization and security baselines, see [`universal-coding-standards`](file:///Users/apple/Projects/yash/skills/universal-coding-standards/SKILL.md#6-security-baseline).

---

## 1. Secret vs. Configuration Classification

Before storing any value, categorize it strictly:

| Category | Definition | Examples | Storage Rule |
|---|---|---|---|
| **Secret** | Confidential data that proves identity or grants access. Compromise leads directly to unauthorized system access or financial loss. | Database passwords, API tokens (Stripe, OpenAI), private SSH/TLS keys, JWT signing keys, OAuth client secrets. | **NEVER in Git.** Local `.env` (gitignored), CI secret vaults, or cloud secrets managers. |
| **Configuration** | Non-sensitive runtime parameters that control application behavior without granting access. | Port numbers, log levels (`INFO`, `DEBUG`), timeout thresholds (30s), pagination limits, public CDN URLs, feature flags. | Safe to commit in version control (e.g. `config/default.json`, `settings.py`) or inject via environment variables. |

---

## 2. Local Development Standards

- [ ] **2.1 Strict `.gitignore` Protection:**
  - Verify that `.gitignore` contains entries for all local secret files:
    ```gitignore
    .env
    .env.*
    !.env.example
    *.pem
    *.key
    ```
- [ ] **2.2 Commit `.env.example` with Safe Placeholders:**
  - Always maintain a committed `.env.example` documenting all required variables with dummy values:
    ```bash
    # Database
    DATABASE_URL=postgresql://user:password@localhost:5432/dev_db

    # Third-Party APIs (Do not commit real keys!)
    STRIPE_SECRET_KEY=sk_test_placeholder_key_here
    OPENAI_API_KEY=sk-placeholder
    ```
- [ ] **2.3 Never Commit Secrets "Temporarily":**
  - A secret committed to Git is **permanent in history**, even if deleted in the very next commit.
  - If a secret is committed, you must **rotate the secret immediately at the provider**, not merely delete the file.
- [ ] **2.4 Centralized Configuration Loader:**
  - Never scatter direct `process.env.MY_VAR` or `os.environ.get("MY_VAR")` calls across controllers and UI components.
  - Load and validate all configuration in a single, typed central configuration module (e.g., using `Zod`, `Pydantic`, or a Config class) that fails loudly at application startup if required keys are missing.

---

## 3. CI/CD Pipeline Practices

- [ ] **3.1 Encrypted Platform Stores Only:**
  - Store CI secrets strictly within the hosting platform's encrypted secret store (GitHub Actions Secrets, GitLab CI Masked Variables, CircleCI Contexts).
  - **Never** hardcode tokens inside pipeline YAML files (e.g., `.github/workflows/deploy.yml`).
- [ ] **3.2 Automatic Log Masking:**
  - Ensure secret values are masked in CI execution logs.
  - 🚫 **Never `echo` or print secrets to stdout** for pipeline debugging.
- [ ] **3.3 Minimum Job Scoping (Least Privilege):**
  - Inject deployment credentials only into the specific `deploy` job, never globally across all linting or unit test jobs.

---

## 4. Production Secret Architecture

- [ ] **4.1 Dedicated Secrets Managers Over Static Files:**
  - In production, avoid placing static `.env` files on production virtual machines or baking secrets into Docker image layers.
  - Use cloud-native secrets managers (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault, or Doppler) to inject secrets at runtime via IAM service identities (see [`references/tooling-notes.md`](file:///Users/apple/Projects/yash/skills/secrets-and-config-management/references/tooling-notes.md)).
- [ ] **4.2 Service-Level Isolation:**
  - Give each microservice or component access only to the exact secrets it requires, rather than sharing a single monolithic environment blob.
- [ ] **4.3 Strict Environment Separation:**
  - Never point a development or staging environment at production databases, Stripe live keys, or production third-party webhooks as a "shortcut".

---

## 5. Secret Rotation & Incident Response

- [ ] **5.1 Scheduled vs. Emergency Rotation:**
  - Rotate database passwords and API tokens on a defined schedule (e.g. every 90 days).
  - Trigger **immediate emergency rotation** upon any suspected leak (committed to Git, printed in Sentry/Datadog logs, or exposed in a client-side bundle).
- [ ] **5.2 The Incident Rule: Rotate First, Investigate Second:**
  - When an exposure is identified, **revoke and rotate the secret immediately** at the provider. Never leave an exposed credential active while investigating how it happened.
- [ ] **5.3 Maintain a Secret Inventory:**
  - Keep a documented catalog mapping each external credential to the applications, CI pipelines, and environments that depend on it to prevent unexpected outages during rotation.

---

## 6. Automated Secret Detection

- [ ] **6.1 Pre-Commit & CI Scanning:**
  - Enforce automated secret scanners (e.g. `gitleaks`, `trufflehog`) in local pre-commit hooks and CI pull request gates.
- [ ] **6.2 Handling Scanner False Positives:**
  - When a scanner flags a simulated test fixture or documentation example, allowlist the specific fingerprint in the scanner configuration (e.g. `.gitleaksignore`).
  - 🚫 **Never disable the scanner** to bypass a build failure.

---

## Detailed References

- [`references/tooling-notes.md`](file:///Users/apple/Projects/yash/skills/secrets-and-config-management/references/tooling-notes.md): Setup commands and configuration examples for **Gitleaks**, **TruffleHog**, **AWS Secrets Manager**, **GCP Secret Manager**, **HashiCorp Vault**, **Doppler**, and the **Git History Scrubbing Playbook** (`git-filter-repo`).
