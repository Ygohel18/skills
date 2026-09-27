# Keep a Changelog Template & Guidelines

> Companion reference for `docs-and-adr`.
> Based on the official [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) specification and Semantic Versioning 2.0.0.

---

## 1. Ready-to-Copy `CHANGELOG.md` Template

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Multi-factor authentication (MFA) via TOTP authenticator apps.
- Webhook delivery retry backoff policy for HTTP 5xx responses.

### Fixed
- Prevent duplicate payment authorization on rapid double-click in checkout.

---

## [1.2.0] - 2026-09-15

### Added
- Export orders to CSV directly from the merchant dashboard (#412).
- Filter search results by custom tag attributes.

### Changed
- Improved order table loading time by memoizing customer address lookups.
- Upgraded Node runtime target from v18 to v20.

### Deprecated
- Legacy `/api/v1/orders/export` endpoint; will be removed in v2.0.0 in favor of `/api/v2/reports/orders`.

### Fixed
- Resolve memory leak in long-running WebSocket subscription workers (#389).
- Fix timezone parsing discrepancy when converting UTC timestamps to local browser times.

### Security
- Upgrade `axios` from 1.6.0 to 1.7.4 to remediate CVE-2024-XXXX (SSRF vulnerability).

---

## [1.1.0] - 2026-08-01

### Added
- Real-time order notification sound alert for new orders.

### Removed
- Removed support for deprecated Internet Explorer 11 browser builds.

---

## [1.0.0] - 2026-06-10

### Added
- Initial public stable release.
- Core checkout, order management, and customer portal APIs.

---

<!-- Version Comparison Links -->
[Unreleased]: https://github.com/organization/project/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/organization/project/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/organization/project/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/organization/project/releases/tag/v1.0.0
```

---

## 2. Standard Category Definitions

Group all changes under these exact six standardized headings (newest version first):

| Category | Usage & Definition |
|---|---|
| `Added` | New features, endpoints, or user capabilities. |
| `Changed` | Changes in existing functionality, performance improvements, refactors affecting behavior. |
| `Deprecated` | Features that are still functional but slated for removal in future major releases. |
| `Removed` | Features, flags, or endpoints that have now been permanently deleted. |
| `Fixed` | Bug fixes, calculation corrections, regression patches. |
| `Security` | Vulnerability remediations, dependency security upgrades, encryption enhancements. |

---

## 3. Reader-First vs. Git Commit Dump

A changelog is written for **human consumers, customers, and developers integrating your software**. It is NOT a copy-paste of internal Git commits.

### Comparison:
- ❌ **Git Commit Dump:**
  - `feat(api): refactor UserController.ts line 42`
  - `fix: typo in sql`
  - `WIP testing merge`
- ✅ **Human-Centric Changelog:**
  - `Fixed an issue where user avatar uploads larger than 5MB failed without an error message (#241).`
  - `Added support for European SEPA direct debit payment processing.`
