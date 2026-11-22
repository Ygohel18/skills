# Dependency Directory Guardrails & Package Manager Restrictions

A strict operational standard forbidding unauthorized inspection, traversal, and execution inside third-party dependency environments.

---

## 1. The Core Threat: Context Pollution & Unintended Mutations

AI coding agents often make two catastrophic mistakes:
1. **Dumping Vendor Source into Context:** A simple search or recursive listing pulls thousands of lines from `node_modules/` or `vendor/`. This swamps the context window with third-party code that the agent is not tasked with editing, driving up token costs and diluting reasoning capacity.
2. **Executing Side-Effect Heavy Package Operations:** The agent unilaterally runs `npm install`, `composer update`, or `pip install`. This mutates lockfiles, triggers postinstall scripts, breaks frozen build environments, or introduces version drift across hundreds of dependencies.

---

## 2. Strictly Banned Directories

Under no circumstances may an agent read, grep, or traverse the following paths unless the user explicitly names a file inside them:

| Stack | Forbidden Directories & Files |
|---|---|
| **Node.js / JS / TS** | `node_modules/`, `.pnpm-store/`, `.yarn/`, `package-lock.json` *(editing)*, `yarn.lock`, `pnpm-lock.yaml` |
| **PHP / Composer** | `vendor/`, `composer.lock` *(editing)* |
| **Python** | `.venv/`, `venv/`, `env/`, `site-packages/`, `__pycache__/`, `poetry.lock` *(editing)*, `Pipfile.lock` |
| **Ruby** | `vendor/bundle/`, `Gemfile.lock` *(editing)* |
| **Rust / Go** | `target/`, `vendor/`, `Cargo.lock` *(editing)* |
| **Build Outputs** | `.next/`, `dist/`, `build/`, `out/`, `.nuxt/`, `.svelte-kit/`, `coverage/` |

---

## 3. Explicit Command Prohibitions

Unless the user's prompt contains an explicit instruction like *"install package X"* or *"run composer update"*, the agent is **strictly prohibited from executing**:

- 🚫 `npm install`, `npm i`, `npm update`, `npm audit fix`, `npx <untrusted-pkg>`
- 🚫 `yarn install`, `yarn add`, `yarn upgrade`
- 🚫 `pnpm install`, `pnpm add`, `pnpm update`
- 🚫 `composer install`, `composer update`, `composer require`
- 🚫 `pip install`, `poetry install`, `pipenv install`
- 🚫 `cargo update`, `bundle install`, `go get -u`

### Why?
1. Existing repositories rely on pinned dependency hashes. Updating changes the runtime environment unpredictably.
2. Installing packages in sandboxed or isolated test environments can trigger network timeouts or permission errors.
3. Your role as an IDE coding agent is to implement features and fix bugs using the **existing installed ecosystem**.

---

## 4. How to Exclude Dependencies in Terminal Commands

Always pass exclusion flags when using shell utilities:

### `grep`
```bash
# ✅ SECURE & EFFICIENT: Exclude vendor directories
grep -rn "PaymentGateway" ./src \
  --exclude-dir=node_modules \
  --exclude-dir=vendor \
  --exclude-dir=.git \
  --exclude-dir=dist
```

### `find`
```bash
# ✅ SECURE & EFFICIENT: Prune dependency directories
find . \( -name node_modules -o -name vendor -o -name .git -o -name dist \) -prune -o -name "*.ts" -print
```

### `rg` (Ripgrep)
Ripgrep automatically respects `.gitignore` rules, naturally ignoring `node_modules` and `vendor`.
