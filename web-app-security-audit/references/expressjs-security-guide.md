# Express.js & Fastify Security Audit Guide

A security engineering manual covering vulnerability paths, middleware misconfigurations, and defensive hardening for Express.js and Fastify applications.

---

## 1. Open Redirect Vulnerabilities

Redirecting users to unvalidated URLs supplied via query parameters (`?returnTo=...` or `?redirect=...`).

### Vulnerable Pattern
```javascript
// ❌ VULNERABLE: Direct redirect to user-supplied URL
app.get('/login', (req, res) => {
  // Attacker sends: /login?returnTo=https://evil-phishing.com
  res.redirect(req.query.returnTo);
});
```

### Remediated Pattern
```javascript
// ✅ SECURE: Validate that the redirect path is relative and starts with a single slash
function isSafeRedirect(targetUrl) {
  if (!targetUrl || typeof targetUrl !== 'string') return false;
  // Disallow protocol-relative URLs (e.g. "//evil.com") and absolute URLs
  return targetUrl.startsWith('/') && !targetUrl.startsWith('//');
}

app.get('/login', (req, res) => {
  const returnTo = isSafeRedirect(req.query.returnTo) ? req.query.returnTo : '/dashboard';
  res.redirect(returnTo);
});
```

---

## 2. Path Traversal in `res.sendFile()`

Express's `res.sendFile()` method sends files directly from disk. If the filename is concatenated from user input without the `root` option, directory traversal attacks can read sensitive server files.

```javascript
const path = require('node:path');

// ❌ VULNERABLE: Direct sendFile with user path
app.get('/view', (req, res) => {
  // Attacker passes: ?file=../../../../etc/passwd
  res.sendFile(req.query.file);
});

// ✅ SECURE: Specify root directory and validate filename
app.get('/view', (req, res) => {
  const filename = path.basename(String(req.query.file)); // Strips directory slashes
  res.sendFile(filename, {
    root: path.join(__dirname, 'public/documents'),
    dotfiles: 'deny'
  });
});
```

---

## 3. Missing Security Headers (`helmet`)

By default, Express exposes the `X-Powered-By: Express` response header and lacks clickjacking, HSTS, and CSP protections.

```javascript
// ✅ SECURE: Always mount helmet early in the middleware chain
const express = require('express');
const helmet = require('helmet');

const app = express();
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      objectSrc: ["'none'"],
      upgradeInsecureRequests: [],
    },
  },
  crossOriginEmbedderPolicy: false,
}));
```

---

## 4. Body Parser DoS via Unbounded Payload Limit

By default, `express.json()` without a specified `limit` may allow excessively large JSON payloads that consume memory and block V8 JSON parsing.

```javascript
// ❌ VULNERABLE: Default or excessive limit
app.use(express.json({ limit: '50mb' }));

// ✅ SECURE: Strict payload limits
app.use(express.json({ limit: '100kb' }));
app.use(express.urlencoded({ extended: true, limit: '100kb' }));
```

---

## 5. Insecure CORS with Reflected Origin

```javascript
const cors = require('cors');

// ❌ VULNERABLE: Reflects any Origin header with credentials
app.use(cors({
  origin: true, // Reflects request origin
  credentials: true,
}));

// ✅ SECURE: Strict domain whitelist
const ALLOWED_ORIGINS = new Set([
  'https://app.example.com',
  'https://admin.example.com'
]);

app.use(cors({
  origin: (origin, callback) => {
    if (!origin || ALLOWED_ORIGINS.has(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Blocked by CORS policy'));
    }
  },
  credentials: true,
}));
```
