# Stack Reference: Vite + React + Tailwind

## Project Initialization

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install

# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Install React Router
npm install react-router-dom

# Install Lucide icons
npm install lucide-react

# Install clsx + tailwind-merge for class merging
npm install clsx tailwind-merge
```

## Folder Structure

```
src/
├── main.tsx                    ← Entry point
├── App.tsx                     ← Router setup
├── index.css                   ← CSS variables + Tailwind imports
├── lib/
│   └── utils.ts               ← cn() helper
├── pages/
│   ├── HomePage.tsx            ← /
│   ├── AboutPage.tsx           ← /about
│   ├── ContactPage.tsx         ← /contact
│   ├── FAQPage.tsx             ← /faq
│   ├── blog/
│   │   ├── BlogListPage.tsx    ← /blog
│   │   └── BlogDetailPage.tsx  ← /blog/:slug
│   ├── auth/
│   │   ├── LoginPage.tsx       ← /login
│   │   ├── RegisterPage.tsx    ← /register
│   │   ├── ForgotPasswordPage.tsx
│   │   ├── ResetPasswordPage.tsx
│   │   └── OTPPage.tsx         ← /otp
│   └── legal/
│       ├── LegalHubPage.tsx    ← /legal
│       ├── PrivacyPage.tsx     ← /legal/privacy
│       ├── TermsPage.tsx       ← /legal/terms
│       └── RefundPage.tsx      ← /legal/refund
├── components/
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   └── PageWrapper.tsx
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   └── Badge.tsx
│   └── sections/
│       ├── Hero.tsx
│       └── ...
└── assets/
```

## App.tsx — Complete Router Setup

```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Header } from './components/layout/Header'
import { Footer } from './components/layout/Footer'

// Pages
import { HomePage } from './pages/HomePage'
import { AboutPage } from './pages/AboutPage'
import { ContactPage } from './pages/ContactPage'
import { FAQPage } from './pages/FAQPage'
import { BlogListPage } from './pages/blog/BlogListPage'
import { BlogDetailPage } from './pages/blog/BlogDetailPage'
import { LoginPage } from './pages/auth/LoginPage'
import { RegisterPage } from './pages/auth/RegisterPage'
import { ForgotPasswordPage } from './pages/auth/ForgotPasswordPage'
import { ResetPasswordPage } from './pages/auth/ResetPasswordPage'
import { OTPPage } from './pages/auth/OTPPage'
import { LegalHubPage } from './pages/legal/LegalHubPage'
import { PrivacyPage } from './pages/legal/PrivacyPage'
import { TermsPage } from './pages/legal/TermsPage'
import { RefundPage } from './pages/legal/RefundPage'

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen flex-col bg-bg text-text">
        <Header />
        <main className="flex-1">
          <Routes>
            {/* Main */}
            <Route path="/" element={<HomePage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/contact" element={<ContactPage />} />
            <Route path="/faq" element={<FAQPage />} />

            {/* Blog */}
            <Route path="/blog" element={<BlogListPage />} />
            <Route path="/blog/:slug" element={<BlogDetailPage />} />

            {/* Auth */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/forgot-password" element={<ForgotPasswordPage />} />
            <Route path="/reset-password" element={<ResetPasswordPage />} />
            <Route path="/otp" element={<OTPPage />} />

            {/* Legal */}
            <Route path="/legal" element={<LegalHubPage />} />
            <Route path="/legal/privacy" element={<PrivacyPage />} />
            <Route path="/legal/terms" element={<TermsPage />} />
            <Route path="/legal/refund" element={<RefundPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  )
}
```

## index.css

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
}
```

## tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
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
  plugins: [],
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

## Header with React Router

```tsx
import { Link, useLocation } from 'react-router-dom'
import { useState } from 'react'
import { Menu, X } from 'lucide-react'
import { cn } from '@/lib/utils'

const navLinks = [
  { to: '/', label: 'Home' },
  { to: '/about', label: 'About' },
  { to: '/blog', label: 'Blog' },
  { to: '/faq', label: 'FAQ' },
  { to: '/contact', label: 'Contact' },
]

export function Header() {
  const { pathname } = useLocation()
  const [open, setOpen] = useState(false)

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-bg/95 backdrop-blur-sm">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <Link to="/" className="font-display text-xl font-bold text-heading">Logo</Link>

        <nav className="hidden gap-1 md:flex">
          {navLinks.map(({ to, label }) => (
            <Link
              key={to}
              to={to}
              className={cn(
                'px-3 py-2 text-sm font-medium transition-colors hover:text-text',
                pathname === to ? 'text-primary' : 'text-text-muted'
              )}
            >
              {label}
            </Link>
          ))}
        </nav>

        <div className="hidden gap-3 md:flex">
          <Link to="/login" className="px-4 py-2 text-sm font-medium text-text-muted hover:text-text">
            Log in
          </Link>
          <Link to="/register" className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-text-inverse hover:bg-primary-hover transition-colors">
            Get started
          </Link>
        </div>

        <button className="md:hidden" onClick={() => setOpen(!open)}>
          {open ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {open && (
        <div className="border-t border-border bg-bg px-6 py-4 md:hidden">
          {navLinks.map(({ to, label }) => (
            <Link key={to} to={to} onClick={() => setOpen(false)}
              className="block rounded-md px-3 py-2.5 text-sm font-medium text-text-muted hover:bg-bg-alt hover:text-text">
              {label}
            </Link>
          ))}
          <div className="mt-4 flex gap-2 border-t border-border pt-4">
            <Link to="/login" className="flex-1 rounded-md border border-border px-4 py-2 text-center text-sm font-medium">Log in</Link>
            <Link to="/register" className="flex-1 rounded-md bg-primary px-4 py-2 text-center text-sm font-medium text-text-inverse">Sign up</Link>
          </div>
        </div>
      )}
    </header>
  )
}
```
