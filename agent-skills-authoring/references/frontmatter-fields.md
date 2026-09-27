# SKILL.md frontmatter — full field reference

Source: https://agentskills.io/specification

`SKILL.md` must contain YAML frontmatter followed by Markdown content.

| Field           | Required | Constraints                                                                                            |
| --------------- | -------- | ------------------------------------------------------------------------------------------------------ |
| `name`          | Yes      | Max 64 chars. Lowercase letters, numbers, hyphens only. No leading/trailing hyphen.                     |
| `description`   | Yes      | Max 1024 chars. Non-empty. States what the skill does and when to use it.                               |
| `license`       | No       | License name, or a reference to a bundled license file.                                                 |
| `compatibility` | No       | Max 500 chars. Environment requirements (target product, system packages, network access).              |
| `metadata`      | No       | Arbitrary string-to-string map for extra properties not covered by the spec.                            |
| `allowed-tools` | No       | Space-separated string of pre-approved tools. Experimental — support varies by agent.                   |

## Minimal example

```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

## Example with optional fields

```yaml
---
name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
---
```

## `name`

- 1-64 characters.
- Unicode lowercase alphanumeric (`a-z`, `0-9`) and hyphens (`-`) only.
- Must not start or end with a hyphen.
- Must not contain consecutive hyphens (`--`).
- Must match the parent directory name exactly.

Valid: `pdf-processing`, `data-analysis`, `code-review`
Invalid: `PDF-Processing` (uppercase), `-pdf` (leading hyphen),
`pdf--processing` (consecutive hyphens)

## `description`

- 1-1024 characters.
- Should describe both *what* the skill does and *when* to use it.
- Should include the specific keywords a real task would contain, since this
  is the only field an agent sees before deciding to load the full skill.

Good: `Extracts text and tables from PDF files, fills PDF forms, and merges
multiple PDFs. Use when working with PDF documents or when the user mentions
PDFs, forms, or document extraction.`

Poor: `Helps with PDFs.`

## `license`

- Optional. Keep it short: either a license name (`Apache-2.0`) or a pointer
  to a bundled license file (`Proprietary. LICENSE.txt has complete terms`).

## `compatibility`

- Optional, 1-500 characters if present.
- Only include it when the skill has real environment requirements —
  intended product, required system packages, network access, etc.
- Most skills do **not** need this field.

Examples:
```yaml
compatibility: Designed for Claude Code (or similar products)
compatibility: Requires git, docker, jq, and access to the internet
compatibility: Requires Python 3.14+ and uv
```

## `metadata`

- Optional map from string keys to string values.
- Clients can use it to store properties the spec itself doesn't define.
- Recommend reasonably unique key names to avoid collisions.

```yaml
metadata:
  author: example-org
  version: "1.0"
```

## `allowed-tools`

- Optional, space-separated string of tools pre-approved to run.
- Experimental — behavior may vary between agent implementations.

```yaml
allowed-tools: Bash(git:*) Bash(jq:*) Read
```

## Progressive disclosure budget

1. Metadata (`name` + `description`) — always loaded, ~100 tokens.
2. Full `SKILL.md` body — loaded on activation, keep under ~5000 tokens /
   500 lines.
3. `scripts/`, `references/`, `assets/` — loaded only when the instructions
   actually reference them.

## Validation

If the `skills-ref` reference library is available:

```bash
skills-ref validate ./my-skill
```

Repo: https://github.com/agentskills/agentskills/tree/main/skills-ref
