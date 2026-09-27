# Stack Reference: Astro + Vite + React + Tailwind

Astro uses Vite as its build tool. Use file-based routing in `src/pages/` for static pages, and React islands (`client:load` / `client:visible`) only for interactive UI (mobile nav, forms, OTP input).

## Project Initialization

```bash
npm create astro@latest my-app -- --template minimal --typescript strict --install --git --yes
cd my-app

# Add Tailwind + React integrations
npx astro add tailwind react --yes

# Install Lucide icons + class utilities
npm install lucide-react clsx tailwind-merge

# Typography plugin for blog/legal prose
npm install -D @tailwindcss/typography
```

## astro.config.mjs

```js
import { defineConfig } from 'astro/config'
import tailwind from '@astrojs/tailwind'
import react from '@astrojs/react'

export default defineConfig({
  integrations: [
    tailwind({ applyBaseStyles: false }),
    react(),
  ],
})
```

## Folder Structure

```
src/
├── layouts/
│   └── BaseLayout.astro        ← Root layout (Header, Footer, fonts)
├── pages/
│   ├── index.astro             ← /
│   ├── about.astro             ← /about
│   ├── contact.astro           ← /contact
│   ├── faq.astro               ← /faq
│   ├── blog/
│   │   ├── index.astro         ← /blog
│   │   └── [slug].astro        ← /blog/:slug
│   ├── login.astro             ← /login
│   ├── register.astro          ← /register
│   ├── forgot-password.astro   ← /forgot-password
│   ├── reset-password.astro    ← /reset-password
│   ├── otp.astro               ← /otp
│   └── legal/
│       ├── index.astro         ← /legal
│       ├── privacy.astro       ← /legal/privacy
│       ├── terms.astro         ← /legal/terms
│       └── refund.astro        ← /legal/refund
├── components/
│   ├── layout/
│   │   ├── Header.tsx          ← React island (mobile menu)
│   │   ├── Footer.astro
│   │   └── PageWrapper.astro
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   └── Badge.tsx
│   ├── sections/
│   │   ├── Hero.astro
│   │   └── ...
│   └── forms/
│       ├── LoginForm.tsx
│       ├── RegisterForm.tsx
│       ├── ContactForm.tsx
│       └── OTPForm.tsx
├── lib/
│   └── utils.ts                ← cn() helper
└── styles/
    └── global.css              ← CSS variables + Tailwind imports
```

## global.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=...');

@layer base {
  :root {
    /* All color tokens from DESIGN.md */
    --color-primary: #XXXXXX;
    /* ... */
  }

  body {
    @apply bg-bg text-text font-body antialiased;
  }

  h1, h2, h3, h4, h5, h6 {
    @apply font-display;
  }
}
```

## tailwind.config.mjs

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        /* Paste from DESIGN.md section 2.2 */
      },
      fontFamily: {
        display: ['var(--font-display)', 'system-ui', 'sans-serif'],
        body: ['var(--font-body)', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        /* Paste from DESIGN.md section 5 */
      },
      boxShadow: {
        /* Paste from DESIGN.md section 6 */
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
}
```

## lib/utils.ts

```ts
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

## BaseLayout.astro

```astro
---
import '../styles/global.css'
import { Header } from '../components/layout/Header'
import Footer from '../components/layout/Footer.astro'

interface Props {
  title?: string
  description?: string
}

const { title = 'Site Name', description = 'Site description' } = Astro.props
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content={description} />
    <title>{title}</title>
  </head>
  <body class="flex min-h-screen flex-col bg-bg text-text">
    <Header client:load currentPath={Astro.url.pathname} />
    <main class="flex-1">
      <slot />
    </main>
    <Footer />
  </body>
</html>
```

## Page Pattern

```astro
---
// src/pages/about.astro
import BaseLayout from '../layouts/BaseLayout.astro'
import PageWrapper from '../components/layout/PageWrapper.astro'
---

<BaseLayout title="About | Site Name" description="About us">
  <PageWrapper>
    <h1 class="font-display text-4xl font-bold text-heading">About</h1>
    <!-- Page content -->
  </PageWrapper>
</BaseLayout>
```

## Dynamic Blog Route

```astro
---
// src/pages/blog/[slug].astro
import BaseLayout from '../../layouts/BaseLayout.astro'

export function getStaticPaths() {
  const posts = [
    { slug: 'example-post', title: 'Example Post', excerpt: '...', date: '2025-01-01' },
  ]
  return posts.map((post) => ({ params: { slug: post.slug }, props: { post } }))
}

const { post } = Astro.props
---

<BaseLayout title={`${post.title} | Site Name`}>
  <article class="container mx-auto max-w-3xl px-6 py-16">
    <h1 class="font-display text-4xl font-bold text-heading">{post.title}</h1>
    <p class="mt-2 text-sm text-text-muted">{post.date}</p>
    <div class="prose prose-neutral mt-8 max-w-none">
      <!-- Article content -->
    </div>
  </article>
</BaseLayout>
```

## Header — React Island

Use a React component for the header because it needs client-side state (mobile menu). Pass `currentPath` from Astro for active link styling.

```tsx
// src/components/layout/Header.tsx
import { useState } from 'react'
import { Menu, X } from 'lucide-react'
import { cn } from '../../lib/utils'

const navLinks = [
  { href: '/', label: 'Home' },
  { href: '/about', label: 'About' },
  { href: '/blog', label: 'Blog' },
  { href: '/faq', label: 'FAQ' },
  { href: '/contact', label: 'Contact' },
]

interface HeaderProps {
  currentPath: string
}

export function Header({ currentPath }: HeaderProps) {
  const [open, setOpen] = useState(false)

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-bg/95 backdrop-blur-sm">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <a href="/" className="font-display text-xl font-bold text-heading">Logo</a>

        <nav className="hidden gap-1 md:flex">
          {navLinks.map(({ href, label }) => (
            <a
              key={href}
              href={href}
              className={cn(
                'px-3 py-2 text-sm font-medium transition-colors hover:text-text',
                currentPath === href ? 'text-primary' : 'text-text-muted'
              )}
            >
              {label}
            </a>
          ))}
        </nav>

        <div className="hidden gap-3 md:flex">
          <a href="/login" className="px-4 py-2 text-sm font-medium text-text-muted hover:text-text">
            Log in
          </a>
          <a href="/register" className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-text-inverse hover:bg-primary-hover transition-colors">
            Get started
          </a>
        </div>

        <button className="md:hidden" onClick={() => setOpen(!open)} aria-label="Toggle menu">
          {open ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {open && (
        <div className="border-t border-border bg-bg px-6 py-4 md:hidden">
          {navLinks.map(({ href, label }) => (
            <a
              key={href}
              href={href}
              onClick={() => setOpen(false)}
              className="block rounded-md px-3 py-2.5 text-sm font-medium text-text-muted hover:bg-bg-alt hover:text-text"
            >
              {label}
            </a>
          ))}
          <div className="mt-4 flex gap-2 border-t border-border pt-4">
            <a href="/login" className="flex-1 rounded-md border border-border px-4 py-2 text-center text-sm font-medium">Log in</a>
            <a href="/register" className="flex-1 rounded-md bg-primary px-4 py-2 text-center text-sm font-medium text-text-inverse">Sign up</a>
          </div>
        </div>
      )}
    </header>
  )
}
```

## Footer — Static Astro Component

Prefer `.astro` for static markup (no JS shipped to client):

```astro
---
// src/components/layout/Footer.astro
const linkGroups = [
  { title: 'Product', links: [{ href: '/about', label: 'About' }, { href: '/faq', label: 'FAQ' }] },
  { title: 'Legal', links: [{ href: '/legal/privacy', label: 'Privacy' }, { href: '/legal/terms', label: 'Terms' }] },
]
---

<footer class="border-t border-border bg-bg-alt">
  <div class="mx-auto max-w-7xl px-6 py-12">
    <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
      {linkGroups.map((group) => (
        <div>
          <h3 class="mb-3 text-sm font-semibold text-heading">{group.title}</h3>
          <ul class="space-y-2">
            {group.links.map((link) => (
              <li>
                <a href={link.href} class="text-sm text-text-muted hover:text-text">{link.label}</a>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
    <p class="mt-8 border-t border-border pt-8 text-sm text-text-faint">
      &copy; {new Date().getFullYear()} Site Name. All rights reserved.
    </p>
  </div>
</footer>
```

## Auth Page Pattern

Use React islands for forms with validation state:

```astro
---
// src/pages/login.astro
import BaseLayout from '../layouts/BaseLayout.astro'
import { LoginForm } from '../components/forms/LoginForm'
---

<BaseLayout title="Log in | Site Name">
  <div class="flex min-h-[calc(100vh-4rem)] items-center justify-center px-4 py-12">
    <LoginForm client:load />
  </div>
</BaseLayout>
```

## Client Hydration Directives

Choose the lightest directive that works:

| Directive | When to use |
|-----------|-------------|
| *(none)* | Static `.astro` components — zero JS |
| `client:visible` | Below-fold interactive UI (forms, accordions) |
| `client:load` | Above-fold interactivity (header mobile menu) |
| `client:idle` | Non-critical interactivity after page idle |

**Rule**: Default to static Astro components. Only add `client:*` to components that need browser state or event handlers.

## Astro vs Vite/React SPA — Key Differences

| Concern | Vite + React SPA | Astro + Vite |
|---------|------------------|--------------|
| Routing | React Router in `App.tsx` | File-based in `src/pages/` |
| Links | `<Link to="/">` | `<a href="/">` in Astro; `<a href="/">` in React islands |
| Layout | Wrapper in `App.tsx` | `BaseLayout.astro` with `<slot />` |
| Static sections | React components | `.astro` components (preferred) |
| Interactive UI | All components are client | React islands with `client:*` |
| Blog slugs | `useParams()` | `getStaticPaths()` + `[slug].astro` |

## tsconfig.json Path Alias (optional)

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

Then import with `@/lib/utils`, `@/components/ui/Button`, etc.

## Dev & Build Commands

```bash
npm run dev      # Start Vite dev server (default :4321)
npm run build    # Production build to dist/
npm run preview  # Preview production build
```
