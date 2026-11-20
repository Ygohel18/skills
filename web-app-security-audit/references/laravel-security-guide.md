# Laravel & PHP Security Audit Guide

A comprehensive security engineering manual covering vulnerability paths, dangerous sinks, and defensive patterns in Laravel and modern PHP web applications.

---

## 1. Debug Mode & Environment Exposure

### 1.1 `APP_DEBUG=true` in Production
- **Risk:** Uncaught exceptions display full stack traces, complete environment variables (including database passwords, AWS keys, mail credentials), and database query parameters.
- **Historic Exploitation (CVE-2021-3129):** Older Laravel Ignition error pages allowed unauthenticated Remote Code Execution (RCE) by abusing the `_ignition/execute-solution` endpoint with PHP wrapper log poisoning (`php://filter/write=convert.base64-decode`).
- **Remediation:**
  ```ini
  # .env (Production)
  APP_DEBUG=false
  APP_ENV=production
  ```

### 1.2 `APP_KEY` Leakage & Deserialization
- **Risk:** The `APP_KEY` (AES-256-CBC or AES-128-CBC key) encrypts session cookies. In older Laravel versions, encrypted cookie payloads were directly unserialized via `unserialize()`. An attacker possessing the `APP_KEY` can forge signed cookies containing custom POP (Property-Oriented Programming) gadget chains (e.g. from Monolog, Guzzle, or Symfony packages) leading to RCE.
- **Remediation:**
  - Never commit `.env` or hardcode `APP_KEY` in `config/app.php`.
  - Rotate the key immediately if exposed: `php artisan key:generate`.
  - Ensure Laravel is on version 10+ where cookie serialization uses HMAC-verified JSON rather than raw PHP `unserialize`.

### 1.3 Exposed `.env` via Incorrect Web Server Root
- **Risk:** If Apache or Nginx `root` points to `/var/www/laravel` instead of `/var/www/laravel/public`, navigating to `https://example.com/.env` downloads the raw environment file.
- **Remediation (Nginx):**
  ```nginx
  server {
      root /var/www/laravel/public;
      index index.php;

      # Block access to hidden files
      location ~ /\. {
          deny all;
      }
  }
  ```

---

## 2. Model Mass Assignment

### Vulnerable Pattern
```php
// ❌ VULNERABLE: $guarded = [] or unvalidated $request->all()
class User extends Model {
    protected $guarded = []; // Disables mass assignment protection
}

// Controller
public function update(Request $request, User $user) {
    // Attacker sends: {"name": "Alice", "is_admin": true, "role": "superadmin"}
    $user->update($request->all()); 
}
```

### Remediated Pattern
```php
// ✅ SECURE: Explicit $fillable attributes
class User extends Model {
    protected $fillable = [
        'name',
        'email',
        'avatar_url',
    ];
}

// ✅ SECURE: Use validated FormRequest
public function update(UpdateUserProfileRequest $request, User $user) {
    $user->update($request->validated());
}
```

---

## 3. SQL Injection in Raw Database Methods

Eloquent and the Query Builder parameterize standard clauses (`where()`, `find()`, `first()`). However, raw SQL helper methods do **not** escape inputs if passed as concatenated strings.

### Vulnerable Calls
```php
// ❌ VULNERABLE: String concatenation in whereRaw
$users = DB::table('users')
    ->whereRaw("email = '" . $request->input('email') . "'")
    ->get();

// ❌ VULNERABLE: Interpolated order by
$posts = Post::orderByRaw("created_at " . $request->input('direction'))->get();
```

### Remediated Calls
```php
// ✅ SECURE: Parameterized bindings
$users = DB::table('users')
    ->whereRaw("email = ?", [$request->input('email')])
    ->get();

// ✅ SECURE: Strict direction allow-listing
$direction = in_array(strtolower($request->input('direction')), ['asc', 'desc']) 
    ? $request->input('direction') 
    : 'desc';
$posts = Post::orderBy('created_at', $direction)->get();
```

---

## 4. Blade Cross-Site Scripting (XSS)

- Auto-escaped syntax: `{{ $content }}` runs through `htmlspecialchars($content, ENT_QUOTES, 'UTF-8')`.
- Unescaped syntax: `{!! $content !!}` bypasses escaping completely.

```blade
<!-- ❌ VULNERABLE: Direct rendering of user input -->
<div class="user-bio">
    {!! $user->bio !!}
</div>

<!-- ✅ SECURE: Auto-escaped output -->
<div class="user-bio">
    {{ $user->bio }}
</div>

<!-- ✅ SECURE: If rich text is required, sanitize through HTMLPurifier -->
<div class="user-bio">
    {!! clean($user->bio) !!}
</div>
```

---

## 5. Insecure Deserialization & File Uploads

### Insecure Deserialization
```php
// ❌ VULNERABLE: Native unserialize on request payload
$state = unserialize($request->input('saved_state'));

// ✅ SECURE: JSON decoding
$state = json_decode($request->input('saved_state'), true, 512, JSON_THROW_ON_ERROR);
```

### Unsafe File Uploads
```php
// ❌ VULNERABLE: Trusting user-provided extension
$file = $request->file('avatar');
$file->move(public_path('uploads'), $file->getClientOriginalName()); // e.g. shell.php

// ✅ SECURE: Validate MIME type, store in private storage, generate random hash
$request->validate([
    'avatar' => 'required|file|image|mimes:jpeg,png,webp|max:2048',
]);
$path = $request->file('avatar')->store('avatars', 'private');
```
