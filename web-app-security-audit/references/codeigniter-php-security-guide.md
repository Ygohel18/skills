# CodeIgniter & Legacy PHP Security Audit Guide

A security engineering reference covering vulnerability paths, dangerous sinks, and defensive patterns in CodeIgniter (CI3 & CI4) and standalone PHP applications.

---

## 1. SQL Injection in CodeIgniter Database Queries

CodeIgniter's Query Builder parameterizes calls like `$this->db->get_where()`. However, calling `$this->db->query()` with string concatenation executes raw SQL without automatic escaping.

### Vulnerable Calls
```php
// ❌ VULNERABLE: Direct string concatenation into query()
$username = $this->input->post('username');
$sql = "SELECT * FROM users WHERE username = '" . $username . "'";
$query = $this->db->query($sql);

// ❌ VULNERABLE (CI4):
$db = \Config\Database::connect();
$query = $db->query("SELECT * FROM products WHERE category = '" . $_GET['cat'] . "'");
```

### Remediated Calls
```php
// ✅ SECURE: Parameterized query bindings (?)
$sql = "SELECT * FROM users WHERE username = ? AND status = ?";
$query = $this->db->query($sql, [$username, 'active']);

// ✅ SECURE: Use Query Builder methods
$query = $this->db->where('username', $username)->get('users');
```

---

## 2. CSRF Protection Disabled

CodeIgniter provides built-in CSRF protection, but legacy projects frequently disable it to bypass form token mismatch errors.

### Vulnerable Configuration (CI3)
```php
// application/config/config.php
// ❌ VULNERABLE: CSRF protection turned off
$config['csrf_protection'] = FALSE;

// ✅ SECURE: Enforce CSRF protection with cookie regeneration
$config['csrf_protection'] = TRUE;
$config['csrf_token_name'] = 'csrf_token_app';
$config['csrf_cookie_name'] = 'csrf_cookie_app';
$config['csrf_expire'] = 7200;
$config['csrf_regenerate'] = TRUE;
```

---

## 3. Disabling XSS Filtering on Input

In CodeIgniter 3, `$this->input->post('field', TRUE)` applies XSS filtering, but developers often pass `FALSE` or access `$_POST` directly without escaping output.

```php
// ❌ VULNERABLE: Explicitly turning off XSS filtering and direct echo
$comment = $this->input->post('comment', FALSE);
echo "<div>" . $comment . "</div>";

// ✅ SECURE (CI4): Use esc() output helper
echo "<div>" . esc($comment, 'html') . "</div>";
```

---

## 4. CodeIgniter Auto-Routing Vulnerabilities

In older CodeIgniter 3 and early CI4 installations, auto-routing (`$routes->setAutoRoute(true)`) automatically maps URL segments (`/controller/method/arg1`) to controller public methods.

- **Risk:** If a controller defines a helper method as `public` (e.g. `public function deleteUser($id)` or `public function resetDatabase()`), an external attacker can invoke it directly via URL.
- **Remediation:**
  - In CI4: Disable auto-routing in `app/Config/Routes.php`:
    ```php
    $routes->setAutoRoute(false);
    ```
  - Mark internal controller methods as `protected` or `private`.
