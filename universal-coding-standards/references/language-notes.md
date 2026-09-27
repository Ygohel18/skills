# Language-Specific Engineering Notes & Deltas

> Reference companion for `universal-coding-standards`. Consult when writing or reviewing code in specific languages to reconcile generic principles with ecosystem idioms.

---

## 1. Naming & Case Conventions Summary

| Language | Variables & Fields | Functions & Methods | Types & Classes | Constants | Files / Modules |
|---|---|---|---|---|---|
| **Python** | `snake_case` | `snake_case` | `PascalCase` | `SCREAMING_SNAKE` | `snake_case.py` |
| **JavaScript / TypeScript** | `camelCase` | `camelCase` | `PascalCase` | `SCREAMING_SNAKE` (true consts) | `kebab-case.ts` or `camelCase.ts` |
| **Go** | `camelCase` / `PascalCase` (exported) | `camelCase` / `PascalCase` (exported) | `PascalCase` / `camelCase` | `camelCase` / `PascalCase` | `snake_case.go` |
| **Rust** | `snake_case` | `snake_case` | `PascalCase` | `SCREAMING_SNAKE` | `snake_case.rs` |
| **Java** | `camelCase` | `camelCase` | `PascalCase` | `SCREAMING_SNAKE` | `PascalCase.java` (matches class) |
| **C# (.NET)** | `camelCase` (`_camelCase` for private fields) | `PascalCase` | `PascalCase` | `PascalCase` or `SCREAMING_SNAKE` | `PascalCase.cs` |
| **PHP** | `camelCase` or `$snake_case` | `camelCase` | `PascalCase` | `SCREAMING_SNAKE` | `PascalCase.php` (PSR-4 classes) |
| **Ruby** | `snake_case` | `snake_case` (`?` for predicate, `!` for dangerous) | `PascalCase` | `SCREAMING_SNAKE` | `snake_case.rb` |
| **C / C++** | `snake_case` / `m_camelCase` | `snake_case` / `camelCase` | `PascalCase` / `snake_case_t` | `SCREAMING_SNAKE` | `snake_case.cpp` / `snake_case.hpp` |

---

## 2. Tooling, Formatters & Linters

Always defer to project-level configuration (`.editorconfig`, `.prettierrc`, `ruff.toml`, etc.). If unconfigured, invoke the canonical ecosystem defaults:

| Language | Canonical Formatter | Primary Linter / Static Analysis | Package / Dependency Manager |
|---|---|---|---|
| **Python** | `ruff format` or `black` | `ruff check` or `flake8` + `mypy` | `uv`, `poetry`, or `pip-tools` (`requirements.txt.lock`) |
| **JS / TS** | `prettier` or `biome format` | `eslint` or `biome lint`, `tsc --noEmit` | `pnpm-lock.yaml`, `package-lock.json`, `bun.lockb` |
| **Go** | `gofmt` / `goimports` | `golangci-lint` | `go.mod` + `go.sum` |
| **Rust** | `rustfmt` | `cargo clippy -- -D warnings` | `Cargo.lock` |
| **Java** | `google-java-format` or `Spotless` | `Checkstyle`, `SonarQube`, `SpotBugs` | `pom.xml` (Maven) or `gradle.lockfile` |
| **C#** | `dotnet format` | `dotnet format analyzers`, Roslyn analyzers | NuGet (`packages.lock.json` or `.csproj`) |
| **PHP** | `PHP-CS-Fixer` or `Laravel Pint` | `PHPStan` (level 5+), `Psalm` | `composer.lock` |
| **Ruby** | `rubocop -a` | `rubocop`, `brakeman` (security) | `Gemfile.lock` |
| **C / C++** | `clang-format` | `clang-tidy`, `cppcheck` | `CMakePresets.json`, `conan.lock`, `vcpkg.json` |

---

## 3. Idiomatic Error Handling Patterns

### Python
- **Idiom:** EAFP (*Easier to Ask for Forgiveness than Permission*). Raise specific built-in or custom exceptions inheriting from `Exception`.
- **Anti-pattern:** `except:` or `except Exception:` with `pass` (silently swallowing bugs).
- **Correct Pattern:**
  ```python
  try:
      record = fetch_record(user_id)
  except RecordNotFoundError as err:
      logger.warning("User %s record missing", user_id, exc_info=err)
      return None
  except DatabaseConnectionError:
      logger.error("Database connection failure fetching %s", user_id)
      raise
  ```

### JavaScript / TypeScript
- **Idiom:** Always throw `Error` objects, never plain strings, numbers, or objects (`throw new Error(...)` vs `throw "failed"`).
- **TypeScript:** When typing catch blocks, treat errors as `unknown`:
  ```typescript
  try {
    await processPayment(payload);
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : "Unknown payment error";
    logger.error("Payment failed", { error: message });
    throw new PaymentProcessingError(message, { cause: error });
  }
  ```

### Go
- **Idiom:** Multiple returns `(value, error)`. Always check `if err != nil` immediately.
- **Rules:** Never ignore return errors (`val, _ := fn()`). Wrap context with `fmt.Errorf("failed fetching account %s: %w", id, err)`.
  ```go
  res, err := client.Fetch(ctx, id)
  if err != nil {
      return nil, fmt.Errorf("fetch customer %s: %w", id, err)
  }
  ```

### Rust
- **Idiom:** `Result<T, E>` and `Option<T>` with pattern matching or the `?` propagation operator.
- **Rules:** Avoid `.unwrap()` and `.expect()` in production library or server code. Reserve `.expect("invariant: explanation")` strictly for provable internal invariants.
  ```rust
  let user = repository
      .find_by_id(user_id)
      .map_err(|e| UserError::DatabaseError(format!("query failed for {user_id}: {e}")))?;
  ```

### Java / C#
- **Idiom:** Use checked exceptions (Java) or typed runtime exceptions (C# / Java) for recoverable conditions. Use unchecked exceptions for programming bugs.
- **Rules:** Preserve the original stack trace when wrapping exceptions (`throw new ServiceException("Failed to load user", innerException)`).

---

## 4. Per-Language Security Footguns & Traps

### Python
1. **Mutable default arguments:** `def add_item(item, target=[])` causes shared state across calls. Always use `target=None` and initialize inside the function.
2. **Dynamic code execution:** Never use `eval()`, `exec()`, or unverified `pickle.loads()` on untrusted external data.
3. **Subprocess injection:** Use `subprocess.run(["cmd", arg1, arg2], check=True, shell=False)` instead of `shell=True`.

### JavaScript / TypeScript
1. **Loose equality (`==`):** Type coercion causes subtle bugs (`"" == 0` is `true`). Always enforce `===` and `!==`.
2. **Prototype pollution:** When merging user-provided JSON objects into existing objects, sanitize or block `__proto__`, `constructor`, and `prototype`.
3. **ReDoS (Regular Expression Denial of Service):** Avoid catastrophic backtracking regex on untrusted input strings.
4. **Client-side auth assumption:** Never trust clientside route guards or JWT payload claims without backend signature verification.

### Go
1. **Ignored error returns:** Discarding `err` with `_` creates silent logic corruption.
2. **Goroutine leaks:** Launching goroutines without a terminating `context.Context` or channel drain creates memory/CPU exhaustion.
3. **Loop variable capture (pre-Go 1.22):** In Go < 1.22, taking a pointer to a loop variable captures the shared iteration pointer rather than the per-iteration value.

### Rust
1. **Unnecessary `unsafe`:** `unsafe` should be strictly confined, provably bounded, and accompanied by a `// SAFETY: ...` explanation comment.
2. **Unbounded memory allocation:** Always validate sizes before allocating vectors or reading streams from network inputs (`Vec::with_capacity(user_input_size)`).

### Java / C#
1. **Unsafe deserialization:** Java `ObjectInputStream` and .NET `BinaryFormatter` deserializing untrusted streams lead directly to Remote Code Execution (RCE). Use JSON/Protobuf with strict schema validation.
2. **SQL concatenation:** Never construct SQL queries with string interpolation (`"SELECT * FROM users WHERE id = " + id`). Always use parameterized queries / prepared statements.

### PHP
1. **Type juggling / Loose comparison:** `in_array($val, $arr)` defaults to loose comparison. Always pass strict flag: `in_array($val, $arr, true)`.
2. **Direct variable output in Blade / Twig / HTML:** Avoid unescaped `{!! $var !!}` when rendering user data to prevent Cross-Site Scripting (XSS).

### Ruby
1. **SQL injection in ActiveRecord:** Dynamic parameters in string fragments: `User.where("name = '#{params[:name]}'")`. Always use parameterized form: `User.where(name: params[:name])`.
2. **Unsafe YAML loading:** Use `YAML.safe_load` instead of `YAML.load` to avoid object instantiation vulnerabilities.
