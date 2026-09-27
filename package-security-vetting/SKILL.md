---
name: package-security-vetting
description: >
  Language-agnostic security protocol for auditing, vetting, installing, and managing third-party dependencies.
  Triggers whenever an agent is about to recommend, add, install, or audit a package ("add a dependency",
  "install this package", "is this npm package safe?", "check this library", "add to requirements.txt",
  "npm install", "pnpm add", "pip install", "uv add", "composer require", "go get", "cargo add", "bundle add").
  Provides a fast-path audit for routine packages and a comprehensive deep-vetting checklist covering typosquatting,
  lifecycle scripts, license compliance, lockfile pinning, and supply-chain attack prevention.
metadata:
  author: yash
  version: "1.0"
  scope: "supply-chain-security, dependency-vetting, vulnerability-auditing"
allowed-tools: Read Write Bash
---

# Package Security Vetting

A language-agnostic operational standard for evaluating third-party dependencies before and after adding them to any project.

> **Sibling Standards:**
> - For general dependency hygiene, pair with [`universal-coding-standards`](file:///Users/apple/Projects/yash/skills/universal-coding-standards/SKILL.md#7-dependency--version-hygiene).
> - For committing lockfiles safely and reviewing staged diffs, pair with [`git-commit-workflow`](file:///Users/apple/Projects/yash/skills/git-commit-workflow/SKILL.md#14-prevent-unintended--binary-files).

---

## Decision Flow: Fast-Path vs Deep-Check

```text
Is the package a top-tier, industry-standard library
(e.g., React, Express, FastAPI, Pydantic, Gin, Serde)
with millions of weekly downloads and an established organization?
│
├── YES ──> Follow FAST-PATH (1. Verify name spelling -> 2. Run ecosystem audit -> 3. Commit lockfile)
│
└── NO  ──> Follow FULL DEEP-CHECK PATH (All 4 phases below)
```

---

## ⚡ The Fast-Path (Routine, Established Dependencies)

When adding well-known industry packages:
1. **Name Check:** Confirm exact package spelling against official documentation (prevent typosquatting like `crossenv` vs `cross-env`).
2. **Audit Scan:** Run the native vulnerability scanner (see [`references/ecosystem-commands.md`](file:///Users/apple/Projects/yash/skills/package-security-vetting/references/ecosystem-commands.md)):
   - Node: `npm audit` or `pnpm audit`
   - Python: `uv audit` or `pip-audit`
   - Go: `govulncheck ./...`
   - PHP: `composer audit`
   - Rust: `cargo audit`
3. **Commit Lockfile:** Generate and stage the lockfile with pinned cryptographic hashes.

---

## 🛡️ Full Deep-Check Path (Unfamiliar, Low-Adoption, or High-Risk Packages)

### 1. Pre-Vetting (Before Recommending or Installing)
- [ ] **1.1 Justify the Need (Left-Pad Avoidance):**
  - Does the modern standard library already provide this? (e.g. `fetch()`, `crypto.randomUUID()`, `pathlib`, `json`).
  - Does an already-installed dependency in the project already expose this functionality?
  - Reject adding a 50-line package for a 3-line utility.
- [ ] **1.2 Verify Provenance & Typosquatting:**
  - Check author credibility: Is it backed by a known organization or verified publisher?
  - Verify download statistics and age: Packages under 60 days old with low download counts require extreme scrutiny.
  - Verify official links: Ensure repository URL on GitHub/GitLab matches the author website, not an unlinked clone.
- [ ] **1.3 Maintenance & Community Health:**
  - When was the last release published? (Flag packages abandoned > 2 years).
  - Are open issues and PRs actively triaged?
  - Is the repository officially archived or marked deprecated?
- [ ] **1.4 Vulnerability & Advisory Database Check:**
  - Query the exact target version against [GitHub Advisory Database](https://github.com/advisories) and [OSV.dev](https://osv.dev).
  - Confirm zero unpatched HIGH or CRITICAL CVEs exist for the specified version.
- [ ] **1.5 License Compatibility:**
  - Verify package license (MIT, Apache-2.0, BSD-3-Clause, ISC).
  - Flag copyleft licenses (GPL, AGPL) in proprietary commercial codebases.
  - Reject packages with non-commercial (Commons Clause) or custom restrictive licenses.
- [ ] **1.6 Inspect Code & Install Scripts:**
  - Check `package.json` / `setup.py` / `composer.json` for automated lifecycle hooks (`preinstall`, `postinstall`, `build.rs`).
  - If install scripts make outbound network calls (`curl`, `fetch`) or execute shell binaries, inspect the source manually before proceeding.

### 2. Lockfile & Version Pinning Discipline
- [ ] **2.1 Lockfile Mandatory:**
  - Every project must maintain a committed lockfile (`package-lock.json`, `pnpm-lock.yaml`, `uv.lock`, `poetry.lock`, `composer.lock`, `go.sum`, `Cargo.lock`).
  - **Never** add lockfiles to `.gitignore`.
- [ ] **2.2 Version Pinning Strategy:**
  - In applications / services: Pin exact versions (`1.4.2`) or narrow tilde ranges (`~1.4.2`) to prevent unexpected upstream compromise.
  - In libraries: Use standard caret ranges (`^1.4.0`) to avoid duplicate transitive dependencies for consumers, while locking test runs.
- [ ] **2.3 Cryptographic Integrity Enforcement:**
  - Enforce hash checks (npm `integrity` SHA-512, pip `--require-hashes`, Go `go.sum`).
  - Never disable checksum validation to bypass an installation error.

### 3. Safe Installation Execution
- [ ] **3.1 Never Install as Root:**
  - Never run `sudo npm install`, `sudo pip install`, or root package commands.
- [ ] **3.2 Restrict Lifecycle Scripts:**
  - When evaluating an unknown package, install with script execution disabled:
    - Node: `pnpm add <pkg> --ignore-scripts`
    - PHP: `composer require <pkg> --no-scripts`
    - Python: Prefer pre-compiled binary wheels (`pip install --only-binary :all:`) over raw source tarballs with untrusted `setup.py`.
- [ ] **3.3 Trusted Registries Only:**
  - Never install from unpinned git branches (`git+https://...#main`), unverified personal forks, or HTTP tarball URLs when an official package exists on the canonical registry (npm, PyPI, Packagist, crates.io).

### 4. Post-Install & Ongoing Hygiene
- [ ] **4.1 Continuous CI Auditing:**
  - Integrate native audit commands (`npm audit`, `uv audit`, `govulncheck`, `composer audit`) into CI pull request pipelines.
- [ ] **4.2 Dependency Confusion Defense:**
  - Scope all internal enterprise packages under an organization namespace (e.g. `@company/pkg`).
  - Configure package managers to never query public registries for private scoped namespaces.
- [ ] **4.3 Monitor Ownership & Maintainer Changes:**
  - Be suspicious of sudden major releases on long-dormant packages or transfers to unknown maintainers (see [`references/known-attack-patterns.md`](file:///Users/apple/Projects/yash/skills/package-security-vetting/references/known-attack-patterns.md)).
- [ ] **4.4 Prune Unused Packages:**
  - Periodically clean stale dependencies (`npm prune`, `go mod tidy`, `composer install --prune`). Unused packages remain attack surface.

---

## Reference Guides

- [`references/ecosystem-commands.md`](file:///Users/apple/Projects/yash/skills/package-security-vetting/references/ecosystem-commands.md): Canonical audit, lockfile verification, safe flags (`--ignore-scripts`), and pruning commands for npm, pnpm, yarn, pip, uv, poetry, Composer, Go, Cargo, Bundler, Maven, Gradle, and NuGet.
- [`references/known-attack-patterns.md`](file:///Users/apple/Projects/yash/skills/package-security-vetting/references/known-attack-patterns.md): Real-world supply-chain attack analysis (typosquatting, dependency confusion, account takeover, malicious postinstall scripts, protestware) with historical case studies.
