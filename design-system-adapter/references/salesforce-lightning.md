# Salesforce Lightning Design System (SLDS)

> Source: https://www.lightningdesignsystem.com/ | https://www.lightningdesignsystem.com/design-tokens/
> Confidence: **Fully documented spec** (Salesforce is the pioneer of design tokens; SLDS publishes complete token repositories, CSS utilities, and accessibility standards).

## Core Principles (2–3 sentences)
SLDS is built to drive complex CRM, business operations, and enterprise customer workflows at scale. It prioritizes **high data density, visual hierarchy, clarity of state, and workflow acceleration**. Designed around explicit token categories (Color, Spacing, Sizing, Font, Elevation), SLDS supports both enterprise multi-tenant branding and deep theming without sacrificing enterprise ergonomics.

---

## Color System

SLDS organizes colors around semantic palettes: Brand, Neutral, Background, and Feedback.

### Semantic Tokens (SLDS Design Tokens)
| Token Name | Hex Value | Usage |
|---|---|---|
| `$color-brand` | `#0176D3` | Salesforce Lightning Brand Blue |
| `$color-brand-dark` | `#014486` | Brand button hover/active |
| `$color-background` | `#F3F3F3` | Global page / app canvas background |
| `$color-background-alt` | `#FFFFFF` | Primary card, tab panel, and table background |
| `$color-text-default` | `#181818` | Primary body text and labels |
| `$color-text-weak` | `#444444` | Secondary text, helper labels |
| `$color-border` | `#C9C9C9` | Input borders, card headers, table rows |
| `$color-border-separator` | `#E5E5E5` | Subtle horizontal dividers |
| `$color-background-success` | `#2E844A` | Completed stages, success toasts |
| `$color-background-warning` | `#FE9339` | Needs attention warnings |
| `$color-background-error` | `#EA001E` | Validation failures, destructive actions |

---

## Typography Scale

Font Stack:
- **Primary:** `'Salesforce Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`

| Step | Font Size | Line Height | Weight | Usage |
|---|---|---|---|---|
| `$font-size-heading-large` | 24px | 30px | 700 | Record home hero title |
| `$font-size-heading-medium` | 18px | 24px | 700 | Card headers, modal headers |
| `$font-size-heading-small` | 14px | 20px | 700 | Section headers, table header text |
| `$font-size-text-large` | 16px | 22px | 400 | Emphasized body text |
| `$font-size-text-medium` | 13px | 18px | 400 | Standard form inputs, grid cell content |
| `$font-size-text-small` | 11px | 14px | 400 | Field labels, timestamp metadata |

---

## Spacing & Layout Grid

- **Base unit:** 4px (with 16px default container padding)
- **Token Scale:**
  - `$spacing-xxx-small`: 2px
  - `$spacing-xx-small`: 4px
  - `$spacing-x-small`: 8px
  - `$spacing-small`: 12px
  - `$spacing-medium`: 16px
  - `$spacing-large`: 24px
  - `$spacing-x-large`: 32px
  - `$spacing-xx-large`: 48px
- **Density Modes:**
  - **Comfy (Standard):** 16px cell padding, 36px button heights.
  - **Compact (High density):** 8px cell padding, 28px button heights, ideal for rapid multi-record data entry.

---

## Elevation & Materiality Model

SLDS cards and surfaces rest flat on `#F3F3F3` with clean `1px solid #C9C9C9` borders and restrained shadows:
- `$elevation-shadow-0`: None
- `$elevation-shadow-1`: `0 2px 2px 0 rgba(0, 0, 0, 0.1)` (Cards, panels)
- `$elevation-shadow-2`: `0 4px 6px 0 rgba(0, 0, 0, 0.16)` (Dropdown popovers, pickers)
- `$elevation-shadow-3`: `0 8px 12px 0 rgba(0, 0, 0, 0.2)` (Modal dialogs)

---

## Corner Radius Conventions

- `$border-radius-small`: 2px (Badges, tag tokens)
- `$border-radius-medium`: 4px (Buttons, text inputs, standard cards)
- `$border-radius-large`: 8px (Modal dialog windows)
- `$border-radius-circle`: 50% (User profile avatar icons)

---

## Motion & Animation Principles

- **Durations:** `$duration-instantly` (0ms), `$duration-immediately` (50ms), `$duration-quickly` (100ms), `$duration-promptly` (200ms), `$duration-slowly` (400ms).
- **Easings:** Smooth cubic bezier curves: `cubic-bezier(0.1, 0, 0.1, 1)`.

---

## Iconography Style

- **System:** **SLDS Icons** (Utility, Standard, Action, Doctype).
- **Signature Icon Containers:** SLDS is famous for colored rounded square containers wrapping white utility icons (e.g. Accounts = Blue square with building icon, Leads = Orange square with person icon, Opportunities = Gold square with trophy icon).

---

## Accessibility Notes
- Meets Section 508 and WCAG 2.1 AA standards.
- Form inputs always use persistent `<label>` tags above inputs (`$font-size-text-small` at `#444444`).
- Focus rings: 2px solid `#0176D3` with high contrast against white inputs.

---

## Signature Visual "Tells"

1. **The "Path" stage progression:** Chevron-linked horizontal stage indicator bar (e.g. `Prospecting > Qualification > Needs Analysis > Closed Won`) with completed green and active blue segments.
2. **Colored square entity icons:** 32px $\times$ 32px rounded square containers with high-chroma backgrounds and white SVG glyphs representing CRM entities.
3. **Record Page Header:** Two-tier hero card with object icon, entity title, action button cluster on top right, and 4-column key field metadata row below.
4. **Salesforce Blue #0176D3:** Prominent brand blue across primary CTA buttons, active tabs, and interactive links.
5. **Restrained cards with header borders:** White card container placed on light gray background with distinct 1px border separating the card header from body.
