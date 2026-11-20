# Next.js Security Audit Guide

A security manual for Next.js applications (App Router and Pages Router), covering Server Actions, React Server Components (RSC), middleware authorization bypasses, and client secret leakages.

---

## 1. Middleware Authorization Bypass (CVE-2025-29927)

### The Flaw
In Next.js, relying exclusively on `middleware.ts` to enforce authentication or role-based access control creates a single point of failure. If an edge routing misconfiguration, proxy discrepancy, or framework parsing bug (such as CVE-2025-29927) allows a request to bypass middleware, unprotected server components and route handlers execute with zero authentication checks.

### Remediation: Defense-in-Depth Authorization
Never assume a request entering a Server Action, Route Handler, or Server Component has been pre-authorized by middleware. Always authenticate and authorize at the handler boundary:

```typescript
// app/actions/update-org.ts
'use server'

import { auth } from '@/lib/auth';
import { db } from '@/lib/db';

export async function updateOrganization(orgId: string, data: any) {
  // ✅ SECURE: Verify session explicitly inside the Server Action
  const session = await auth();
  if (!session || !session.user) {
    throw new Error('Unauthorized');
  }

  // ✅ SECURE: Verify Object-Level Access (IDOR protection)
  const isOwner = await db.organizationMember.findFirst({
    where: { orgId, userId: session.user.id, role: 'ADMIN' },
  });
  if (!isOwner) {
    throw new Error('Forbidden');
  }

  return db.organization.update({ where: { id: orgId }, data });
}
```

---

## 2. Client Secret Leakage via `NEXT_PUBLIC_`

Any environment variable prefixed with `NEXT_PUBLIC_` is inlined into the client-side JavaScript bundle during `next build`.

```bash
# ❌ VULNERABLE: Sensitive secrets exposed to browser
NEXT_PUBLIC_STRIPE_SECRET_KEY=sk_live_...
NEXT_PUBLIC_DATABASE_URL=postgres://user:pass@db.internal:5432/prod
NEXT_PUBLIC_JWT_SECRET=super_secret_signing_key

# ✅ SECURE: Server-only variables (no NEXT_PUBLIC_ prefix)
STRIPE_SECRET_KEY=sk_live_...
DATABASE_URL=postgres://user:pass@db.internal:5432/prod
JWT_SECRET=super_secret_signing_key

# ✅ SECURE: Only public keys receive NEXT_PUBLIC_
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...
NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN=pk.eyJ1...
```

---

## 3. Cross-Site Scripting via `dangerouslySetInnerHTML`

Rendering raw HTML in React components bypasses React's automatic string escaping.

```tsx
// ❌ VULNERABLE: Direct rendering of unsanitized user content
export function CommentBody({ userHtml }: { userHtml: string }) {
  return <div dangerouslySetInnerHTML={{ __html: userHtml }} />;
}

// ✅ SECURE: Sanitize using DOMPurify / isomorphic-dompurify
import DOMPurify from 'isomorphic-dompurify';

export function CommentBody({ userHtml }: { userHtml: string }) {
  const clean = DOMPurify.sanitize(userHtml, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'code'],
    ALLOWED_ATTR: ['href', 'title', 'target'],
  });
  return <div dangerouslySetInnerHTML={{ __html: clean }} />;
}
```

---

## 4. Server-Side Request Forgery (SSRF)

Next.js provides built-in image optimization and server-side fetching. If user input dictates the destination URL without validation, internal network services can be probed.

### Next.js Image Component Configuration
Restrict allowed external domains in `next.config.js`:

```javascript
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 's3.us-east-1.amazonaws.com',
        pathname: '/my-company-assets/**',
      },
    ],
  },
};
```

---

## 5. React Server Components (RSC) Deserialization Risks

In late 2025, critical security advisories highlighted deserialization vulnerabilities in React Server Components when handling complex flight payloads.
- **Rule:** Keep `next` and `react` pinned to actively maintained, patched versions.
- **Rule:** Do not pass unvalidated raw binary or complex serialized prototypes into server action parameters.
