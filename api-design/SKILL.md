---
name: api-design
description: >
  Language-agnostic framework for designing, evaluating, and standardizing HTTP APIs (REST and GraphQL).
  Triggers whenever an agent is asked to "design an API", "add an endpoint", "review this API contract",
  "how should I version this?", "REST vs GraphQL", "design pagination", or when selecting HTTP status codes.
  Enforces clean noun-based REST routing, strict HTTP method semantics, RFC 9457 error contracts,
  cursor/offset pagination, rate limiting, and spec-first OpenAPI documentation.
metadata:
  author: yash
  version: "1.0"
  scope: "api-design, rest-api, graphql, openapi, http-contracts"
allowed-tools: Read Write Bash
---

# API Design & Contract Standards

A language-agnostic operational standard for designing, reviewing, and versioning HTTP APIs (REST-first, with GraphQL guidance).

> **Sibling Standards:**
> - For input validation and injection prevention at the controller layer, see [`universal-coding-standards`](file:///Users/apple/Projects/yash/skills/universal-coding-standards/SKILL.md#6-security-baseline).
> - For vetting third-party routing or gateway packages, see [`package-security-vetting`](file:///Users/apple/Projects/yash/skills/package-security-vetting/SKILL.md).

---

## 1. Resource & URL Architecture (REST)

- [ ] **1.1 Nouns, Not Verbs in Paths:**
  - ✅ `/orders`, `/users/42/invoices`, `/subscriptions`
  - ❌ `/getOrders`, `/createUser`, `/api/update_order`
- [ ] **1.2 Plural Resource Names:** Always use plural nouns for collections (`/products`, `/customers`).
- [ ] **1.3 Consistent URL Casing:** Use `kebab-case` for multi-word path segments (`/payment-methods`, `/shipping-addresses`).
- [ ] **1.4 Shallow Nesting ($\le 2$ Levels):**
  - Nest resources only when a strict parent-child ownership exists:
    - ✅ `/organizations/{org_id}/members`
    - ✅ `/orders/{order_id}/items`
  - Avoid deep nesting:
    - ❌ `/authors/12/books/4/chapters/8/paragraphs/2`
    - ✅ Top-level resource by ID: `/chapters/8/paragraphs`
- [ ] **1.5 Strict HTTP Method Semantics:**
  - `GET`: Safe, idempotent, no side effects, returns resource. **Never** mutates state.
  - `POST`: Creates a child resource or executes a non-idempotent operation.
  - `PUT`: Full replacement of resource representation; idempotent.
  - `PATCH`: Partial update of specific fields; non-idempotent or idempotent.
  - `DELETE`: Deletes the resource; idempotent (subsequent calls return 204 or 404).

---

## 2. Request & Response Contracts

- [ ] **2.1 Consistent Envelope Architecture:**
  - Choose one style across the entire API and never mix:
    - **No Envelope (Clean REST standard):** Return raw entity or array: `{ "id": "...", "name": "..." }`.
    - **Enveloped:** `{ "data": { ... }, "meta": { ... } }`.
- [ ] **2.2 Uniform Field Casing:**
  - Strictly enforce one JSON casing style across all endpoints (`camelCase` or `snake_case`). Never return `user_id` on one endpoint and `userId` on another.
- [ ] **2.3 Stable Invariant Types:**
  - A field must never change type based on state (e.g. returning `null` vs `""` vs `0`, or returning a string sometimes and an integer other times).
  - Explicit ISO-8601 strings for timestamps: `"2026-09-28T02:30:00Z"`.

---

## 3. Error Handling & Status Codes

- [ ] **3.1 Accurate HTTP Status Codes:**
  - 🚫 **Never return HTTP 200 OK with an error payload!**
  - Use exact status codes (see [`references/status-codes.md`](file:///Users/apple/Projects/yash/skills/api-design/references/status-codes.md)):
    - `400 Bad Request`: Malformed JSON or unparseable syntax.
    - `401 Unauthorized`: Unauthenticated (missing/expired token).
    - `403 Forbidden`: Authenticated, but lacks required role or permission.
    - `404 Not Found`: Target resource does not exist.
    - `409 Conflict`: Unique constraint violation or state collision.
    - `422 Unprocessable Content`: Valid syntax, but business validation failed.
    - `429 Too Many Requests`: Rate limit exceeded (include `Retry-After`).
    - `500 Internal Server Error`: Unhandled server-side fault.
- [ ] **3.2 Standardized Error Body (RFC 9457 Problem Details):**
  - Every error response must return a machine-readable code, human title, and field-level invalid parameters.
- [ ] **3.3 Zero Internal Leakage:**
  - Strip stack traces, raw SQL queries, internal database table names, and server hostnames from error payloads.

---

## 4. Versioning Strategy

- [ ] **4.1 Explicit Versioning Scheme:**
  - Select and document the versioning mechanism before launching v1:
    - **URI Path (Most common & debuggable):** `/v1/invoices`
    - **Header-based:** `X-API-Version: 2026-09-28` or `Accept: application/vnd.company.v1+json`
- [ ] **4.2 Additive Changes Do Not Require Version Bumps:**
  - Adding a new endpoint, optional query parameter, or new response field is backwards-compatible.
  - Breaking changes (removing a field, renaming a field, changing a type, altering required headers) require a new version.
- [ ] **4.3 Graceful Deprecation:**
  - Add `Sunset: <date>` and `Deprecation: true` HTTP headers to deprecated endpoints.
  - Support previous versions for a published deprecation window before terminating.

---

## 5. Pagination, Filtering & Sorting

- [ ] **5.1 Never Allow Unbounded Queries:**
  - Every collection endpoint must enforce a default limit (e.g. 20) and a maximum hard ceiling (e.g. 100).
- [ ] **5.2 Choose the Right Pagination Mechanism:**
  - **Offset/Limit (`?limit=20&offset=40`):** Simple, permits jumping to page N. Slower on deep tables and susceptible to phantom row skips under live writes.
  - **Cursor-Based (`?limit=20&starting_after=order_123`):** High-performance on large datasets, stable against insertions/deletions, recommended for real-time feeds.
- [ ] **5.3 Consistent Filter & Sort Syntax:**
  - Sorting: `?sort=-created_at,status` (minus prefix for descending).
  - Filtering: `?status=pending&customer_id=42`.

---

## 6. Security, Rate Limiting & Auth

- [ ] **6.1 Explicit Auth Scopes:**
  - Every endpoint specification must state its authorization tier: `Public`, `AuthenticatedUser`, or `Role(Admin)`.
- [ ] **6.2 Rate Limiting:**
  - Protect all public and compute-heavy endpoints. Return `429 Too Many Requests` with a `Retry-After: 60` header.
- [ ] **6.3 Boundary Input Validation:**
  - Validate and sanitize all query parameters, route IDs, and request JSON bodies before invoking service logic.

---

## 7. Spec-First Documentation

- [ ] **Contract Before Code:** Author the OpenAPI 3.1 specification or GraphQL schema alongside implementation.
- [ ] **Complete Endpoint Schema:** Every endpoint definition must include:
  1. Purpose & summary description.
  2. Authentication requirement / OAuth scopes.
  3. JSON request payload schema with required fields.
  4. Response schemas for 2xx success and 4xx/5xx failure modes.
  5. One copy-pasteable cURL or JSON request/response example.

---

## Detailed References

- [`references/status-codes.md`](file:///Users/apple/Projects/yash/skills/api-design/references/status-codes.md): Full status code semantics, RFC 9457 Problem Details JSON format, and common anti-patterns (such as HTTP 200 with error bodies).
- [`references/graphql-notes.md`](file:///Users/apple/Projects/yash/skills/api-design/references/graphql-notes.md): GraphQL schema-first patterns, nullability discipline, DataLoaders for N+1 prevention, query depth/complexity security limits, and REST vs GraphQL decision matrix.
