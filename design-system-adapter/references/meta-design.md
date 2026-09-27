# Meta Design System (Astryx)

> Source: https://github.com/facebook/astryx | https://atmeta.com/
> Note: Meta operates 20+ internal design systems. Astryx (open-sourced June 2026) is the
> official public reference system powering 13,000+ internal applications.

## Core Principles (2–3 sentences)
Meta's design philosophy centres on **scale, clarity, and social context** — interfaces must work across billions of users on wildly different devices and network conditions, so they prioritise load speed and content density over decorative flair. Astryx is "token-first" and "AI-fluent": every visual decision is a CSS custom property that can be overridden for product-level theming (Facebook, Instagram, Messenger each have distinct tokens on the same foundation). Accessibility is non-negotiable — every component ships with WCAG AA compliance built in, and dark mode is a first-class concern from day one.

---

## Color System

Meta does not use a single brand colour across all products. Each product has its own palette layer, but all share the same token naming convention:

### Facebook-flavoured (reference implementation)
| Token | Light | Dark | Usage |
|---|---|---|---|
| `$blueBase` / `--color-brand` | `#1877F2` | `#2D88FF` | Primary CTA, links |
| `$blueDark` | `#166FE5` | — | Button hover |
| `$white` | `#FFFFFF` | — | Surface (light) |
| `$black` | `#000000` | — | Surface (dark) |
| `--bg-base` | `#FFFFFF` | `#18191A` | Root background |
| `--bg-surface` | `#F0F2F5` | `#242526` | Card/panel background |
| `--bg-hover` | `#E4E6EB` | `#3A3B3C` | Hover state |
| `--text-primary` | `#050505` | `#E4E6EB` | Primary text |
| `--text-secondary` | `#65676B` | `#B0B3B8` | Secondary text |
| `--text-placeholder` | `#8A8D91` | `#8A8D91` | Input placeholders |
| `--border-default` | `#CED0D4` | `#3E4042` | Dividers, card borders |
| `--color-success` | `#42B72A` | `#45BD62` | Confirm, success |
| `--color-error` | `#E02E2E` | `#FA3E3E` | Errors, destructive |

### Dark Mode
Meta's dark mode is deeper than most — `#18191A` background is near-black, surfaces are `#242526` and `#3A3B3C`. This creates a stark, OLED-friendly dark palette.

### Theming
CSS custom properties cascade from `:root` theme tokens down to component-level overrides. Each product line imports the foundation then overrides brand-level tokens.

---

## Typography Scale

Meta uses the system font stack by default (no proprietary typeface for Astryx). For Facebook specifically, **Facebook Clarity** is the app font, but it is proprietary.

Font stack: `system-ui, -apple-system, BlinkMacSystemFont, '.SFNSText-Regular', 'Helvetica Neue', Helvetica, Arial, sans-serif`

| Role | Size | Weight | Line Height |
|---|---|---|---|
| Display | 32px | 700 | 40px |
| Heading 1 | 24px | 700 | 32px |
| Heading 2 | 20px | 700 | 28px |
| Heading 3 | 17px | 600 | 24px |
| Body / Default | 15px | 400 | 20px |
| Secondary | 13px | 400 | 18px |
| Caption | 12px | 400 | 16px |
| Label | 11px | 600 | 14px |

**Facebook-specific:** Body text is 15px (slightly smaller than industry standard 16px) — this higher density is intentional for feed contexts. Never go below 11px for any visible text.

---

## Spacing & Layout Grid

- **Base unit:** 8px (multiples: 4, 8, 12, 16, 20, 24, 32, 40, 48)
- **Content feed width:** Max 680px (desktop Facebook feed), full-width on mobile
- **Panel/sidebar width:** 280px (right rail), 360px (extended)
- **Card padding:** 12–16px
- **Between-card gap:** 8px (feed is dense — no large white gaps)
- **Border-box sizing everywhere** — always `box-sizing: border-box`

---

## Elevation Model

Meta uses **subtle drop shadows** — no tonal overlays, no blur materials.

| Level | Box Shadow | Usage |
|---|---|---|
| Resting | `0 1px 2px rgba(0,0,0,0.1)` | Cards in feed |
| Lifted | `0 2px 4px rgba(0,0,0,0.1), 0 8px 16px rgba(0,0,0,0.1)` | Menus, dropdowns |
| Floating | `0 4px 12px rgba(0,0,0,0.15), 0 12px 28px rgba(0,0,0,0.12)` | Modals, panels |

Dark mode: shadows are lighter (rgba values at 60% of light-mode opacity) because dark backgrounds provide inherent separation.

---

## Corner Radius Conventions

| Context | Radius |
|---|---|
| Buttons (primary, small) | 6px |
| Buttons (large) | 8px |
| Buttons (pill, e.g. "Like") | 9999px |
| Cards, panels | 8px |
| Inputs (text fields) | 6px |
| Avatars (circle) | 50% |
| Story rings | 50% |
| Tooltips | 4px |
| Modal/dialog | 8px |

Facebook uses **consistent 8px radius for containers** — more rounded than GitHub, less than Material 3.

---

## Motion Principles

- **Fast and invisible** — animations should not delay task completion
- Standard transition: `all 0.1s ease-in-out` for hover states
- Modal open: fade + subtle scale (0.98→1.0) — `0.2s ease-out`
- Toast/notification slide: slide in from right/top — `0.25s cubic-bezier(0.08,0.82,0.17,1)`
- Reaction animation: spring pop on emoji — `0.3s cubic-bezier(0.34,1.56,0.64,1)`
- **No heavy page transitions** — navigation is near-instant (SPA with minimal animation)

---

## Iconography

- Meta uses a **custom icon set** for each product (no open-source icon library)
- **Astryx ships with Phosphor Icons** as its open-source component icon set
- NPM: `phosphor-react` or `@phosphor-icons/react`
- Default style: Regular (outline); Filled for selected/active states
- Size: 16px (compact UI), 20px (standard), 24px (feature/hero)
- Facebook uses its own 24dp filled icon set — not publicly available

---

## 5 Signature "Tells" — Unmistakably Meta/Facebook Design

1. **`#1877F2` Facebook Blue** — the primary action colour is this specific shade of mid-blue; no ambiguity
2. **Dense, card-heavy feed layout** — content packed into 680px max-width feed column, cards at 8px gap
3. **Near-black dark mode** — `#18191A` background is deeper than most dark modes; surfaces have very low lightness delta
4. **System font at 15px** — body text is 1px smaller than most web conventions, creating higher content density
5. **Pill-shaped reaction buttons** — the rounded-full "Like / Love / Haha" buttons are unmistakably Facebook
