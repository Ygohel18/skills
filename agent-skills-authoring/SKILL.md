---
name: agent-skills-authoring
description: Create, validate, and structure Agent Skills (SKILL.md files and skill folders) per the open agentskills.io specification. Use when the user wants to write a new skill, package instructions for an AI agent, fix a SKILL.md's frontmatter, or asks about the Agent Skills format, progressive disclosure, or making a skill portable across Claude Code, Cursor, Codex, Gemini CLI, and other compatible agents.
license: CC-BY-4.0 (docs reference); no license implied for generated skills
metadata:
  source: https://agentskills.io/home
  spec_version: "2026-09"
---

# Agent Skills Authoring

Agent Skills are an open, portable format (agentskills.io) for giving AI
agents new capabilities: a folder containing a required `SKILL.md` plus
optional `scripts/`, `references/`, and `assets/`. This skill tells you how
to write one correctly.

## When to use this

- The user asks you to "make a skill" for some task, tool, or piece of
  domain knowledge.
- The user has a rough set of instructions, a playbook, or a workflow they
  want turned into a reusable `SKILL.md`.
- The user asks you to validate, fix, or restructure an existing skill.
- The user asks what Agent Skills are, how progressive disclosure works, or
  which clients support the format.

## Directory structure

A skill is a folder whose name matches the skill's `name` field:

```
skill-name/
├── SKILL.md          # Required: YAML frontmatter + Markdown instructions
├── scripts/           # Optional: executable code (Python/Bash/JS)
├── references/        # Optional: docs loaded only when needed
└── assets/             # Optional: templates, images, data files
```

Only `SKILL.md` is required. Everything else is created on demand.

## Step-by-step: writing a new skill

1. **Name it.** Pick a `name`: lowercase letters, digits, and hyphens only,
   1-64 characters, no leading/trailing/consecutive hyphens (`pdf-processing`,
   not `PDF-Processing` or `-pdf`). It must match the folder name exactly.

2. **Write the description first.** This is the single most important line
   in the file — it is the *only* thing loaded into an agent's context at
   startup, for every skill it has. Write it so a task description could be
   matched against it. State both what the skill does and when to use it,
   and include the concrete keywords a user's message would contain.

   - Good: `Extracts text and tables from PDF files, fills PDF forms, and
     merges multiple PDFs. Use when working with PDF documents or when the
     user mentions PDFs, forms, or document extraction.`
   - Poor: `Helps with PDFs.`

3. **Draft the frontmatter.** Minimum viable frontmatter is just `name` and
   `description`. Add the optional fields only if they earn their place (see
   `references/frontmatter-fields.md` for the full field table and
   constraints).

4. **Write the body.** After the frontmatter, write plain Markdown — there's
   no required structure. What tends to work well:
   - Step-by-step instructions (numbered, like this list)
   - Concrete examples of inputs and outputs
   - Common edge cases and how to handle them
   - Links to `references/*.md` for anything long, using relative paths,
     e.g. `See [the reference guide](references/REFERENCE.md).`

5. **Keep it lean.** Target under 500 lines / ~5000 tokens for `SKILL.md`
   itself. If the domain knowledge is bigger than that, split the detail
   into `references/` files and point to them from the main file — the
   agent only loads a reference file when it actually needs it. Keep
   references one level deep; avoid chains of files pointing to other files.

6. **Add scripts/assets only if useful.** `scripts/` holds executable code
   the agent can run instead of writing from scratch (self-contained,
   documented dependencies, clear error messages). `assets/` holds templates,
   images, or data files the instructions reference but don't need to read
   as text.

7. **Validate.** If the `skills-ref` CLI is available, run
   `skills-ref validate ./skill-name` to check the frontmatter against the
   spec. Otherwise, hand-check against `references/frontmatter-fields.md`.

## Why the format works this way: progressive disclosure

Agents load skills in three stages, and a well-written skill is structured
around this:

1. **Discovery** (~100 tokens) — only `name` + `description`, for every
   skill, all the time. This is why the description has to be dense and
   specific.
2. **Activation** — when a task matches, the full `SKILL.md` body loads.
3. **Execution** — the agent follows the instructions, running bundled
   scripts or reading referenced files only as the task actually requires.

Writing for this means: put the searchable keywords in the description, put
the load-bearing how-to in the body, and put everything else in
`references/`, `scripts/`, or `assets/` so it costs nothing until needed.

## Common mistakes to avoid

- Vague descriptions ("helps with X") that never trigger on real tasks.
- `name` that doesn't match the folder name, or uses uppercase/underscores.
- Cramming a full reference manual into `SKILL.md` instead of splitting it
  into `references/`.
- Deeply nested reference chains (a reference file pointing to another
  reference file pointing to another).
- Adding `compatibility` or `allowed-tools` when the skill has no real
  environment requirements — most skills don't need either field.

## Reference

- `references/frontmatter-fields.md` — full field-by-field spec (required
  fields, character limits, valid/invalid examples) for `name`,
  `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`.

Full upstream docs: https://agentskills.io/specification and
https://agentskills.io/home. The format was originated by Anthropic,
released as an open standard, and is now supported by Claude Code, Cursor,
Codex, Gemini CLI, VS Code Copilot, Goose, and dozens of other agent clients.
