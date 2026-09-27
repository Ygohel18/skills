# HTTP Status Codes & Error Design Reference

> Companion reference for `api-design`.
> Complete reference for HTTP status code semantics, correct usage, common misuses, and RFC 9457 Problem Details error schemas.

---

## 1. Status Code Classification & Semantic Reference

### 2xx: Success
| Code | Name | Semantic Meaning | Required Headers / Body |
|---|---|---|---|
| **200** | `OK` | Request succeeded. General response for GET, PUT, or PATCH. | Returns payload body. |
| **201** | `Created` | Resource was successfully created via POST. | Should include `Location: /resources/{id}` header and newly created representation in body. |
| **202** | `Accepted` | Request accepted for asynchronous processing (e.g. background queue job). | Returns status monitoring URL or job ID: `{"jobId": "..."}`. |
| **204** | `No Content` | Request succeeded, but there is no body to return (common for DELETE or empty PATCH). | **MUST NOT** include a response body or `Content-Type`. |

### 3xx: Redirection & Caching
| Code | Name | Semantic Meaning | Usage |
|---|---|---|---|
| **301** | `Moved Permanently` | Resource has permanently relocated to a new URI. | Clients automatically update bookmarks and cache. |
| **304** | `Not Modified` | Cached version is still fresh. Response to conditional GET (`If-None-Match: "etag"`). | **Zero body**. Saves network bandwidth. |

### 4xx: Client Errors
| Code | Name | Semantic Meaning | Common Misuse |
|---|---|---|---|
| **400** | `Bad Request` | Malformed syntax (invalid JSON, unrecognized query param syntax). | ❌ Used for validation errors (use 422 instead). |
| **401** | `Unauthorized` | Client is **unauthenticated** (missing, expired, or invalid token/API key). | ❌ Confused with 403. 401 means "Who are you?". Must include `WWW-Authenticate` header. |
| **402** | `Payment Required` | Subscription expired, quota depleted, or payment method failed. | Great for SaaS paywalls and billing gates. |
| **403** | `Forbidden` | Client is authenticated, but **lacks permissions** for this resource. | ❌ Confused with 401. 403 means "I know who you are, but you cannot do this." |
| **404** | `Not Found` | Target resource URI does not exist. | ✅ Can also be used intentionally to conceal secret resources from unauthorized users. |
| **405** | `Method Not Allowed` | HTTP method is not supported on this endpoint (e.g. POST to a read-only endpoint). | Must return `Allow: GET, HEAD` header. |
| **409** | `Conflict` | Request conflicts with current server state (duplicate unique email, edit conflict). | Include details on conflicting state or concurrent revision ID. |
| **410** | `Gone` | Resource was intentionally and permanently deleted; no forwarding address. | Useful for deleted user accounts or deprecated API endpoints. |
| **422** | `Unprocessable Content` | Syntactically valid JSON, but contains semantic validation errors (e.g. invalid email). | Returns field-level error validation list. |
| **429** | `Too Many Requests` | Client exceeded rate limit quotas. | Must include `Retry-After: 60` (seconds or HTTP date). |

### 5xx: Server Errors
| Code | Name | Semantic Meaning | Security Rule |
|---|---|---|---|
| **500** | `Internal Server Error` | Unhandled server exception or unexpected fault. | ⚠️ **Never leak stack traces or internal DB errors.** |
| **502** | `Bad Gateway` | Upstream proxy or microservice returned an invalid response. | Check network connectivity between gateway and service. |
| **503** | `Service Unavailable` | Server temporarily overloaded or undergoing maintenance. | Include `Retry-After` header when downtime is known. |
| **504** | `Gateway Timeout` | Upstream microservice or database timed out. | Audit database query locks and slow third-party APIs. |

---

## 2. Common Anti-Patterns & Misuses

### ❌ Anti-Pattern 1: The "HTTP 200 OK with Error Body"
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "error",
  "message": "User not found"
}
```
**Why it fails:** Breaks HTTP caching, API gateways, monitoring alerts, and client retry libraries. An error is **not** OK.
**Correction:** Return `HTTP/1.1 404 Not Found`.

### ❌ Anti-Pattern 2: 401 Unauthorized vs 403 Forbidden Confusion
- **401 Unauthorized:** The client provided **no credentials** or an **invalid/expired token**.
- **403 Forbidden:** The client provided a **valid token**, but their role (e.g., `member`) is not permitted to perform an admin action.

### ❌ Anti-Pattern 3: 400 Bad Request vs 422 Unprocessable Content
- **400 Bad Request:** Syntactically broken payload (unparseable JSON, unclosed quotes, malformed multipart boundary).
- **422 Unprocessable Content:** Valid JSON, but semantic rules fail (`"email": "not-an-email"`, `"age": -5`).

---

## 3. Standardized Error Response Formats (RFC 9457 / RFC 7807)

Every API should adhere to the IETF Problem Details standard (`application/problem+json`):

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Unprocessable Content",
  "status": 422,
  "detail": "One or more fields in your request payload failed validation.",
  "instance": "/api/v1/users",
  "invalid_params": [
    {
      "name": "email",
      "reason": "Must be a valid email address with a resolvable domain."
    },
    {
      "name": "password",
      "reason": "Must be at least 12 characters and include a special symbol."
    }
  ]
}
```

### Essential Error Fields:
1. `code` / `type`: Stable machine-readable identifier (clients switch on this).
2. `message` / `title`: Human-readable explanation.
3. `detail`: Specific context for this specific failure.
4. `invalid_params` / `errors`: Array of field-level errors for form inputs.
