# Universal Web Application Vulnerabilities & Defense Handbook

A technology-agnostic reference detailing the mechanics, detection methods, and remediation strategies for OWASP Top 10 vulnerabilities affecting all web application stacks.

---

## 1. Insecure Direct Object References (IDOR / BOLA)

### Mechanics
An application provides direct access to objects based on user-supplied input without verifying that the requesting user has authorization to access that specific record.

```text
Attacker visits: GET /api/documents/1042
Attacker modifies URL: GET /api/documents/1043 -> Downloads victim's private invoice
```

### Remediation: Scope Queries to Authenticated Tenant / User
Never query an entity by ID alone if the entity belongs to an account or organization:

```typescript
// ❌ VULNERABLE: Direct ID lookup
const invoice = await db.invoice.findUnique({ where: { id: req.params.id } });

// ✅ SECURE: Multi-tenant scoped query
const invoice = await db.invoice.findFirst({
  where: {
    id: req.params.id,
    organizationId: req.user.currentOrgId, // Scoped to active tenant
  },
});
if (!invoice) throw new NotFoundException();
```

---

## 2. Server-Side Request Forgery (SSRF)

### Mechanics
The server receives a URL from an untrusted client and performs an HTTP/network request to that destination. Attackers target:
- Cloud metadata endpoints: `http://169.254.169.254/latest/meta-data/iam/security-credentials/`
- Local loopback services: `http://127.0.0.1:6379` (Redis), `http://localhost:9200` (Elasticsearch)
- Internal private VPC IP ranges: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`

### Defense: Pre-Request IP Validation & DNS Rebinding Protection
1. Resolve the DNS hostname to an IP address **before** making the request.
2. Verify the resolved IP does not fall within RFC 1918, link-local, loopback, or cloud metadata ranges.
3. Establish the HTTP connection directly to the verified IP to prevent DNS rebinding attacks:

```python
import ipaddress
import socket
import urllib.parse

def is_safe_url(target_url: str) -> bool:
    parsed = urllib.parse.urlparse(target_url)
    if parsed.scheme not in ('http', 'https'):
        return False

    hostname = parsed.hostname
    try:
        ip_str = socket.gethostbyname(hostname)
        ip = ipaddress.ip_address(ip_str)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return False
        return True
    except Exception:
        return False
```

---

## 3. Insecure Deserialization

### Mechanics
Serialization converts in-memory objects into bytes or strings (e.g. PHP `serialize()`, Python `pickle`, Java serialized objects). When untrusted byte streams are deserialized, internal magic methods (`__destruct()`, `__wakeup()`, `readObject()`) execute before type checking, allowing attackers to stitch together existing codebase classes ("gadget chains") to achieve arbitrary code execution.

### Remediation
1. Never deserialize untrusted user data using native language object serializers.
2. Adopt standardized data interchange formats: JSON (`JSON.parse`, `json_decode`, `json.loads`) or Protocol Buffers.
3. If signed objects must be transferred, verify them with HMAC-SHA256 before processing.

---

## 4. Cross-Site Scripting (XSS)

### 3 Core Varieties:
1. **Stored XSS:** Malicious script is saved in the database (e.g. comment body) and executed when other users view the page.
2. **Reflected XSS:** Script is delivered via request parameters (e.g. search query) and rendered directly in the response page.
3. **DOM-based XSS:** Client-side JavaScript reads from an untrusted source (`location.hash`, `URLSearchParams`) and writes into an execution sink (`element.innerHTML`, `eval`, `document.write`).

### Defense:
- Use context-aware auto-escaping template engines by default (Blade `{{ }}`, React JSX `{ }`, Vue `{{ }}`).
- Apply Content Security Policy (`CSP`) headers to restrict script execution sources:
  ```http
  Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-random123'; object-src 'none';
  ```

---

## 5. Security Headers Baseline

Ensure production servers emit the standard security headers:

```http
# Prevent clickjacking
X-Frame-Options: DENY

# Prevent MIME-type sniffing
X-Content-Type-Options: nosniff

# Restrict referrer leakage
Referrer-Policy: strict-origin-when-cross-origin

# Enforce HTTPS
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

# Restrict browser APIs
Permissions-Policy: camera=(), microphone=(), geolocation=()
```
