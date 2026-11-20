# Node.js Security Audit Guide

A security engineering reference covering critical vulnerabilities in Node.js applications, runtime execution risks, event loop starvation, and supply-chain threats.

---

## 1. OS Command Injection

Node.js executes shell commands through the `child_process` module. Calling `exec()` or `execSync()` spawns a subshell (`/bin/sh` or `cmd.exe`), which interprets shell metacharacters (`|`, `&`, `;`, `$()`, `` ` ``).

### Vulnerable Pattern
```javascript
const { exec } = require('node:child_process');

// ❌ VULNERABLE: User input concatenated into shell command
app.get('/api/ping', (req, res) => {
  const host = req.query.host; // e.g. "8.8.8.8; rm -rf /"
  exec(`ping -c 3 ${host}`, (err, stdout) => {
    res.send(stdout);
  });
});
```

### Remediated Pattern
```javascript
const { execFile } = require('node:child_process');

// ✅ SECURE: execFile bypasses shell; arguments passed as discrete array elements
app.get('/api/ping', (req, res) => {
  const host = String(req.query.host);
  
  // Validate format (e.g. valid IP or hostname)
  if (!/^[a-zA-Z0-9.-]+$/.test(host)) {
    return res.status(400).send("Invalid host parameter");
  }

  execFile('ping', ['-c', '3', host], (err, stdout) => {
    if (err) return res.status(500).send("Ping failed");
    res.send(stdout);
  });
});
```

---

## 2. Dynamic Code Evaluation (`eval`, `new Function`, `vm`)

Node's `vm` module is **not a security sandbox**. Code executed inside `vm.runInContext()` or `vm.runInNewContext()` can traverse `this.constructor.constructor('return process')()` to escape the context and execute arbitrary system commands.

```javascript
// ❌ VULNERABLE: Dynamic function generation or eval
const calculate = new Function('input', `return ${req.body.expression};`);

// ✅ SECURE: Use static math expression parsers (e.g. mathjs with disabled execution)
import { evaluate } from 'mathjs';
// Restrict available scope and functions
```

---

## 3. Prototype Pollution

Prototype pollution occurs when user input modifies properties on `Object.prototype`. Because JavaScript inherits properties up the prototype chain, polluted properties affect all objects in the runtime.

### Vulnerable Recursive Merge
```javascript
// ❌ VULNERABLE: Unsafe recursive object merge
function deepMerge(target, source) {
  for (const key in source) {
    if (typeof source[key] === 'object' && source[key] !== null) {
      if (!target[key]) target[key] = {};
      deepMerge(target[key], source[key]); // Attacker passes {"__proto__": {"isAdmin": true}}
    } else {
      target[key] = source[key];
    }
  }
  return target;
}
```

### Remediation Strategies
1. **Block Dangerous Keys:**
   ```javascript
   const BANNED_KEYS = new Set(['__proto__', 'constructor', 'prototype']);
   if (BANNED_KEYS.has(key)) continue;
   ```
2. **Use Prototype-less Objects:**
   ```javascript
   const cleanDictionary = Object.create(null);
   const userMap = new Map();
   ```
3. **Freeze Object Prototype in Production:**
   ```javascript
   Object.freeze(Object.prototype);
   ```

---

## 4. NoSQL Operator Injection (MongoDB / Mongoose)

When parsing JSON bodies with `express.json()`, an attacker can send nested objects containing MongoDB query selectors like `$gt`, `$ne`, or `$regex`.

### Vulnerable Pattern
```javascript
// Request body: {"username": "admin", "password": {"$gt": ""}}
// ❌ VULNERABLE: Direct query with request body object
const user = await db.collection('users').findOne({
  username: req.body.username,
  password: req.body.password // Matches any non-empty password!
});
```

### Remediated Pattern
```javascript
import { z } from 'zod';

const LoginSchema = z.object({
  username: z.string().min(1).max(100),
  password: z.string().min(1).max(100) // Enforces string primitive
});

app.post('/api/login', async (req, res) => {
  const result = LoginSchema.safeParse(req.body);
  if (!result.success) return res.status(400).json({ error: "Invalid credentials" });

  const { username, password } = result.data;
  const user = await User.findOne({ username });
  // Verify hash with bcrypt / argon2
});
```

---

## 5. Path Traversal

Serving local files without resolving and verifying boundary directories.

```javascript
const path = require('node:path');
const fs = require('node:fs');

// ❌ VULNERABLE: path.join allows "../" traversal
app.get('/download', (req, res) => {
  const filePath = path.join(__dirname, 'public/files', req.query.filename);
  res.sendFile(filePath); // Attacker passes filename="../../../../etc/passwd"
});

// ✅ SECURE: Verify resolved path begins with safe base directory
app.get('/download', (req, res) => {
  const baseDir = path.resolve(__dirname, 'public/files');
  const safePath = path.resolve(baseDir, req.query.filename);

  if (!safePath.startsWith(baseDir)) {
    return res.status(403).send("Forbidden: Path traversal detected");
  }
  res.sendFile(safePath);
});
```

---

## 6. Regular Expression Denial of Service (ReDoS)

A single-threaded Node.js event loop can be completely halted by evaluating an exponential regular expression against user input.

- Vulnerable regex example: `^(a+)+$` evaluated against `"aaaaaaaaaaaaaaaaaaaaaaaaaaaa!"`.
- **Defense:**
  - Audit regexes with `safe-regex`.
  - Enforce timeout limits or use non-backtracking engines (e.g. `node-re2`).
