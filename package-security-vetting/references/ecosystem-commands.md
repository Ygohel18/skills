# Ecosystem Package Management & Security Audit Commands

> Companion reference for `package-security-vetting`.
> Contains canonical audit, lockfile verification, safe installation, and pruning commands across major language ecosystems.

---

## 1. Node.js (npm / pnpm / yarn)

| Action | `npm` | `pnpm` | `yarn` (v2+ Berry / v4) |
|---|---|---|---|
| **Vulnerability Audit** | `npm audit` / `npm audit --omit=dev` | `pnpm audit` | `yarn npm audit` |
| **Lockfile Name** | `package-lock.json` | `pnpm-lock.yaml` | `yarn.lock` |
| **Strict CI Install** | `npm ci` | `pnpm install --frozen-lockfile` | `yarn install --immutable` |
| **Disable Lifecycle Scripts** | `npm install --ignore-scripts` | `pnpm add --ignore-scripts` | `yarn install --mode=skip-build` |
| **Integrity Verification** | Automatically enforced via `integrity` SHA-512 hashes in `package-lock.json` | Checked via content-addressable store & `pnpm-lock.yaml` | Enforced via checksums in `yarn.lock` |
| **Outdated Check** | `npm outdated` | `pnpm outdated` | `yarn outdated` |
| **Prune Unused** | `npm prune` | `pnpm prune` | Built-in |

> **Pro Tip:** In `package.json`, inspect the `"scripts"` field of third-party dependencies before installing, looking for `preinstall`, `install`, or `postinstall` entries executing `node`, `curl`, or `bash`.

---

## 2. Python (uv / pip / poetry / pipenv)

| Action | `uv` (Modern standard) | `pip` + `pip-audit` | `poetry` |
|---|---|---|---|
| **Vulnerability Audit** | `uv audit` | `pip-audit` (or `pip-audit -r requirements.txt`) | `poetry run pip-audit` |
| **Lockfile Name** | `uv.lock` | `requirements.lock` / `requirements.txt` with `--hash` | `poetry.lock` |
| **Strict CI Install** | `uv sync --frozen` | `pip install --no-deps --require-hashes -r requirements.lock` | `poetry install --no-root --sync` |
| **Generate Hashes** | Built-in to `uv.lock` | `pip-compile --generate-hashes requirements.in` | Built-in to `poetry.lock` |
| **Malware Prevention** | `UV_MALWARE_CHECK=1 uv sync` | Manual inspection / OSV scanner | Manual inspection |
| **Outdated Check** | `uv pip list --outdated` | `pip list --outdated` | `poetry show --outdated` |

> **Pro Tip:** Always avoid bare `pip install <package>` in global environments. Restrict builds to binary wheels (`pip install --only-binary :all: <pkg>`) to prevent arbitrary code execution inside legacy `setup.py` scripts.

---

## 3. Go (Go Modules & Toolchain)

| Action | Go Command | Notes |
|---|---|---|
| **Vulnerability Audit** | `govulncheck ./...` | Official Go vulnerability scanner backed by the Go vulnerability database (`vuln.go.dev`). Install via `go install golang.org/x/vuln/cmd/govulncheck@latest`. |
| **Lockfile & Hashes** | `go.mod` and `go.sum` | `go.sum` contains cryptographic SHA-256 hashes of module contents and `go.mod` files. |
| **Strict Verification** | `go mod verify` | Verifies that dependencies on disk match the cryptographic hashes recorded in `go.sum`. Run in CI! |
| **Tidy & Prune** | `go mod tidy` | Adds missing modules and removes unused modules from `go.mod` and `go.sum`. |
| **Download Only** | `go mod download` | Pre-fetches modules into local cache without executing build code. |

---

## 4. PHP (Composer)

| Action | Composer Command | Notes |
|---|---|---|
| **Vulnerability Audit** | `composer audit` | Built natively into Composer (v2.4+). Checks the FriendsOfPHP security advisory database and Packagist advisories. |
| **Lockfile Name** | `composer.lock` | Contains locked versions, commit references, and package content hashes (`content-hash`). |
| **Strict CI Install** | `composer install --no-dev --no-interaction --prefer-dist` | Installs exact versions from `composer.lock`. |
| **Disable Execution** | `composer install --no-scripts --no-plugins` | **Crucial:** Blocks execution of third-party Composer plugins and lifecycle scripts during installation. |
| **Outdated Check** | `composer outdated --direct` | Highlights direct dependencies with newer releases. |

---

## 5. Rust (Cargo)

| Action | Cargo Command | Notes |
|---|---|---|
| **Vulnerability Audit** | `cargo audit` | Uses the RustSec Advisory Database (`cargo-audit` crate). |
| **Lockfile Name** | `Cargo.lock` | Contains exact versions and `checksum` hashes of all crates. |
| **Strict CI Build** | `cargo build --locked` | Fails immediately if `Cargo.lock` requires updates. |
| **Policy / License Audit** | `cargo deny check` | `cargo-deny` checks advisories, licenses, bans, and duplicate crates. |
| **Outdated Check** | `cargo outdated` | Requires `cargo-outdated` crate. |

---

## 6. Ruby (Bundler & RubyGems)

| Action | Bundler Command | Notes |
|---|---|---|
| **Vulnerability Audit** | `bundle exec bundle-audit check --update` | Uses `bundler-audit` gem against the Ruby Advisory Database. |
| **Lockfile Name** | `Gemfile.lock` | Contains resolved gem versions and SHA-256 checksums. |
| **Strict CI Install** | `bundle config set --local deployment 'true' && bundle install` | Enforces exact lockfile dependencies in CI. |
| **Outdated Check** | `bundle outdated --strict` | Lists outdated direct gems. |

---

## 7. Java / Kotlin (Maven & Gradle)

| Action | Maven | Gradle |
|---|---|---|
| **Vulnerability Audit** | `mvn org.owasp:dependency-check-maven:check` | `./gradlew dependencyCheckAnalyze` |
| **Lockfile Support** | Extension / `pom.xml` exact versions | `./gradlew dependencies --write-locks` (`gradle.lockfile`) |
| **Strict CI Enforce** | `mvn verify` | `./gradlew build --dependency-locking` |
| **Dependency Tree** | `mvn dependency:tree` | `./gradlew dependencies` |

---

## 8. C# / .NET (NuGet)

| Action | .NET CLI Command | Notes |
|---|---|---|
| **Vulnerability Audit** | `dotnet list package --vulnerable` | Queries the GitHub Advisory Database and NuGet security feed. Add `--include-transitive` for full depth. |
| **Lockfile Name** | `packages.lock.json` | Enable by setting `<RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>` in `.csproj`. |
| **Strict CI Restore** | `dotnet restore --locked-mode` | Fails build if lockfile does not match project file. |
| **Outdated Check** | `dotnet list package --outdated` | Lists direct dependencies with newer versions. |
