# DESIGN.md Template

This is the exact format to generate for every UI clone project.
Fill in every section based on your visual analysis of the screenshot.

---

# DESIGN.md — [Project Name]

> Generated from UI analysis. Single source of truth for all design tokens and component patterns.

---

## 1. Design Overview

| Property | Value |
|---|---|
| Style | e.g. "Modern SaaS, minimal, dark-accented" |
| Primary Audience | e.g. "B2B tech professionals" |
| Layout Type | e.g. "Full-width sections, boxed container (max-w-7xl)" |
| Mode | Light / Dark / Both |
| Base Spacing Unit | 4px / 8px |

---

## 2. Color Tokens

### 2.1 Brand & Accent

```css
:root {
  /* Brand */
  --color-primary:        #XXXXXX;  /* Primary CTA, links, highlights */
  --color-primary-hover:  #XXXXXX;  /* Primary on hover */
  --color-primary-light:  #XXXXXX;  /* Light tint of primary (bg use) */
  --color-secondary:      #XXXXXX;  /* Secondary accent */
  --color-secondary-hover:#XXXXXX;

  /* Backgrounds */
  --color-bg:             #XXXXXX;  /* Main page background */
  --color-bg-alt:         #XXXXXX;  /* Alternating section background */
  --color-bg-card:        #XXXXXX;  /* Card / panel background */
  --color-bg-input:       #XXXXXX;  /* Form input background */
  --color-bg-overlay:     rgba(0,0,0,0.5); /* Modal overlay */

  /* Text */
  --color-text:           #XXXXXX;  /* Primary body text */
  --color-text-muted:     #XXXXXX;  /* Secondary / supporting text */
  --color-text-faint:     #XXXXXX;  /* Placeholders, disabled */
  --color-text-inverse:   #XXXXXX;  /* Text on dark/primary backgrounds */
  --color-heading:        #XXXXXX;  /* Heading text (often same as text) */

  /* Borders */
  --color-border:         #XXXXXX;  /* Default border, dividers */
  --color-border-strong:  #XXXXXX;  /* Focused / prominent borders */

  /* Semantic */
  --color-success:        #XXXXXX;
  --color-success-bg:     #XXXXXX;
  --color-error:          #XXXXXX;
  --color-error-bg:       #XXXXXX;
  --color-warning:        #XXXXXX;
  --color-warning-bg:     #XXXXXX;
  --color-info:           #XXXXXX;
  --color-info-bg:        #XXXXXX;
}
```

### 2.2 Tailwind Mapping

Extend `tailwind.config.js` colors section with:

```js
colors: {
  primary: {
    DEFAULT: 'var(--color-primary)',
    hover: 'var(--color-primary-hover)',
    light: 'var(--color-primary-light)',
  },
  secondary: {
    DEFAULT: 'var(--color-secondary)',
    hover: 'var(--color-secondary-hover)',
  },
  bg: {
    DEFAULT: 'var(--color-bg)',
    alt: 'var(--color-bg-alt)',
    card: 'var(--color-bg-card)',
    input: 'var(--color-bg-input)',
  },
  text: {
    DEFAULT: 'var(--color-text)',
    muted: 'var(--color-text-muted)',
    faint: 'var(--color-text-faint)',
    inverse: 'var(--color-text-inverse)',
  },
  border: {
    DEFAULT: 'var(--color-border)',
    strong: 'var(--color-border-strong)',
  },
  success: 'var(--color-success)',
  error: 'var(--color-error)',
  warning: 'var(--color-warning)',
  info: 'var(--color-info)',
}
```

---

## 3. Typography

### 3.1 Font Families

```css
/* Google Fonts import (add to <head> or globals.css) */
@import url('https://fonts.googleapis.com/css2?family=HEADING_FONT:wght@400;500;600;700;800&family=BODY_FONT:wght@300;400;500;600&display=swap');

:root {
  --font-display:   'HEADING_FONT', system-ui, sans-serif;
  --font-body:      'BODY_FONT', system-ui, sans-serif;
  --font-mono:      'JetBrains Mono', 'Fira Code', monospace; /* if applicable */
}
```

```js
// tailwind.config.js
fontFamily: {
  display: ['var(--font-display)'],
  body:    ['var(--font-body)'],
  mono:    ['var(--font-mono)'],
}
```

### 3.2 Type Scale

| Token | Tailwind | px equiv | Weight | Line Height | Use |
|---|---|---|---|---|---|
| `text-display` | `text-5xl lg:text-7xl` | 48–72px | 800 | 1.05 | Hero headline |
| `text-h1` | `text-4xl lg:text-5xl` | 36–48px | 700 | 1.1 | Page title |
| `text-h2` | `text-3xl lg:text-4xl` | 30–36px | 700 | 1.15 | Section heading |
| `text-h3` | `text-xl lg:text-2xl` | 20–24px | 600 | 1.25 | Card/subsection heading |
| `text-h4` | `text-lg` | 18px | 600 | 1.3 | Small heading |
| `text-body-lg` | `text-lg` | 18px | 400 | 1.7 | Lead paragraph |
| `text-body` | `text-base` | 16px | 400 | 1.6 | Body copy |
| `text-body-sm` | `text-sm` | 14px | 400 | 1.5 | Supporting text |
| `text-caption` | `text-xs` | 12px | 500 | 1.4 | Labels, captions |
| `text-label` | `text-xs uppercase tracking-wider` | 12px | 600 | — | UI labels |

---

## 4. Spacing & Layout

### 4.1 Container

```css
.container {
  max-width: XXXXpx;   /* e.g. 1280px = max-w-7xl */
  padding-left: 24px;  /* px-6 */
  padding-right: 24px;
}
/* On lg: padding-left/right: 32px (px-8) */
```

### 4.2 Section Spacing

| Section Type | Top Padding | Bottom Padding | Tailwind |
|---|---|---|---|
| Hero | 80px | 80px | `py-20` |
| Content | 64px | 64px | `py-16` |
| Tight | 40px | 40px | `py-10` |
| Footer | 48px | 32px | `pt-12 pb-8` |

### 4.3 Grid System

```
Desktop:  12-column grid, gap-8 (32px)
Tablet:   8-column grid,  gap-6 (24px)
Mobile:   4-column grid,  gap-4 (16px)
```

---

## 5. Border Radius

```css
:root {
  --radius-none:   0px;
  --radius-sm:     4px;    /* rounded-sm — inputs, subtle cards */
  --radius-md:     8px;    /* rounded-md — cards, modals */
  --radius-lg:     12px;   /* rounded-lg — prominent cards */
  --radius-xl:     16px;   /* rounded-xl — hero cards */
  --radius-2xl:    24px;   /* rounded-2xl — featured sections */
  --radius-full:   9999px; /* rounded-full — pills, avatars */
}
```

```js
// tailwind.config.js
borderRadius: {
  none:  '0',
  sm:    'var(--radius-sm)',
  DEFAULT:'var(--radius-md)',
  md:    'var(--radius-md)',
  lg:    'var(--radius-lg)',
  xl:    'var(--radius-xl)',
  '2xl': 'var(--radius-2xl)',
  full:  'var(--radius-full)',
}
```

---

## 6. Shadows

```css
:root {
  --shadow-none:     none;
  --shadow-sm:       0 1px 2px 0 rgba(0,0,0,0.05);
  --shadow-md:       0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
  --shadow-lg:       0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
  --shadow-xl:       0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
  --shadow-card:     /* custom from screenshot */;
  --shadow-elevated: /* custom from screenshot */;
}
```

```js
// tailwind.config.js
boxShadow: {
  sm:       'var(--shadow-sm)',
  DEFAULT:  'var(--shadow-md)',
  md:       'var(--shadow-md)',
  lg:       'var(--shadow-lg)',
  xl:       'var(--shadow-xl)',
  card:     'var(--shadow-card)',
  elevated: 'var(--shadow-elevated)',
  none:     'none',
}
```

---

## 7. Component Specs

### 7.1 Buttons

| Variant | Background | Text | Border | Hover |
|---|---|---|---|---|
| Primary | `bg-primary` | `text-text-inverse` | none | `bg-primary-hover` |
| Secondary | `bg-secondary` | `text-text-inverse` | none | `bg-secondary-hover` |
| Outline | transparent | `text-primary` | `border border-primary` | `bg-primary-light` |
| Ghost | transparent | `text-text-muted` | none | `bg-bg-alt text-text` |
| Destructive | `bg-error` | white | none | darker red |
| Link | transparent | `text-primary` | none | underline |

| Size | Height | Padding | Font Size | Border Radius |
|---|---|---|---|---|
| xs | 28px | `px-2.5 py-1` | `text-xs` | `rounded` |
| sm | 32px | `px-3 py-1.5` | `text-sm` | `rounded` |
| md | 40px | `px-4 py-2` | `text-sm` | `rounded-md` |
| lg | 48px | `px-6 py-3` | `text-base` | `rounded-md` |
| xl | 56px | `px-8 py-4` | `text-lg` | `rounded-lg` |

### 7.2 Inputs

```
Height:         40px (md) / 48px (lg)
Padding:        px-3 py-2
Background:     bg-bg-input
Border:         border border-border
Border Radius:  rounded-md
Focus:          ring-2 ring-primary border-primary
Error:          border-error ring-2 ring-error/20
Placeholder:    text-text-faint
Font size:      text-sm (14px)
```

### 7.3 Cards

```
Background:     bg-bg-card
Border:         border border-border (or none)
Border Radius:  rounded-lg / rounded-xl (from screenshot)
Shadow:         shadow-card (from screenshot)
Padding:        p-6 (standard) / p-4 (compact)
Hover:          shadow-lg transition-shadow (if interactive)
```

### 7.4 Badges / Tags

| Variant | Background | Text |
|---|---|---|
| Default | `bg-bg-alt` | `text-text-muted` |
| Primary | `bg-primary-light` | `text-primary` |
| Success | `bg-success-bg` | `text-success` |
| Error | `bg-error-bg` | `text-error` |
| Warning | `bg-warning-bg` | `text-warning` |

```
Height: 20-24px
Padding: px-2.5 py-0.5
Font: text-xs font-medium
Radius: rounded-full (pill) or rounded (subtle)
```

### 7.5 Navigation

```
Header height:     64px (h-16) desktop / 56px mobile
Logo width:        ~120-160px (from screenshot)
Nav link style:    text-sm font-medium text-text-muted hover:text-text
Active nav link:   text-primary font-semibold
CTA button:        Primary or Outline button, sm/md size
Mobile menu:       Full-screen or slide-in drawer
Sticky:            Yes/No (from screenshot)
Background:        bg-bg or bg-bg/95 backdrop-blur-sm (if frosted)
Bottom border:     border-b border-border (if visible)
```

---

## 8. Animation Tokens

```css
:root {
  --transition-fast:   150ms ease;
  --transition-base:   200ms ease;
  --transition-slow:   300ms ease;
  --transition-slower: 500ms ease;
}
```

```js
// tailwind.config.js
transitionDuration: {
  fast:   '150ms',
  base:   '200ms',
  slow:   '300ms',
  slower: '500ms',
}
```

---

## 9. Section Inventory

List every visible section from the screenshot:

| # | Section Name | Component File | Key Elements |
|---|---|---|---|
| 1 | Hero | `Hero.tsx` | Headline, subheading, CTA, bg image/gradient |
| 2 | Features | `Features.tsx` | 3-col icon cards |
| 3 | Testimonials | `Testimonials.tsx` | Carousel or grid |
| 4 | Pricing | `Pricing.tsx` | Toggle monthly/annual, 3 tiers |
| 5 | CTA Banner | `CTABanner.tsx` | Full-width, primary bg |
| ... | ... | ... | ... |

---

## 10. Required Routes Reference

All routes that must be implemented:

| Route | Component/Page | Notes |
|---|---|---|
| `/` | `HomePage` | Cloned from screenshot |
| `/about` | `AboutPage` | Company info, team |
| `/contact` | `ContactPage` | Form + map/info |
| `/faq` | `FAQPage` | Accordion list |
| `/blog` | `BlogListPage` | Card grid |
| `/blog/[slug]` | `BlogDetailPage` | Full article layout |
| `/login` | `LoginPage` | Auth form |
| `/register` | `RegisterPage` | Sign up form |
| `/forgot-password` | `ForgotPasswordPage` | Email input |
| `/reset-password` | `ResetPasswordPage` | New password form |
| `/otp` | `OTPPage` | 6-digit code input |
| `/legal` | `LegalHubPage` | Links to legal pages |
| `/legal/privacy` | `PrivacyPage` | Privacy policy |
| `/legal/terms` | `TermsPage` | Terms of service |
| `/legal/refund` | `RefundPage` | Refund policy |
