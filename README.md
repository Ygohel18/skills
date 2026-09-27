# Agent Skills

A collection of production-grade, language-agnostic AI agent skills built to the [Agent Skills Specification](https://agentskills.io/specification).

These skills give AI coding agents operational checklists, security guardrails, design token mappings, and engineering standards across the entire software development lifecycle.

---

## Skills Catalog

| Skill | Description | Primary Triggers |
|---|---|---|
| [`accessibility-audit`](./accessibility-audit) | Audit web UI against WCAG 2.2 AA, ARIA APG patterns, 4.5:1 contrast, and keyboard navigation. | `a11y audit`, `WCAG compliant`, `add ARIA`, `screen reader` |
| [`agent-skills-authoring`](./agent-skills-authoring) | Meta-skill for authoring, structuring, and validating new agent skills against the specification. | `author a skill`, `create skill`, `SKILL.md spec` |
| [`api-design`](./api-design) | Design REST & GraphQL contracts, RFC 9457 error models, status codes, pagination, and OpenAPI specs. | `design an API`, `add endpoint`, `review API contract`, `REST vs GraphQL` |
| [`ci-cd-pipeline`](./ci-cd-pipeline) | Design and optimize pipelines with fast-fail topologies, lockfile caching, and deployment safety. | `set up CI`, `GitHub Actions workflow`, `pipeline slow`, `deploy safety` |
| [`code-review`](./code-review) | Review PRs using a 3-tier severity triage (`[BLOCKER]`, `[SHOULD-FIX]`, `[NIT]`) and constructive phrasing. | `review this PR`, `review this diff`, `is this ready to merge` |
| [`design-system-adapter`](./design-system-adapter) | Adapt any UI to 15 design systems (M3, Apple HIG, Liquid Glass, Carbon, Polaris, Fluent 2, etc.). | `make this look like M3`, `apply Apple HIG`, `IBM Carbon style`, `Polaris` |
| [`docker-and-containers`](./docker-and-containers) | Author multi-stage Dockerfiles, minimal base images, non-root users, and Trivy security scans. | `write a Dockerfile`, `containerize app`, `why is image so big`, `compose` |
| [`docs-and-adr`](./docs-and-adr) | Write 30-second READMEs, Keep a Changelog releases, and immutable Architecture Decision Records (ADRs). | `write a README`, `write an ADR`, `add changelog entry`, `document decision` |
| [`git-commit-workflow`](./git-commit-workflow) | Enforce pre-commit diff checks, secret scanning, Conventional Commits, and safety guardrails. | `git commit`, `commit these changes`, `check git diff`, `prepare PR` |
| [`package-security-vetting`](./package-security-vetting) | Audit third-party packages, prevent typosquatting/dependency confusion, and lock dependency hashes. | `add a dependency`, `npm install`, `pip install`, `is package safe` |
| [`secrets-and-config-management`](./secrets-and-config-management) | Separate secrets from config, enforce `.env.example`, CI vaults, secret rotation, and Gitleaks scanning. | `add an API key`, `store credential`, `committed secret`, `secrets in CI` |
| [`testing-strategy`](./testing-strategy) | Structure test pyramids, test contracts over implementation details, eliminate flaky tests, and framework idioms. | `write tests for this`, `what should I test`, `test is flaky`, `test coverage` |
| [`ui-clone-skill`](./ui-clone-skill) | Screenshot-to-code UI cloning, design system tokenization, and custom multi-stack component generation. | `clone this UI`, `screenshot to code`, `build component library` |
| [`universal-coding-standards`](./universal-coding-standards) | 10 universal engineering pillars (naming, error handling, SRP, security, testing) across any language. | `write code`, `refactor this`, `is this good code`, `clean code standards` |

---

## Directory Structure

Each skill follows the `agentskills.io` specification with progressive disclosure:

```text
skill-name/
├── SKILL.md             # Core instructions, frontmatter metadata, and operational checklist
└── references/          # Deep documentation, language deltas, worked examples, and templates
```

---

## Installation & Usage

### Antigravity IDE / Gemini
Copy any skill folder into your project's customization directory:
```bash
# Workspace level:
mkdir -p .agents/skills
cp -r /path/to/skill-name .agents/skills/

# Or global configuration:
mkdir -p ~/.gemini/config/skills
cp -r /path/to/skill-name ~/.gemini/config/skills/
```

### Other AI Coding Agents (Claude Code, Cursor, Copilot)
Point your agent at the target `SKILL.md` or add it to your project's agent rules. The agent will read the operational checklist and load reference files on demand.

---

## Author

Created and maintained by **[@ygohel18](https://github.com/ygohel18)**.

## License

[MIT](LICENSE)
