# Stack: Next.js + shadcn/ui + Tailwind CSS

## Overview
The modern full-stack React framework with shadcn/ui component library (built on Radix UI primitives + Tailwind). Best for production SaaS, dashboards, and pixel-perfect design systems.

---

## Project Setup

```bash
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
npx shadcn@latest init
```

### shadcn init prompts
- Style: **Default** or **New York** (match DESIGN.md aesthetic)
- Base color: pick closest to DESIGN.md primary
- CSS variables: **Yes**

### Add shadcn components
```bash
npx shadcn@latest add button card input label badge
npx shadcn@latest add navigation-menu sheet dialog toast
npx shadcn@latest add form select textarea checkbox radio-group
npx shadcn@latest add table tabs accordion alert avatar
npx shadcn@latest add dropdown-menu popover tooltip separator
```

---

## tailwind.config.ts (extend with DESIGN.md tokens)

```ts
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // shadcn CSS-variable driven colors (auto-added by init)
        background:  "hsl(var(--background))",
        foreground:  "hsl(var(--foreground))",
        primary: {
          DEFAULT:    "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        card: {
          DEFAULT:    "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        muted: {
          DEFAULT:    "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT:    "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        destructive: {
          DEFAULT:    "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
      },
      fontFamily: {
        sans:    ["var(--font-sans)", "sans-serif"],
        heading: ["var(--font-heading)", "sans-serif"],
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate"), require("@tailwindcss/typography")],
};

export default config;
```

---

## CSS Variables (src/app/globals.css)

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background:         0 0% 100%;
    --foreground:         222.2 84% 4.9%;
    --card:               0 0% 100%;
    --card-foreground:    222.2 84% 4.9%;
    --primary:            YOUR_H YOUR_S% YOUR_L%;   /* from DESIGN.md */
    --primary-foreground: 0 0% 100%;
    --muted:              210 40% 96%;
    --muted-foreground:   215.4 16.3% 46.9%;
    --accent:             210 40% 96%;
    --accent-foreground:  222.2 47.4% 11.2%;
    --destructive:        0 84.2% 60.2%;
    --border:             214.3 31.8% 91.4%;
    --input:              214.3 31.8% 91.4%;
    --ring:               YOUR_H YOUR_S% YOUR_L%;
    --radius:             0.5rem;
    --font-sans:          'Inter', sans-serif;
    --font-heading:       'Inter', sans-serif;
  }
  .dark {
    --background:         222.2 84% 4.9%;
    --foreground:         210 40% 98%;
    --card:               222.2 84% 4.9%;
    --card-foreground:    210 40% 98%;
    --muted:              217.2 32.6% 17.5%;
    --muted-foreground:   215 20.2% 65.1%;
    --border:             217.2 32.6% 17.5%;
  }
  * { @apply border-border; }
  body { @apply bg-background text-foreground font-sans antialiased; }
}
```

---

## App Structure

```
src/
├── app/
│   ├── layout.tsx              ← RootLayout with fonts
│   ├── page.tsx                ← /
│   ├── about/page.tsx
│   ├── contact/page.tsx
│   ├── faq/page.tsx
│   ├── blog/
│   │   ├── page.tsx            ← /blog
│   │   └── [slug]/page.tsx     ← /blog/:slug
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   ├── forgot-password/page.tsx
│   │   ├── reset-password/page.tsx
│   │   └── otp/page.tsx
│   └── legal/
│       ├── page.tsx
│       ├── privacy/page.tsx
│       ├── terms/page.tsx
│       └── refund/page.tsx
├── components/
│   ├── layout/
│   │   ├── header.tsx
│   │   ├── footer.tsx
│   │   └── page-wrapper.tsx
│   ├── sections/
│   │   ├── hero.tsx
│   │   ├── features.tsx
│   │   ├── testimonials.tsx
│   │   ├── pricing.tsx
│   │   └── cta.tsx
│   └── forms/
│       ├── login-form.tsx
│       ├── register-form.tsx
│       └── contact-form.tsx
└── lib/
    └── utils.ts                ← cn() helper (auto-added by shadcn)
```

---

## Key Patterns

### Root Layout with Font
```tsx
// src/app/layout.tsx
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans`}>
        {children}
      </body>
    </html>
  );
}
```

### Hero Section
```tsx
// src/components/sections/hero.tsx
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import Link from 'next/link';

export function Hero() {
  return (
    <section className="relative py-24 lg:py-32 overflow-hidden">
      <div className="container mx-auto px-4 text-center">
        <Badge variant="secondary" className="mb-6 px-4 py-1.5 text-sm">
          New Feature Launched
        </Badge>
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight text-foreground mb-6">
          Your Headline <span className="text-primary">Here</span>
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-10">
          Supporting description text that explains the value proposition.
        </p>
        <div className="flex flex-wrap gap-4 justify-center">
          <Button size="lg" asChild>
            <Link href="/register">Get Started</Link>
          </Button>
          <Button size="lg" variant="outline" asChild>
            <Link href="/about">Learn More</Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
```

### Login Page
```tsx
// src/app/(auth)/login/page.tsx
import { LoginForm } from '@/components/forms/login-form';
import Link from 'next/link';

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-muted/30 p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <Link href="/" className="text-2xl font-bold text-primary">BrandName</Link>
          <h1 className="text-xl font-semibold text-foreground mt-4">Sign in to your account</h1>
          <p className="text-muted-foreground text-sm mt-1">Welcome back!</p>
        </div>
        <div className="bg-card border border-border rounded-xl shadow-sm p-8">
          <LoginForm />
          <p className="text-center text-sm text-muted-foreground mt-6">
            No account?{' '}
            <Link href="/register" className="text-primary font-medium hover:underline">Sign up</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
```

### Header with Mobile Sheet
```tsx
// src/components/layout/header.tsx
"use client";
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { Menu } from 'lucide-react';
import Link from 'next/link';

const navLinks = [
  { href: '/about', label: 'About' },
  { href: '/blog', label: 'Blog' },
  { href: '/contact', label: 'Contact' },
];

export function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background/80 backdrop-blur-md">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="text-xl font-bold text-primary">BrandName</Link>
        <nav className="hidden md:flex items-center gap-6">
          {navLinks.map(link => (
            <Link key={link.href} href={link.href}
                  className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              {link.label}
            </Link>
          ))}
        </nav>
        <div className="hidden md:flex items-center gap-3">
          <Button variant="ghost" asChild><Link href="/login">Sign In</Link></Button>
          <Button asChild><Link href="/register">Get Started</Link></Button>
        </div>
        <Sheet>
          <SheetTrigger asChild className="md:hidden">
            <Button variant="ghost" size="icon"><Menu className="h-5 w-5"/></Button>
          </SheetTrigger>
          <SheetContent side="right" className="w-64">
            <nav className="flex flex-col gap-4 mt-8">
              {navLinks.map(link => (
                <Link key={link.href} href={link.href} className="text-sm font-medium">{link.label}</Link>
              ))}
              <Button asChild className="mt-4"><Link href="/register">Get Started</Link></Button>
            </nav>
          </SheetContent>
        </Sheet>
      </div>
    </header>
  );
}
```

---

## Checklist

- [ ] `npx create-next-app` with TypeScript + Tailwind + App Router
- [ ] `npx shadcn@latest init` with CSS variables
- [ ] shadcn components added (button, card, input, label, badge, sheet, dialog, form, toast)
- [ ] CSS variables in globals.css match DESIGN.md colors
- [ ] tailwind.config.ts extended with DESIGN.md tokens
- [ ] All routes created in `src/app/`
- [ ] Header with mobile Sheet navigation
- [ ] Footer with all link groups
- [ ] Auth pages use centered card layout
- [ ] `@tailwindcss/typography` added for blog prose
- [ ] `next/font/google` for font loading (no @import in CSS)
- [ ] Dark mode configured via `class` strategy
