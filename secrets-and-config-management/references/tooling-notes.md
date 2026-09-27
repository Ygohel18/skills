# Secret Scanners & Secrets Managers Reference Guide

> Companion reference for `secrets-and-config-management`.
> Concrete installation, configuration, and operational guidance for automated secret scanners, production secret vaults, and emergency credential exposure procedures.

---

## 1. Secret Scanning Tools (Pre-Commit & CI)

Automated scanners detect high-entropy strings, known token prefixes (e.g., `ghp_`, `sk_live_`, `AKIA`), and private key blocks before code is pushed.

### 1.1 Gitleaks (Industry Standard)
Gitleaks is a fast, lightweight scanner written in Go, ideal for local pre-commit hooks and CI pipelines.

- **Installation:**
  ```bash
  # macOS (Homebrew)
  brew install gitleaks

  # Go install
  go install github.com/gitleaks/gitleaks/v8@latest
  ```

- **Local Scan:**
  ```bash
  # Scan uncommitted staged changes
  gitleaks protect --staged --verbose

  # Scan entire git history
  gitleaks detect --verbose
  ```

- **Pre-Commit Hook (`.pre-commit-config.yaml`):**
  ```yaml
  repos:
    - repo: https://github.com/gitleaks/gitleaks
      rev: v8.18.2
      hooks:
        - id: gitleaks
  ```

- **Handling False Positives (`.gitleaksignore`):**
  Never disable the scanner. Add the false-positive fingerprint to `.gitleaksignore`:
  ```text
  # Allow mock test fixture
  test/fixtures/mock_stripe_key.json:stripe-api-token:73
  ```

---

### 1.2 TruffleHog (Live Verification)
TruffleHog scans Git history, filesystems, and S3 buckets. Its killer feature is **live credential verification**—it tests discovered keys against provider APIs (e.g. AWS, Slack, GitHub) to verify if the secret is active.

- **Installation & Scan:**
  ```bash
  # Run via Docker without installing
  docker run --rm -v "$PWD:/pwd" trufflesecurity/trufflehog:latest git file:///pwd --since-commit HEAD~5

  # CLI scan of recent commit
  trufflehog git file://. --since-commit HEAD~1
  ```

---

### 1.3 GitHub Secret Scanning & Push Protection
- Enable **Secret Scanning** and **Push Protection** in repository settings (`Settings > Code security and analysis`).
- Push protection intercepts `git push` attempts that contain known tokens from 100+ partner providers (AWS, Stripe, OpenAI, Slack, Google) and rejects the push before the commit reaches GitHub.

---

## 2. Production Secrets Managers

In production, applications should fetch secrets at runtime using IAM identities rather than storing static secrets in local disks or unencrypted configuration maps.

### 2.1 AWS Secrets Manager & SSM Parameter Store
- **Authentication:** Use IAM Roles for Service Accounts (IRSA) on EKS or ECS Task Roles. Never hardcode AWS access keys!
- **Features:** Automated Lambda-based rotation for RDS PostgreSQL, MySQL, and Aurora.
- **Node.js Example:**
  ```javascript
  import { SecretsManagerClient, GetSecretValueCommand } from "@aws-sdk/client-secrets-manager";

  const client = new SecretsManagerClient({ region: "us-east-1" });
  const response = await client.send(new GetSecretValueCommand({ SecretId: "prod/db/credentials" }));
  const { username, password } = JSON.parse(response.SecretString);
  ```

---

### 2.2 GCP Secret Manager
- **Authentication:** Google Cloud Workload Identity.
- **Python Example:**
  ```python
  from google.cloud import secretmanager

  client = secretmanager.SecretManagerServiceClient()
  name = "projects/my-project/secrets/stripe-api-key/versions/latest"
  response = client.access_secret_version(request={"name": name})
  api_key = response.payload.data.decode("UTF-8")
  ```

---

### 2.3 HashiCorp Vault
- **Best For:** Hybrid multi-cloud, on-premise, and dynamic short-lived credentials.
- **Dynamic Secrets:** Generates temporary, single-use database credentials with an automatic TTL (e.g. valid for 1 hour), completely eliminating permanent database passwords.

---

### 2.4 Doppler (Universal Developer Secret Ops)
- **Best For:** Fast developer setup synchronizing dev, staging, and prod configurations without manual `.env` file sharing.
- **Runtime Injection:**
  ```bash
  doppler run -- node server.js
  ```
  Injects environment variables into the process memory without ever writing them to disk.

---

## 3. Emergency Secret Incident Response Playbook

When a credential (API key, private token, DB password) is accidentally committed to Git or leaked into public logs:

```text
Step 1: ROTATE IMMEDIATELY (Do not wait to diagnose)
  │
Step 2: Revoke the Exposed Credential at the Provider
  │
Step 3: Audit Cloud / Service Provider Access Logs for Unauthorized Usage
  │
Step 4: Rewrite Git History (if committed to a public or shared branch)
```

### Detailed Response Steps:
1. **Rotate First:** Issue a new secret immediately and deploy it to dependent production services.
2. **Revoke the Leaked Secret:** Disable the compromised key in Stripe, AWS IAM, GitHub, or OpenAI dashboard. Treat the key as 100% compromised from the second it was committed.
3. **Audit Access Logs:**
   - For AWS: Check CloudTrail for calls made with the compromised `AccessKeyId`.
   - For Stripe / GitHub: Inspect webhook delivery and API request logs for unfamiliar IP addresses during the exposure window.
4. **Scrub Git History:**
   - Removing the line in a new commit does **NOT** delete it from history.
   - Use `git-filter-repo` (recommended over legacy `git filter-branch` or BFG):
     ```bash
     # Install git-filter-repo
     pip install git-filter-repo

     # Remove offending file from all commits across all branches
     git filter-repo --invert-paths --path .env
     ```
   - Coordinate with teammates before force-pushing rewritten history.
