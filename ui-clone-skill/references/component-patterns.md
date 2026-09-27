# Component Patterns Reference

Reusable patterns for common UI components. Always adapt colors/spacing to match DESIGN.md tokens.

---

## OTP Input (6-digit code)

```tsx
// For Next.js / Vite React / Astro React islands
// Next.js: add 'use client' at top
// Astro: use client:load or client:visible on the component in the .astro page
'use client'
import { useRef, useState } from 'react'

export function OTPInput({ length = 6, onComplete }: { length?: number; onComplete?: (code: string) => void }) {
  const [values, setValues] = useState<string[]>(Array(length).fill(''))
  const inputs = useRef<HTMLInputElement[]>([])

  const handleChange = (index: number, value: string) => {
    if (!/^\d*$/.test(value)) return
    const next = [...values]
    next[index] = value.slice(-1)
    setValues(next)
    if (value && index < length - 1) inputs.current[index + 1]?.focus()
    if (next.every(Boolean)) onComplete?.(next.join(''))
  }

  const handleKeyDown = (index: number, e: React.KeyboardEvent) => {
    if (e.key === 'Backspace' && !values[index] && index > 0) {
      inputs.current[index - 1]?.focus()
    }
  }

  const handlePaste = (e: React.ClipboardEvent) => {
    const paste = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, length)
    if (!paste) return
    const next = [...values]
    paste.split('').forEach((char, i) => { next[i] = char })
    setValues(next)
    inputs.current[Math.min(paste.length, length - 1)]?.focus()
    if (next.every(Boolean)) onComplete?.(next.join(''))
  }

  return (
    <div className="flex gap-3">
      {Array(length).fill(0).map((_, i) => (
        <input
          key={i}
          ref={(el) => { if (el) inputs.current[i] = el }}
          type="text"
          inputMode="numeric"
          maxLength={1}
          value={values[i]}
          onChange={(e) => handleChange(i, e.target.value)}
          onKeyDown={(e) => handleKeyDown(i, e)}
          onPaste={handlePaste}
          className="h-14 w-12 rounded-md border border-border bg-bg-input text-center text-xl font-semibold text-text outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20"
        />
      ))}
    </div>
  )
}
```

---

## FAQ Accordion

```tsx
'use client'
import { useState } from 'react'
import { ChevronDown } from 'lucide-react'
import { cn } from '@/lib/utils'

const faqs = [
  { q: 'Question one?', a: 'Answer one.' },
  { q: 'Question two?', a: 'Answer two.' },
]

export function FAQAccordion() {
  const [open, setOpen] = useState<number | null>(null)

  return (
    <div className="divide-y divide-border">
      {faqs.map((faq, i) => (
        <div key={i}>
          <button
            onClick={() => setOpen(open === i ? null : i)}
            className="flex w-full items-center justify-between py-5 text-left"
          >
            <span className="font-display text-base font-semibold text-heading">{faq.q}</span>
            <ChevronDown
              size={20}
              className={cn('shrink-0 text-text-muted transition-transform', open === i && 'rotate-180')}
            />
          </button>
          {open === i && (
            <div className="pb-5 text-sm leading-relaxed text-text-muted">{faq.a}</div>
          )}
        </div>
      ))}
    </div>
  )
}
```

---

## Pricing Cards (3-tier with toggle)

```tsx
'use client'
import { useState } from 'react'
import { Check } from 'lucide-react'
import { cn } from '@/lib/utils'

const plans = [
  {
    name: 'Starter', monthlyPrice: 0, annualPrice: 0,
    description: 'For individuals and small projects.',
    features: ['5 projects', '1 GB storage', 'Basic analytics', 'Email support'],
    cta: 'Get started free', featured: false,
  },
  {
    name: 'Pro', monthlyPrice: 29, annualPrice: 19,
    description: 'For growing teams and businesses.',
    features: ['Unlimited projects', '50 GB storage', 'Advanced analytics', 'Priority support', 'Custom domain'],
    cta: 'Start free trial', featured: true,
  },
  {
    name: 'Enterprise', monthlyPrice: 99, annualPrice: 79,
    description: 'For large organizations.',
    features: ['Unlimited everything', 'SSO / SAML', 'SLA guarantee', 'Dedicated manager', 'Custom integrations'],
    cta: 'Contact sales', featured: false,
  },
]

export function PricingSection() {
  const [annual, setAnnual] = useState(false)

  return (
    <section className="py-20">
      <div className="mx-auto max-w-7xl px-6">
        <div className="mb-10 text-center">
          <h2 className="font-display text-4xl font-bold text-heading">Simple pricing</h2>
          <p className="mt-3 text-lg text-text-muted">Choose the plan that works for you</p>

          {/* Toggle */}
          <div className="mt-6 flex items-center justify-center gap-3">
            <span className={cn('text-sm font-medium', !annual && 'text-text' , annual && 'text-text-muted')}>Monthly</span>
            <button
              onClick={() => setAnnual(!annual)}
              className={cn(
                'relative h-6 w-11 rounded-full transition-colors',
                annual ? 'bg-primary' : 'bg-border'
              )}
            >
              <span className={cn(
                'absolute top-0.5 h-5 w-5 rounded-full bg-white shadow transition-transform',
                annual ? 'translate-x-5' : 'translate-x-0.5'
              )} />
            </button>
            <span className={cn('text-sm font-medium', annual && 'text-text', !annual && 'text-text-muted')}>
              Annual <span className="text-xs font-semibold text-primary">Save 35%</span>
            </span>
          </div>
        </div>

        <div className="grid gap-8 lg:grid-cols-3">
          {plans.map((plan) => (
            <div key={plan.name} className={cn(
              'rounded-xl border p-8',
              plan.featured
                ? 'border-primary bg-primary-light shadow-elevated ring-2 ring-primary'
                : 'border-border bg-bg-card shadow-card'
            )}>
              <h3 className="font-display text-xl font-bold text-heading">{plan.name}</h3>
              <p className="mt-1 text-sm text-text-muted">{plan.description}</p>
              <div className="my-6">
                <span className="font-display text-4xl font-bold text-heading">
                  ${annual ? plan.annualPrice : plan.monthlyPrice}
                </span>
                <span className="text-text-muted">/mo</span>
              </div>
              <ul className="mb-8 space-y-3">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-center gap-2.5 text-sm text-text">
                    <Check size={16} className="shrink-0 text-primary" />
                    {f}
                  </li>
                ))}
              </ul>
              <button className={cn(
                'w-full rounded-md py-2.5 text-sm font-semibold transition-colors',
                plan.featured
                  ? 'bg-primary text-text-inverse hover:bg-primary-hover'
                  : 'border border-border bg-bg text-text hover:bg-bg-alt'
              )}>
                {plan.cta}
              </button>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

---

## Blog Card Grid

```tsx
import Link from 'next/link'

type Post = { slug: string; title: string; excerpt: string; date: string; category: string; image?: string; readTime: string }

export function BlogGrid({ posts }: { posts: Post[] }) {
  return (
    <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
      {posts.map((post) => (
        <Link key={post.slug} href={`/blog/${post.slug}`} className="group flex flex-col">
          {post.image && (
            <div className="mb-4 aspect-video w-full overflow-hidden rounded-xl bg-bg-alt">
              <img src={post.image} alt={post.title} className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105" />
            </div>
          )}
          <div className="flex flex-1 flex-col rounded-xl border border-border bg-bg-card p-6 shadow-card transition-shadow group-hover:shadow-lg">
            <div className="mb-3 flex items-center gap-2">
              <span className="rounded-full bg-primary-light px-2.5 py-0.5 text-xs font-medium text-primary">{post.category}</span>
              <span className="text-xs text-text-faint">{post.readTime} read</span>
            </div>
            <h2 className="mb-2 font-display text-lg font-semibold text-heading transition-colors group-hover:text-primary line-clamp-2">{post.title}</h2>
            <p className="flex-1 text-sm text-text-muted line-clamp-3">{post.excerpt}</p>
            <time className="mt-4 text-xs text-text-faint">{post.date}</time>
          </div>
        </Link>
      ))}
    </div>
  )
}
```

---

## Contact Form

```tsx
'use client'
import { useState } from 'react'

export function ContactForm() {
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setStatus('loading')
    // Add your form submission logic here
    setTimeout(() => setStatus('success'), 1000)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div className="grid gap-5 sm:grid-cols-2">
        <div className="space-y-1.5">
          <label className="text-sm font-medium text-text">First name</label>
          <input type="text" required placeholder="John"
            className="w-full rounded-md border border-border bg-bg-input px-3 py-2 text-sm text-text placeholder-text-faint outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20" />
        </div>
        <div className="space-y-1.5">
          <label className="text-sm font-medium text-text">Last name</label>
          <input type="text" required placeholder="Doe"
            className="w-full rounded-md border border-border bg-bg-input px-3 py-2 text-sm text-text placeholder-text-faint outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20" />
        </div>
      </div>
      <div className="space-y-1.5">
        <label className="text-sm font-medium text-text">Email</label>
        <input type="email" required placeholder="you@example.com"
          className="w-full rounded-md border border-border bg-bg-input px-3 py-2 text-sm text-text placeholder-text-faint outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20" />
      </div>
      <div className="space-y-1.5">
        <label className="text-sm font-medium text-text">Subject</label>
        <input type="text" required placeholder="How can we help?"
          className="w-full rounded-md border border-border bg-bg-input px-3 py-2 text-sm text-text placeholder-text-faint outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20" />
      </div>
      <div className="space-y-1.5">
        <label className="text-sm font-medium text-text">Message</label>
        <textarea required rows={5} placeholder="Tell us more..."
          className="w-full resize-none rounded-md border border-border bg-bg-input px-3 py-2 text-sm text-text placeholder-text-faint outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/20" />
      </div>
      <button type="submit" disabled={status === 'loading'}
        className="w-full rounded-md bg-primary px-4 py-2.5 text-sm font-semibold text-text-inverse transition hover:bg-primary-hover disabled:opacity-50">
        {status === 'loading' ? 'Sending...' : status === 'success' ? 'Sent!' : 'Send message'}
      </button>
      {status === 'error' && <p className="text-center text-sm text-error">Something went wrong. Please try again.</p>}
    </form>
  )
}
```

---

## Legal Hub Page

```tsx
import Link from 'next/link'
import { Shield, FileText, RotateCcw } from 'lucide-react'

const legalPages = [
  { href: '/legal/privacy', icon: Shield, title: 'Privacy Policy', description: 'How we collect, use, and protect your data.' },
  { href: '/legal/terms', icon: FileText, title: 'Terms of Service', description: 'Rules and guidelines for using our platform.' },
  { href: '/legal/refund', icon: RotateCcw, title: 'Refund Policy', description: 'Our cancellation and refund procedures.' },
]

export default function LegalHubPage() {
  return (
    <div className="container mx-auto max-w-3xl px-6 py-16">
      <h1 className="mb-2 font-display text-4xl font-bold text-heading">Legal</h1>
      <p className="mb-10 text-text-muted">Everything you need to know about our policies.</p>

      <div className="grid gap-4">
        {legalPages.map(({ href, icon: Icon, title, description }) => (
          <Link key={href} href={href}
            className="group flex items-center gap-4 rounded-xl border border-border bg-bg-card p-6 shadow-card transition-all hover:border-primary/50 hover:shadow-lg">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-primary-light">
              <Icon size={22} className="text-primary" />
            </div>
            <div>
              <h2 className="font-display text-lg font-semibold text-heading group-hover:text-primary transition-colors">{title}</h2>
              <p className="text-sm text-text-muted">{description}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}
```

---

## Testimonials Grid

```tsx
const testimonials = [
  { quote: 'This product changed how our team works.', author: 'Jane Smith', role: 'CTO at Acme', avatar: '/avatars/jane.jpg', rating: 5 },
]

export function Testimonials() {
  return (
    <section className="py-20 bg-bg-alt">
      <div className="mx-auto max-w-7xl px-6">
        <h2 className="mb-12 text-center font-display text-4xl font-bold text-heading">Loved by teams worldwide</h2>
        <div className="columns-1 gap-6 sm:columns-2 lg:columns-3">
          {testimonials.map((t, i) => (
            <div key={i} className="mb-6 break-inside-avoid rounded-xl border border-border bg-bg-card p-6 shadow-card">
              <div className="mb-3 flex gap-0.5">
                {Array(5).fill(0).map((_, j) => (
                  <svg key={j} className={`h-4 w-4 ${j < t.rating ? 'text-yellow-400' : 'text-border'}`} fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <blockquote className="mb-4 text-sm leading-relaxed text-text">"{t.quote}"</blockquote>
              <div className="flex items-center gap-3">
                <div className="h-9 w-9 rounded-full bg-bg-alt" />
                <div>
                  <p className="text-sm font-semibold text-heading">{t.author}</p>
                  <p className="text-xs text-text-muted">{t.role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```
